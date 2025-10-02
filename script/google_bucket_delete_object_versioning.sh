#!/usr/bin/env bash

BUCKET=$1

declare -A normal
discarding=()

# 用 for loop 要特別處理空白的檔案名稱 (例如改 IFS)
# 否則會被拆成好幾個 loop
while read -r i; do
  normal["$i"]=0
done < <(gcloud storage ls "gs://$BUCKET")
while read -r i; do
  file=${i%#*}
  version=${i##*#}
  if [[ -z "${normal[$file]}" ]]; then
    discarding+=("$i")
  elif [[ "${normal[$file]}" < $version  ]]; then
    if [[ "${normal[$file]}" != 0 ]]; then
      discarding+=("$file#${normal[$file]}")
    fi
    normal["$file"]=$version
  else
    echo PANIC: invalid file and version "$i"
  fi
done < <(gcloud storage ls "gs://$BUCKET" -a)

echo deleting the followings
for i in "${discarding[@]}"; do
  echo "$i"
done
for i in "${discarding[@]}"; do
  gcloud storage rm "$i"
done
