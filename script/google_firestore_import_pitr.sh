#!/usr/bin/env bash

# 遇到未宣告變數 (u) 或執行失敗 (e) 時會立即終止
set -eu

PROJECT_ID="$1"
IMPORT_SOURCE="$2"
DATABASE="${3:-"(default)"}" # 預設為 (default)，可自訂

usage() {
  echo "用法: $0 <project_id> <import_source> [database_id]"
  echo
  echo "import_source 應為 export 時回傳的 outputUriPrefix"
  exit 1
}

if [ -z "$PROJECT_ID" ] || [ -z "$IMPORT_SOURCE" ]; then
  usage
fi

echo "正在從 $IMPORT_SOURCE 匯入 Firestore 資料庫 $DATABASE ..."

gcloud firestore import "$IMPORT_SOURCE" \
  --project="$PROJECT_ID" \
  --database="$DATABASE"
