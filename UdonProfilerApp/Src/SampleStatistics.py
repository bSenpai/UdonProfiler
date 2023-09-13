from dataclasses import dataclass


@dataclass
class SampleStatistics:
    name: str
    min_time: float
    max_time: float
    avg_time: float
    total_time: float
    num_samples: int

    def __init__(self, name: str) -> None:
        self.name = name
        self.min_time = float("inf")
        self.max_time = float("-inf")
        self.avg_time = float("inf")
        self.total_time = 0
        self.num_samples = 0

    def add_statistic(self, time: float) -> None:
        self.min_time = min(time, self.min_time)
        self.max_time = max(time, self.max_time)
        self.total_time += time
        self.num_samples += 1
        self.avg_time = self.total_time / self.num_samples
