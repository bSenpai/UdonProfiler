from __future__ import annotations

from Widgets.Tree.common import *

if TYPE_CHECKING:
    from Widgets.Tree.TreeEntry import TreeEntry


@dataclass
class TreeEntryConfig:
    name: str
    indent: int
    data: List[Any]
    click_cb: Callable[[TreeEntry, bool], None]
    expand_cb: Callable[[TreeEntry, bool], None]

    def __init__(self, name: str, indent: int, data: List[Any],
                 click_cb: Callable[[TreeEntry, bool], None],
                 expand_cb: Callable[[TreeEntry, bool], None]) -> None:
        self.name = name
        self.indent = indent
        self.data = data
        self.click_cb = click_cb
        self.expand_cb = expand_cb
