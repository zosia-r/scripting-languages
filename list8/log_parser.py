from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    raw: str
    uid: str
    timestamp: float
    method: str
    uri: str
    status_code: int
    origin_host: str
    origin_port: int
    destination_host: str
    destination_port: int
    host_domain: str


def parse_log_line(line: str) -> LogEntry:
    parts = line.strip().split('\t')
    if len(parts) < 15:
        raise ValueError("Too little values in log")
    
    for item in reversed(parts):
        if item.isdigit(): 
            found_status_code = int(item)
            break

    return LogEntry(
        raw=line,
        uid=parts[1],
        timestamp=float(parts[0]),
        method=parts[7],
        uri=parts[9],
        status_code=found_status_code,
        origin_host=parts[2],
        origin_port=int(parts[3]),
        destination_host=parts[4],
        destination_port=int(parts[5]),
        host_domain=parts[8]
    )

def load_log_file(filepath: str):
    with open(filepath, 'r') as f:
        return [parse_log_line(line) for line in f if line.strip()]
