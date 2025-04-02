import redis
import argparse
from collections import defaultdict
from operator import itemgetter
import sys
from datetime import datetime


class RedisAnalyzer:
    redis_client: redis.Redis
    output_file: str

    def __init__(
        self, host="localhost", port=6379, db=0, output_file: str = "redis_analysis.txt"
    ):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )
        self.output_file = output_file

    def write_to_file(self, content: str) -> None:
        """將內容寫入檔案"""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"{content}\n")

    def analyze_keys(self, pattern: str = "*", delimiters: list = [":"]) -> None:
        """分析並顯示keys的記憶體使用情況"""
        keys_info = []
        prefix_stats = defaultdict(
            lambda: {
                "count": 0,
                "total_bytes": 0,
                "min_bytes": float("inf"),
                "max_bytes": 0,
                "keys_with_ttl": 0,
            }
        )

        # 寫入分析開始時間
        start_time = datetime.now()
        header = f"\n=== Analysis started at {start_time} ===\n"
        self.write_to_file(content=header)
        print(header)

        # 先計算總key數
        total_keys = self.redis_client.dbsize()
        processed_keys = 0

        # 蒐集資料
        for key in self.redis_client.scan_iter(pattern):
            processed_keys += 1

            # 每處理100個keys就顯示進度
            if processed_keys % 100 == 0:
                progress = f"Processed {processed_keys}/{total_keys} keys ({(processed_keys/total_keys*100):.2f}%)"
                # 一般 print() 預設是 end="\n"，也就是會換行
                # "\r" 是特殊字元,表示讓游標回到該行最開頭
                # 使用 "\r" 會讓下一次輸出從同一行開始,覆蓋掉原本的內容
                print(progress, end="\r")
                sys.stdout.flush()

            memory_usage = self.redis_client.memory_usage(key)
            ttl = self.redis_client.ttl(key)
            prefix = key
            for delimiter in delimiters:
                if delimiter in key:
                    prefix = key.split(delimiter)[0] + delimiter
                    break

            keys_info.append(
                {
                    "key": key,
                    "memory_bytes": memory_usage,
                    "ttl": ttl if ttl > 0 else None,
                }
            )

            # 更新prefix統計
            stats = prefix_stats[prefix]
            stats["count"] += 1
            stats["total_bytes"] += memory_usage
            stats["min_bytes"] = min(stats["min_bytes"], memory_usage)
            stats["max_bytes"] = max(stats["max_bytes"], memory_usage)
            if ttl > 0:
                stats["keys_with_ttl"] += 1

        print("\n")  # 新行，避免進度條影響後續輸出

        # 寫入排序後的keys資訊
        self.write_to_file("\n=== Keys sorted by memory usage ===")
        sorted_keys = sorted(keys_info, key=itemgetter("memory_bytes"), reverse=True)
        for key_info in sorted_keys:
            content = (
                f"Key: {key_info['key']}\n"
                f"Memory: {format_bytes(key_info['memory_bytes'])}\n"
                f"TTL: {key_info['ttl']}\n"
                "---"
            )
            self.write_to_file(content)

            # 寫入prefix統計
        self.write_to_file("\n=== Statistics by prefix ===")
        for prefix, stats in prefix_stats.items():
            avg_bytes = stats["total_bytes"] / stats["count"]
            content = (
                f"\nPrefix: {prefix}\n"
                f"Count: {stats['count']}\n"
                f"Total bytes: {format_bytes(stats['total_bytes'])}\n"
                f"Avg bytes: {format_bytes(avg_bytes)}\n"
                f"Min bytes: {format_bytes(stats['min_bytes'])}\n"
                f"Max bytes: {format_bytes(stats['max_bytes'])}\n"
            )
            self.write_to_file(content)

        # 寫入分析結束時間和總結
        end_time = datetime.now()
        duration = end_time - start_time
        summary = (
            f"\n=== Analysis Summary ===\n"
            f"Total keys processed: {processed_keys}\n"
            f"Analysis duration: {duration}\n"
            f"Output file: {self.output_file}\n"
            f"Analysis completed at: {end_time}\n"
        )
        self.write_to_file(summary)
        print(summary)


def format_bytes(bytes_num: float) -> str:
    """將bytes轉換為人類可讀格式"""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_num < 1024:
            return f"{bytes_num:.2f}{unit}"
        bytes_num /= 1024  # type: ignore
    return f"{bytes_num:.2f}TB"


def parse_args():
    parser = argparse.ArgumentParser(description="Redis Keys Memory Analysis Tool")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--db", type=int, default=0, help="Redis database number")
    parser.add_argument("--pattern", type=str, default="*", help="Scan pattern")
    parser.add_argument(
        "--delimiters", nargs="+", type=str, default=[":"], help="Key delimiters"
    )
    parser.add_argument(
        "--output", type=str, default="redis_analysis.txt", help="Output file path"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    analyzer = RedisAnalyzer(
        host=args.host, port=args.port, db=args.db, output_file=args.output
    )
    analyzer.analyze_keys(pattern=args.pattern, delimiters=args.delimiters)


# rm redis_analysis.txt
# python redis_scan_keys.py --db=0 --pattern="*" --delimiters ":" "#" --output="redis_analysis.txt"
if __name__ == "__main__":
    main()
