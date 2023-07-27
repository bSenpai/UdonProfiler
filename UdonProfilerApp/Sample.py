from dataclasses import dataclass
from typing import List


@dataclass
class Sample:
    name: str
    path_name: str
    parent_path_name: str
    depth: int
    total_time_percent: float
    self_time_percent: float
    num_calls: int
    total_time_ms: float
    self_time_ms: float
    start_times: List[float]
    end_times: List[float]

    def __init__(self, raw_line: str) -> None:
        path_name_idx: int = 0
        parent_path_name_idx: int = 1
        total_time_percent_idx: int = 2
        self_time_percent_idx: int = 3
        num_calls_idx: int = 4
        total_time_ms_idx: int = 5
        self_time_ms_idx: int = 6
        start_times_idx: int = 7
        end_times_idx: int = 8

        arg_delimiter: str = ";"
        time_delimiter: str = ","
        path_delimiter: str = "/"

        args: List[str] = raw_line.split(arg_delimiter)

        self.path_name = args[path_name_idx]
        self.name = self.path_name.split(path_delimiter)[-1]
        self.parent_path_name = args[parent_path_name_idx]
        self.depth = self.path_name.count(path_delimiter) - 1
        self.total_time_percent = float(args[total_time_percent_idx])
        self.self_time_percent = float(args[self_time_percent_idx])
        self.num_calls = int(args[num_calls_idx])
        self.total_time_ms = float(args[total_time_ms_idx])
        self.self_time_ms = float(args[self_time_ms_idx])

        # See: https://stackoverflow.com/a/1614247
        start_times_raw: List[str] = args[start_times_idx].split(time_delimiter)
        self.start_times = [float(t) for t in start_times_raw]

        end_times_raw: List[str] = args[end_times_idx].split(time_delimiter)
        self.end_times = [float(t) for t in end_times_raw]

        print(self)
