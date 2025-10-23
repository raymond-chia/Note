#!/usr/bin/env bash

# 遇到未宣告變數 (u) 或執行失敗 (e) 時會立即終止
set -eu

PROJECT_ID="$1"
EXPORT_BUCKET="$2"
RESTORE_TIME="$3"
DATABASE="${4:-"(default)"}" # 預設為 (default)，可自訂

usage() {
  echo "用法: $0 <project_id> <export_bucket_name> <restore_time> [database_id]"
  echo
  echo "date -u +\"%Y-%m-%dT%H:%M:%SZ\" 可取得 RFC3339 格式的 UTC 時間"
  exit 1
}

if [ -z "$PROJECT_ID" ] || [ -z "$EXPORT_BUCKET" ] || [ -z "$RESTORE_TIME" ]; then
  usage
fi

# 檢查 RFC3339 格式
if ! [[ "$RESTORE_TIME" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]]; then
  echo "錯誤：還原時間格式不正確，請使用 RFC3339 格式 (如 2025-09-05T02:00:00Z)"
  echo
  usage
fi

EARLIEST_TIME=$(gcloud firestore databases describe \
  --database="$DATABASE" \
  --project="$PROJECT_ID" \
  --format="value(earliestVersionTime)")

echo "最早可還原時間: $EARLIEST_TIME"

if [ -z "$EARLIEST_TIME" ]; then
  echo "PITR 尚未啟用或尚未產生資料，請確認狀態。"
  exit 1
fi
if ! EARLIEST_TS=$(date -u -d "$EARLIEST_TIME" +%s 2>/dev/null); then
  echo "錯誤：最早可還原時間格式異常，請檢查 Firestore 狀態"
  exit 1
fi
if ! RESTORE_TS=$(date -u -d "$RESTORE_TIME" +%s 2>/dev/null); then
  echo "錯誤：指定還原時間出現不明問題, 請檢查格式: $RESTORE_TIME"
  exit 1
fi
# 比較還原時間與最早可還原時間
if [[ "$RESTORE_TS" -lt "$EARLIEST_TS" ]]; then
  echo "錯誤：指定還原時間 ($RESTORE_TIME) 早於最早可還原時間 ($EARLIEST_TIME)，無法還原。"
  exit 1
fi

echo "正在 export Firestore 資料庫 $DATABASE 的 PITR $RESTORE_TIME 至 $EXPORT_BUCKET ..."

EXPORT_RESULT=$(gcloud firestore export "gs://$EXPORT_BUCKET" \
  --project="$PROJECT_ID" \
  --database="$DATABASE" \
  --snapshot-time="$RESTORE_TIME")
OUTPUT_URI=$(echo "$EXPORT_RESULT" | grep outputUriPrefix | awk '{print $2}')
echo "=============================="
echo "outputUriPrefix: $OUTPUT_URI"
echo "=============================="
