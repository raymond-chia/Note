#!/bin/bash

# 初始化計數器
declare -A distribution
total=0
sample_size=1000

# 使用 process substitution 來避免子 shell 問題
while read -r key; do
    ttl=$(redis-cli ttl "$key")
    
    # 跳過不存在的 key
    if [ $ttl -eq -2 ]; then
        continue
    fi
    
    # 計算總數
    ((total++))
    
    # 分類 TTL
    if [ $ttl -eq -1 ]; then
        distribution["no_expiry"]=$((${distribution["no_expiry"]} + 1))
    elif [ $ttl -le 86400 ]; then  # 一天(24小時)以內
        hours=$(( (ttl + 3599) / 3600 ))  # 向上取整
        key="<${hours}hr"
        distribution[$key]=$((${distribution[$key]} + 1))
    else
        days=$(( (ttl + 86399) / 86400 ))  # 向上取整
        key="<${days}days"
        distribution[$key]=$((${distribution[$key]} + 1))
    fi
done < <(redis-cli --scan | head -n $sample_size)

# 顯示結果
echo "Sample size: $total"

# 先印出 no_expiry
if [ ${distribution["no_expiry"]+_} ]; then
    echo "no_expiry: ${distribution["no_expiry"]}"
fi

# 印出小時
for i in $(seq 1 24); do
    key="<${i}hr"
    if [ ${distribution[$key]+_} ]; then
        echo "$key: ${distribution[$key]}"
    fi
done

# 印出天數
# 先取得所有天數並排序
for key in "${!distribution[@]}"; do
    if [[ $key == "<"*"days" ]]; then
        echo "$key: ${distribution[$key]}"
    fi
done | sort -t'<' -k2 -n
