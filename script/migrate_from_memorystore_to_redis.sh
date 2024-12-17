#!/usr/bin/env bash

PROJECT_ID=""
BUCKET_NAME=""
FILE_NAME=""
INSTANCE_ID=""
REGION=asia-east1

function export_rdb() {
  gcloud redis instances export gs://$BUCKET_NAME/$FILE_NAME.rdb $INSTANCE_ID --region=$REGION --project=$PROJECT_ID
}

function import_rdb() {
  OBJECT_NAME="$FILE_NAME.rdb"
  DIR=$(redis-cli CONFIG GET dir | grep -v -e dir)
  DB_FILENAME=$(redis-cli CONFIG GET dbfilename | grep -v -e dbfilename)

  redis-cli CONFIG SET appendonly no
  redis-cli CONFIG REWRITE
  systemctl stop redis.service
  systemctl status redis.service # 要看到 Active: inactive (dead)
  gcloud storage cp gs://$BUCKET_NAME/$OBJECT_NAME "$DIR/$DB_FILENAME"
  systemctl start redis.service
  systemctl status redis.service # 要看到 Active: active (running)
  redis-cli CONFIG SET appendonly yes
  redis-cli CONFIG REWRITE
}

function check_status() {
  gcloud redis instances describe $INSTANCE_ID --region=$REGION --project=$PROJECT_ID
  gcloud redis operations list --region=$REGION --project=$PROJECT_ID
  cd /var/log/redis || exit 1
  cat /etc/redis/redis.conf | grep appendonly
  ls -lh /data/db
}

export_rdb
