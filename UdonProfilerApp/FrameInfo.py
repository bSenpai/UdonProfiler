from dataclasses import dataclass
from typing import List

from Sample import Sample


@dataclass
class FrameInfo:
    frame_number: int
    frame_time: float
    samples: List[Sample]
    max_depth: int

    def __init__(self, frame_number: int) -> None:
        self.frame_number = frame_number
        self.frame_time = -1
        self.samples = list()
        self.max_depth = 0

    def add_sample(self, sample: Sample) -> None:
        if self.frame_time < 0 and sample.path_name == "/UdonBehaviour":
            self.frame_time = sample.total_time_ms

        self.samples.append(sample)

        self.max_depth = max(self.max_depth, sample.depth)
