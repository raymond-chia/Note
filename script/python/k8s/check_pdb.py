#!/usr/bin/env python3
"""
Kubernetes PDB 檢查工具

找出 maxUnavailable = 0 的 PDB 設定，這可能會導致節點維護或升級時無法正常進行。

使用：python check_pdb.py [-n NAMESPACE]
"""

import subprocess
import json
import sys
import argparse
from typing import List, Dict, Any, Optional
from tabulate import tabulate


# 常數定義
KUBECTL_COMMAND = "kubectl"
RESOURCE_TYPE = "poddisruptionbudgets"
OUTPUT_FORMAT = "json"
MAX_UNAVAILABLE_WARNING = 0
TABLE_HEADERS = [
    "Namespace",
    "PDB 名稱",
    "Max Unavailable",
    "Min Available",
    "Selector",
]
TABULATE_FORMAT = "grid"
NOT_AVAILABLE = "N/A"
DEFAULT_NAMESPACE = "default"
UNKNOWN_NAME = "unknown"


def get_pdbs(namespace: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    取得所有 PDB 資源

    參數：
        namespace: 指定 namespace，若為 None 則查詢所有 namespace

    返回：
        List[Dict]: PDB 資源列表
    """
    args = ["get", RESOURCE_TYPE, "-o", OUTPUT_FORMAT]
    args += ["-n", namespace] if namespace else ["--all-namespaces"]

    try:
        result = subprocess.run(
            [KUBECTL_COMMAND] + args, capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout).get("items", [])
    except FileNotFoundError:
        print("錯誤：找不到 kubectl 命令", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"錯誤：{e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)


def analyze_pdb(pdb: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    檢查 PDB 是否 maxUnavailable = 0

    參數：
        pdb: PDB 資源物件

    返回：
        Optional[Dict]: 如果 maxUnavailable = 0，返回分析結果，否則返回 None
    """
    metadata = pdb.get("metadata", {})
    spec = pdb.get("spec", {})

    max_unavailable = spec.get("maxUnavailable")

    # 檢查是否為 0（支援 int 或 str 類型）
    if max_unavailable == MAX_UNAVAILABLE_WARNING:
        # 格式化 selector
        selector = spec.get("selector", {}).get("matchLabels", {})
        selector_str = (
            ", ".join(f"{k}={v}" for k, v in selector.items())
            if selector
            else NOT_AVAILABLE
        )

        return {
            "namespace": metadata.get("namespace", DEFAULT_NAMESPACE),
            "name": metadata.get("name", UNKNOWN_NAME),
            "max_unavailable": max_unavailable,
            "min_available": spec.get("minAvailable", NOT_AVAILABLE),
            "selector": selector_str,
        }

    return None


def main() -> int:
    """
    主程式入口

    返回：
        int: 退出碼（0 表示成功，1 表示有問題的 PDB）
    """
    parser = argparse.ArgumentParser(description="檢查 K8s PDB 設定")
    parser.add_argument("-n", "--namespace", help="指定 namespace")
    args = parser.parse_args()

    try:
        pdbs = get_pdbs(namespace=args.namespace)

        if not pdbs:
            print("沒有找到任何 PDB 資源")
            return 0

        # 找出有問題的 PDB（使用 walrus operator）
        problematic = [result for pdb in pdbs if (result := analyze_pdb(pdb))]

        if not problematic:
            print("✅ 沒有發現 maxUnavailable = 0 的 PDB 設定")
            return 0

        # 輸出結果
        print(f"⚠️  發現 {len(problematic)} 個 PDB 的 maxUnavailable = 0\n")
        print("這可能會導致節點維護或升級時無法正常進行！\n")

        table_data = [
            [
                p["namespace"],
                p["name"],
                p["max_unavailable"],
                p["min_available"],
                p["selector"],
            ]
            for p in problematic
        ]
        print(tabulate(table_data, headers=TABLE_HEADERS, tablefmt=TABULATE_FORMAT))

        return 1

    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
