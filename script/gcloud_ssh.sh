#!/usr/bin/env bash

set -eu

function usage() {
  cat << EOF
USAGE:
      $0 --project <project id>
EOF
}

function main() {
  dbtype="mongo"

  gcloud compute instances list --project="$project" | grep "$dbtype"
  read -rp "pick a vm: " vm
  gcloud compute ssh --project="$project" "$vm"
}

if [ "${BASH_SOURCE[0]}" != "$0" ]; then
  usage
  exit 1
fi

# 解析 named 參數
# https://distroid.net/how-to-pass-a-named-argument-in-a-bash-script
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
      IFS='=' read -ra splitted <<< "$1";
      project=${splitted[1]};
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
