# pip install google-cloud-logging

from google.cloud import logging as cloud_logging
from datetime import datetime, timezone, timedelta
import json

project = ""
start_time = datetime(2026, 1, 7, 3, 50, 0, tzinfo=timezone.utc)
end_time = datetime(2026, 1, 7, 4, 5, 0, tzinfo=timezone.utc)

# 構建過濾條件
filter_str = (
    ""
    f' AND timestamp>="{start_time.isoformat()}"'
    f' AND timestamp<="{end_time.isoformat()}"'
)

if not project:
    print("請填寫參數")

print(f"查詢過濾條件：{filter_str}\n")

# 查詢日誌
logging_client = cloud_logging.Client(project=project)
entries = logging_client.list_entries(filter_=filter_str, page_size=1000)

# 列出結果
count = 0
for entry in entries:
    count += 1
    timestamp = entry.timestamp

    # 提取 resource 資訊 (根據 filter 的結構)
    resource_name = entry.labels.get("compute.googleapis.com/resource_name", "unknown")
    instance_id = entry.resource.labels.get("instance_id", "unknown")
    zone = entry.resource.labels.get("zone", "unknown")

    # 提取 payload
    if isinstance(entry.payload, dict):
        # 如果是結構化 log
        payload_dict = entry.payload.copy()
        # 添加 resource 資訊到 payload
        payload_dict["_resource_name"] = resource_name
        payload_dict["_instance_id"] = instance_id
        payload_dict["_zone"] = zone
        message = json.dumps(payload_dict, indent=2)
    else:
        # 如果是純文字 log
        message = entry.payload

    print(f"[{timestamp}] {message}\n")

print(f"\n總共找到 {count} 條日誌")
