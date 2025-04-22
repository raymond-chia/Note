#!/usr/bin/env bash

set -e

function usage() {
  cat << EOF
USAGE:
      $0 --project <project id>
EOF
}

function main() {
  local DB_TYPE="mongo"

  gcloud compute instances list --project="$project" | grep "$DB_TYPE"
  read -rp "pick a vm: " vm
  gcloud compute ssh --project="$project" "$vm"

  # # TODO
  # gcloud --project="$project" compute ssh $VM_NAME -- -N -L 9999:$MONGO_VM_NAME:27017
  # # need iap permission
  # gcloud --project="$project" compute start-iap-tunnel $MONGO_VM_NAME 27017 --local-host-port=localhost:9999
}

if [ "${BASH_SOURCE[0]}" != "$0" ]; then
  usage
  exit 1
fi

# 解析 named 參數
# $# 代表參數數量
# https://stackoverflow.com/questions/402377/using-getopts-to-process-long-and-short-command-line-options
while [ "$#" -gt 0 ]
do
  case "$1" in
    --project)
      project="$2";
      shift;
      ;;
    --project=*)
      # https://stackoverflow.com/questions/918886/how-do-i-split-a-string-on-a-delimiter-in-bash
      IFS='=' read -ra split <<< "$1";
      project=${split[1]};
      ;;
  esac
  shift;
done

# https://stackoverflow.com/questions/18096670/what-does-z-mean-in-bash
if [[ -z "$project" ]]; then
  echo "Wrong number of arguments are passed."
  usage
  exit 1
fi

main "$@"
