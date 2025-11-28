#!/bin/bash

# =================================================================
# 這段程式碼會顯示指定 GKE 節點上所有 Pod 的 CPU 和記憶體用量
# 節點名稱由指令列參數傳入
#
# 使用方式:
# ./check_node_pods.sh <node-name>
#
# 範例:
# ./check_node_pods.sh gke-prod-v1-asia-east2-pool-v1-688ba1ba-vs8m
# =================================================================

# 從第一個指令列參數 ($1) 讀取節點名稱
NODE_NAME=$1

# 檢查使用者是否提供了節點名稱參數
if [ -z "$NODE_NAME" ]; then
    echo "錯誤: 請提供 GKE 節點名稱作為參數。"
    echo "使用方式: $0 <node-name>"
    exit 1
fi

# 檢查 kubectl 是否存在
if ! command -v kubectl &> /dev/null
then
    echo "錯誤: 'kubectl' 指令未找到。請確認您已經安裝並設定好 kubectl。"
    exit 1
fi

# 顯示節點的資源用量
kubectl top node "$NODE_NAME"

echo "================================================================================================="
echo "正在查詢節點 '$NODE_NAME' 上的 Pod 資源用量..."
echo "================================================================================================="

# 取得在指定節點上運行的所有 Pod 的列表
# 使用 -o jsonpath 可以更精準地取得資訊，避免在 Pod 名稱或 namespace 包含空白時出錯
PODS_ON_NODE=$(kubectl get pods --all-namespaces --field-selector spec.nodeName="$NODE_NAME" -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.metadata.namespace}{"\n"}{end}')

if [ -z "$PODS_ON_NODE" ]; then
    echo "在節點 '$NODE_NAME' 上找不到任何 Pod，或節點名稱錯誤。"
    exit 0
fi

# 只顯示 header
HEADER=$(kubectl top pod | head -n 1)
echo "$HEADER"

# 迴圈處理每一個 Pod，並使用 kubectl top pod 取得其資源用量
echo "$PODS_ON_NODE" | while read -r POD_NAME NAMESPACE; do
    if [ -n "$POD_NAME" ]; then
        # 取得該 Pod 的資源用量並顯示，同時抑制找不到 metric 的錯誤訊息
        kubectl top pod "$POD_NAME" -n "$NAMESPACE" 2>/dev/null | tail -n +2
    fi
done

echo "================================================================================================="
echo "查詢完成。"
