#!/usr/bin/env python3
"""
查詢 BigQuery 每個 dataset 中各個 table 前綴最新的 table
用法: python3 bigquery-last-sharding.py <project-id>
範例: python3 bigquery-last-sharding.py my-gcp-project
"""

from google.cloud import bigquery
from collections import defaultdict
import re
import sys

# 常見的日期後綴模式
DATE_PATTERNS = [
    r"_\d{8}$",  # _20240101
    r"_\d{4}_\d{2}_\d{2}$",  # _2024_01_01
    r"\$\d{8}$",  # $20240101 (舊式分片表)
    r"_\d{10}$",  # _2024010100 (帶小時)
]


def extract_table_prefix(table_name: str) -> str:
    """
    從 table 名稱中提取前綴（去除日期後綴）

    參數：
        table_name: 完整的 table 名稱

    返回：
        table 前綴，如果沒有匹配到模式則返回原名稱
    """
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, table_name)
        if match:
            # 返回去除日期後綴的前綴
            return table_name[: match.start()]

    # 沒有匹配到日期模式，返回原名稱作為前綴
    return table_name


def get_latest_tables_by_prefix(client: bigquery.Client, dataset_id: str) -> list:
    """
    取得 dataset 中每個 table 前綴最新的 table

    參數：
        client: BigQuery client
        dataset_id: dataset ID

    返回：
        包含 table 資訊的 list，每個前綴只有最新的一個 table
    """
    tables = list(client.list_tables(dataset_id))

    # 按前綴分組
    prefix_tables = defaultdict(list)

    for table_ref in tables:
        table_name = table_ref.table_id
        prefix = extract_table_prefix(table_name)
        prefix_tables[prefix].append(table_name)

    # 對每個前綴，只取最新的 table（按名稱排序，最大的通常是最新的）
    latest_tables = []

    for prefix, table_names in prefix_tables.items():
        # 按 table 名稱排序，取最新的
        table_names.sort(reverse=True)
        latest_table_name = table_names[0]

        # 取得 table 詳細資訊
        table_ref = client.dataset(dataset_id).table(latest_table_name)
        table = client.get_table(table_ref)

        if table.modified:
            latest_tables.append(
                {
                    "prefix": prefix,
                    "table": latest_table_name,
                    "modified": table.modified,
                    "rows": table.num_rows or 0,
                    "total_tables": len(table_names),  # 該前綴下的 table 總數
                }
            )

    return latest_tables


def main():
    # 檢查命令列參數
    if len(sys.argv) < 2:
        print("錯誤: 請提供 project ID")
        print(f"用法: {sys.argv[0]} <project-id>")
        print(f"範例: {sys.argv[0]} my-gcp-project")
        sys.exit(1)

    project_id = sys.argv[1]
    client = bigquery.Client(project=project_id)

    print(f"專案: {project_id}")
    print(f"顯示每個 dataset 各個 table 前綴最新的 table\n")

    datasets = list(client.list_datasets())

    if not datasets:
        print("沒有找到任何 dataset")
        return

    total_datasets = 0
    total_tables_shown = 0

    for dataset_ref in datasets:
        dataset_id = dataset_ref.dataset_id

        try:
            latest_tables = get_latest_tables_by_prefix(client, dataset_id)
        except Exception as e:
            print(f"⚠️  無法讀取 dataset {dataset_id}: {e}\n")
            continue

        # 如果該 dataset 沒有 table，跳過
        if not latest_tables:
            continue

        # 按修改時間排序（最新的在前）
        latest_tables.sort(key=lambda x: x["modified"], reverse=True)

        # 顯示該 dataset 的結果
        print(f"📁 Dataset: {dataset_id}")
        print("-" * 120)
        print(
            f"  {'前綴':<28} {'最新 Table':<38} {'最後修改時間':<15} {'資料筆數':>8} {'前綴下表數':>7}"
        )
        print(f"  {'-'*30} {'-'*40} {'-'*25} {'-'*10} {'-'*10}")

        for t in latest_tables:
            modified_str = t["modified"].strftime("%Y-%m-%d %H:%M:%S")
            rows_str = f"{t['rows']:,}"
            prefix_display = (
                t["prefix"] if t["prefix"] != t["table"] else "single table"
            )
            print(
                f"  {prefix_display:<30} {t['table']:<40} {modified_str:<25} {rows_str:>10} {t['total_tables']:>10}"
            )

        print()
        total_datasets += 1
        total_tables_shown += len(latest_tables)

    print("=" * 120)
    print(
        f"總共: {total_datasets} 個 datasets, 顯示 {total_tables_shown} 個最新的 tables（按前綴分組）"
    )


if __name__ == "__main__":
    main()
