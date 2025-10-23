#!/usr/bin/env bash

BUCKET=$1

declare -A normal
discarding=()

# TODO --recursive for files in directories
# --recursive or gs://$BUCKET/**
for i in $(gcloud storage ls "gs://$BUCKET"); do
  normal["$i"]=0
done
for i in $(gcloud storage ls "gs://$BUCKET" -a); do
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
done

echo deleting the followings
for i in "${discarding[@]}"; do
  echo "$i"
done
echo "Press Enter to continue..."
read -r
for i in "${discarding[@]}"; do
  gcloud storage rm "$i"
done
