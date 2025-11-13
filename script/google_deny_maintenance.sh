#!/usr/bin/env bash

# 檢查參數
if [ $# -ne 3 ]; then
  echo "Usage: $0 <PROJECT> <START_DATE> <END_DATE>"
  echo "Example: $0 my-gcp-project 2025-11-03 2025-11-10"
  exit 1
fi

PROJECT=$1
START=$2
END=$3

for instance in $(gcloud --project "$PROJECT" sql instances list --format="value(name)"); do
  gcloud --project "$PROJECT" sql instances patch "$instance" \
    --deny-maintenance-period-start-date "$START" \
    --deny-maintenance-period-end-date "$END" \
    --deny-maintenance-period-time 00:00:00 # 08:00:00 UTC+8
done
