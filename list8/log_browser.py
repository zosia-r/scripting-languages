from datetime import datetime
from log_parser import LogEntry

class LogBrowser:
    def __init__(self, log_entries: list[LogEntry]):
        self.all_logs = log_entries
        self.filtered_logs = log_entries
        self.current_index = 0

    def filter_by_time(self, start: datetime, end: datetime):
        self.filtered_logs = [
            log for log in self.all_logs
            if start.timestamp() <= log.timestamp <= end.timestamp()
        ]
        self.current_index = 0

    def current_log(self):
        if self.filtered_logs:
            return self.filtered_logs[self.current_index]
        return None

    def next_log(self):
        if self.current_index < len(self.filtered_logs) - 1:
            self.current_index += 1

    def previous_log(self):
        if self.current_index > 0:
            self.current_index -= 1

    def has_next(self):
        return self.current_index < len(self.filtered_logs) - 1

    def has_previous(self):
        return self.current_index > 0
