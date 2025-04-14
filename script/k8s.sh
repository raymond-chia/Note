#!/usr/bin/env bash

# # 找 name 有 api 名稱的 pods
# kubectl get pods -o json | jq '.items.[] | select(.metadata.name | contains("api"))'
# 統計每個 node 有幾個 pod
kubectl get pods -o json | jq '[.items.[] | select(.status.phase == "Running") | select(.metadata.name | contains("api"))]
    | group_by(.spec.nodeName)
    | sort | .[]
    | {node: first.spec.nodeName, count: length}
    | {node: .node, count: .count, zone: .node|split("-")[7]}' \
    | jq -s \
    | jq 'group_by(.zone)
    | map({node: .[0].node, zone: .[0].zone, count: map(.count)|add})'
# 或者
kubectl get pods -o wide | grep -v NODE | awk '{print $7}' | cut -d "-" -f 8 | sort | uniq -c

# # 設定 image
# # https://kubernetes.io/docs/reference/kubectl/generated/kubectl_set/kubectl_set_image/
# # https://stackoverflow.com/questions/40366192/kubernetes-how-to-make-deployment-to-update-image
# kubectl set image

# 檢查 image
# https://kubernetes.io/docs/tasks/access-application-cluster/list-all-running-container-images/
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.image}{", "}{end}{end}'
