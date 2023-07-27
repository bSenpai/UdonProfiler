from __future__ import annotations

from Widgets.Tree.common import *

if TYPE_CHECKING:
    from Widgets.Tree.TreeEntry import TreeEntry


@dataclass
class TreeNode:
    entry: Union[TreeEntry, None]
    parent: Union[TreeNode, None]
    children: List[TreeNode]

    def __init__(self, data: Union[TreeEntry, None] = None) -> None:
        self.entry = data
        self.parent = None
        self.children = list()

    def __iter__(self) -> Iterator[TreeNode]:
        # Pre-order traversal.
        # Tree view requires this traversal technique to index entries correctly.
        # See: https://stackoverflow.com/a/47733929
        yield self

        for child in self.children:
            yield from child.__iter__()

    def add_child(self, child: TreeNode) -> None:
        self.children.append(child)

    def sort_children(self, key: int, reverse: bool = False) -> None:
        if len(self.children) < 2:
            return

        if key < 0:
            raise KeyError("Sort index out of range", repr(key), repr(len(self.children)))

        for child in self.children:
            if not child.entry:
                continue
            if key >= len(child.entry.entry_config.data):
                raise KeyError("Sort index out of range", repr(key), repr(len(self.children)))

        # Ignore the mypy warning - c.data is guaranteed to be not None from previous check.
        self.children.sort(key=lambda c: c.entry.entry_config.data[key], reverse=reverse)
