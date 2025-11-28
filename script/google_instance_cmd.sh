#!/bin/bash

# 定義要執行的命令。
# 使用 Here Document 的寫法，可讀性高且安全。
read -r -d '' COMMAND <<'EOF'
sudo ctr --namespace k8s.io images list 'labels."io.containerd.image/converted-docker-schema1"'
EOF

echo "準備在每個 GKE 節點實例上執行以下命令："
echo "$COMMAND"
echo "--------------------------------------------------------"

# 檢查必要的參數
if [ -z "$1" ]; then
  echo "錯誤：缺少必要的參數。"
  echo "用法: $0 YOUR_PROJECT_ID [INSTANCE_NAME_PREFIX]"
  exit 1
fi

# 從參數設定變數
PROJECT_ID="$1"
INSTANCE_PREFIX="$2" # 第二個參數是可選的，如果不存在，此變數為空

# --filter 旗標是 gcloud 過濾實例的關鍵
# 我們使用一個陣列來安全地構建命令，避免引號問題
GCLOUD_CMD=(
  "gcloud"
  "compute"
  "instances"
  "list"
  "--project=$PROJECT_ID"
  "--format=value[separator=','](name,zone)"
)

if [ -n "$INSTANCE_PREFIX" ]; then
  echo "正在從專案 [$PROJECT_ID] 獲取並排序名稱以前綴 [$INSTANCE_PREFIX] 開頭的實例..."
  # 如果提供了前綴，將 --filter 旗標添加到命令陣列中
  # name~^... 使用正則表達式來匹配開頭
  GCLOUD_CMD+=("--filter=name~^$INSTANCE_PREFIX")
else
  echo "正在從專案 [$PROJECT_ID] 獲取並排序所有實例..."
fi

# 執行 gcloud 命令並將結果存儲到變數中
# "${GCLOUD_CMD[@]}" 會安全地展開陣列中的所有元素
INSTANCES=$("${GCLOUD_CMD[@]}" | sort)

# 檢查是否找到了任何實例
if [ -z "$INSTANCES" ]; then
  if [ -n "$INSTANCE_PREFIX" ]; then
    echo "在專案 $PROJECT_ID 中未找到任何名稱以前綴 [$INSTANCE_PREFIX] 開頭的實例。"
  else
    echo "在專案 $PROJECT_ID 中未找到任何實例。"
  fi
  exit 0
fi

echo
echo "掃描將按以下順序進行。"
echo "找到的實例列表:"
echo -e "$INSTANCES\n"
read -rp "請按 [Enter] 鍵開始逐一在實例上執行命令，或按 Ctrl+C 中斷..."
echo "--------------------------------------------------------"

# 遍歷每個實例並執行命令
while IFS=',' read -r INSTANCE_NAME INSTANCE_ZONE; do
  # 忽略可能產生的空行
  if [ -z "$INSTANCE_NAME" ]; then
    continue
  fi

  echo "下一個實例: $INSTANCE_NAME (區域: $INSTANCE_ZONE)"

  # 執行 SSH 命令。
  # 【重要】: 這裡的 command 字串使用了複雜的引號來確保命令在遠端伺服器上被正確解析。
  # 並且使用 `< /dev/null` 將標準輸入重定向，以防止 gcloud/ssh 命令消耗掉 while 迴圈的輸入流。
  if ! gcloud compute ssh "$INSTANCE_NAME" --zone="$INSTANCE_ZONE" --project="$PROJECT_ID" \
    --command="$COMMAND" < /dev/null; then
    echo "警告: 在實例 $INSTANCE_NAME 上執行命令時發生錯誤。請檢查權限或實例狀態。"
  fi

  echo "已完成實例: $INSTANCE_NAME 的檢查。"
  echo "--------------------------------------------------------"
done <<< "$INSTANCES"

echo "所有符合條件的實例皆已執行完畢。"