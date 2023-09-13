from Widgets.Tree.common import *


@dataclass
class TreeColumnConfig:
    name: str
    minsize: int
    weight: int

    def __init__(self, name: str, minsize: int, weight: int) -> None:
        self.name = name
        self.minsize = minsize
        self.weight = weight
