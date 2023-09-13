from __future__ import annotations

from Widgets.Tree.common import *

from Widgets.Tree.TreeNode import TreeNode

if TYPE_CHECKING:
    from Widgets.Tree.TreeEntry import TreeEntry


@dataclass
class TreeDataStructure:
    root_node: TreeNode

    def __init__(self) -> None:
        self.root_node = TreeNode()

    def search(self, data: TreeEntry) -> Union[TreeNode, None]:
        for node in self.root_node:
            if node.entry == data:
                return node

        return None

    def sort(self, key: int, reverse: bool = False) -> None:
        # Sorting children of each node preserves tree structure.
        for node in self.root_node:
            node.sort_children(key, reverse)
