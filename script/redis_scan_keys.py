import redis
import argparse
from collections import defaultdict
from operator import itemgetter


class RedisAnalyzer:
    redis_client: redis.Redis

    def __init__(self, host="localhost", port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )

    def analyze_keys(self, pattern: str = "*", delimiter: str = ":") -> None:
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

        # 蒐集資料
        for key in self.redis_client.scan_iter(pattern):
            memory_usage = self.redis_client.memory_usage(key)
            ttl = self.redis_client.ttl(key)
            prefix = key.split(delimiter)[0] if delimiter in key else key

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

        # 顯示排序後的keys
        print("\n=== Keys sorted by memory usage ===")
        sorted_keys = sorted(keys_info, key=itemgetter("memory_bytes"), reverse=True)
        for key_info in sorted_keys:
            print(f"Key: {key_info['key']}")
            print(f"Memory: {format_bytes(key_info['memory_bytes'])}")
            print(f"TTL: {key_info['ttl']}")
            print("---")

        # 顯示prefix統計
        print("\n=== Statistics by prefix ===")
        for prefix, stats in prefix_stats.items():
            avg_bytes = stats["total_bytes"] / stats["count"]
            print(f"\nPrefix: {prefix}")
            print(f"Count: {stats['count']}")
            print(f"Total bytes: {stats['total_bytes']}")
            print(f"Avg bytes: {avg_bytes}")
            print(f"Min bytes: {stats['min_bytes']}")
            print(f"Max bytes: {stats['max_bytes']}")


def format_bytes(bytes_num: int) -> str:
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
    parser.add_argument("--delimiter", type=str, default=":", help="Key delimiter")
    parser.add_argument("--pattern", type=str, default="*", help="Scan pattern")
    return parser.parse_args()


def main():
    args = parse_args()
    analyzer = RedisAnalyzer(host=args.host, port=args.port, db=args.db)
    analyzer.analyze_keys(pattern=args.pattern, delimiter=args.delimiter)


if __name__ == "__main__":
    main()
