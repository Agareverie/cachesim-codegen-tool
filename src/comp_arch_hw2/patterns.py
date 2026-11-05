import re

expected_stdout = re.compile(
    r"""
Cache Size\s*=\s*(?P<cache_bytes>\d+)\s*Bytes\s*=\s*(?P<cache_kib>\d+)\s*Kibibytes.*?
Block Size\s*=\s*(?P<block_bytes>\d+).*?
Associativity\s*=\s*(?P<associativity>\d+).*?
Hit\s*=\s*(?P<hits>\d+),\s*Miss\s*=\s*(?P<misses>\d+).*?
Hit Rate\s*=\s*(?P<hit_rate>[0-9.]+)
""",
    re.DOTALL,
)
