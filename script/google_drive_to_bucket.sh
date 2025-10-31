#!/bin/sh

set -eu

SOURCE="drive:"
DEST="bucket:bucket_name"

echo "正在從 $SOURCE 複製檔案到 $DEST ..."

SOURCE_FILES="/tmp/source_files.txt"
if ! rclone lsf "$SOURCE" --max-depth 2 --files-only > "$SOURCE_FILES"; then
    echo "錯誤: 無法列出來源檔案" >&2
    exit 1
fi

while read -r file; do
  # 取得不含路徑的檔案名稱
  filename=$(basename "$file")
  echo "正在複製: $file  ->  $filename"
  # 執行複製，--progress 會顯示進度
  rclone copyto --gcs-bucket-policy-only --progress "$SOURCE/$file" "$DEST/$filename"
done < "$SOURCE_FILES"
echo "複製完成！"



SOURCE_FILENAMES="/tmp/source_filenames.txt"
DEST_FILES="/tmp/dest_files.txt"
DIFF_FILES="/tmp/diff.txt"

echo "正在準備刪除多餘的檔案..."

# 1. 取得來源端所有第一層子資料夾內的檔案名稱，並排序
rclone lsf "$SOURCE" --max-depth 2 --files-only | while read -r f; do basename "$f"; done | sort > "$SOURCE_FILENAMES"

# 2. 取得目的地端所有檔案名稱，並排序
rclone lsf "$DEST" | sort > "$DEST_FILES"

echo "--------------------------------------------------"
echo "以下檔案存在於目的地 Bucket, 但不存在於來源 Drive 中:"
echo "(這些是下一步將要刪除的檔案)"
echo "--------------------------------------------------"
comm -13 "$SOURCE_FILENAMES" "$DEST_FILES" > "$DIFF_FILES"
cat "$DIFF_FILES"
echo "--------------------------------------------------"
echo "準備刪除多餘的檔案..."

# 3. 比較並找出要刪除的檔案，然後逐一刪除
while read -r file_to_delete; do
  if [ -n "$file_to_delete" ]; then
    echo "正在刪除: $file_to_delete"
    rclone deletefile --progress "$DEST/$file_to_delete"
  fi
done < "$DIFF_FILES"

echo "多餘檔案刪除完成。"
