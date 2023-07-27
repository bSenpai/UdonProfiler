from __future__ import annotations

from Widgets.Tree.common import *

from Widgets.Tree.TreeEntry import TreeEntry
from Widgets.Tree.TreeEntryConfig import TreeEntryConfig
from Widgets.Tree.TreeNode import TreeNode
from Widgets.Tree.TreeDataStructure import TreeDataStructure

if TYPE_CHECKING:
    from Widgets.Tree.TreeColumnConfig import TreeColumnConfig


class TreeBody(ctk.CTkScrollableFrame):
    root_name: str = ""

    def __init__(self, *args,
                 width: int = 100,
                 height: int = 300,
                 col_configs: List[TreeColumnConfig],
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.col_configs: List[TreeColumnConfig] = col_configs

        self.configure(fg_color=("gray78", "gray28"))
        self.grid_columnconfigure(0, weight=1)

        self.tree: TreeDataStructure = TreeDataStructure()
        self.sel_entry: Union[TreeEntry, None] = None
        self.entry_grid_infos: Dict[TreeEntry, Dict[str, Any]] = dict()
        self.entry_expand_states: Dict[TreeEntry, bool] = dict()

    def add_entry(self, name: str, indent: int, data: List[Any], parent_name: str,
                  default_expand: bool = False, default_select: bool = False) -> None:
        # Create tree node.
        entry_config: TreeEntryConfig = TreeEntryConfig(name, indent, data,
                                                        self.on_entry_clicked, self.on_entry_expanded)
        entry: TreeEntry = TreeEntry(master=self, entry_config=entry_config,
                                     col_minsizes=[x.minsize for x in self.col_configs],
                                     col_weights=[x.weight for x in self.col_configs])
        child_node: TreeNode = TreeNode(entry)

        # Start with node collapsed/expanded.
        self.store_entry_expand_state(entry, default_expand)

        # Set select state.
        if default_select:
            self.sel_entry = entry

        # Insert node into tree.
        if parent_name == TreeBody.root_name:
            self.tree.root_node.add_child(child_node)
        else:
            parent_node: Union[TreeNode, None] = None
            for node in self.tree.root_node:
                if not node.entry:
                    continue
                if node.entry.entry_config.name == parent_name:
                    parent_node = node
                    break

            if parent_node:
                parent_node.add_child(child_node)
            else:
                raise RuntimeError(f"Tree entry parent named: {parent_name} does not exist")

    def update_entry(self, name: str, data: List[Any]) -> None:
        for node in self.tree.root_node:
            if not node.entry:
                continue

            if node.entry.entry_config.name == name:
                node.entry.update_entry(data)
                break

    def contains_entry(self, name: str) -> bool:
        for node in self.tree.root_node:
            if not node.entry:
                continue

            if node.entry.entry_config.name == name:
                return True

        return False

    def draw_tree(self) -> None:
        # Flatten tree indices.
        cur_idx: int = 0
        for node in self.tree.root_node:
            if not node.entry:
                continue

            if len(node.children) == 0:
                node.entry.disable_expand()

            node.entry.grid(row=cur_idx, column=0, sticky="ew")
            self.store_entry_grid_info(node.entry)
            cur_idx += 1

        # Needs to be in a separate loop.
        for node in self.tree.root_node:
            if not node.entry:
                continue

            self.restore_entry_expand_state(node.entry)

            # Sets correct button symbol if expanded.
            if self.entry_expand_states[node.entry] and not node.entry.expanded:
                node.entry.on_expanded()

        if self.sel_entry:
            self.sel_entry.select()

    def delete_entries(self) -> None:
        for node in self.tree.root_node:
            if not node.entry:
                continue

            node.entry.grid_forget()
            node.entry.destroy()

        self.sel_entry = None
        self.tree.root_node = TreeNode()

    def sort_by(self, key: int, reverse: bool = False) -> None:
        self.tree.sort(key, reverse)

    def on_entry_clicked(self, entry: TreeEntry, clicked: bool) -> None:
        # Force highlighting of selected node only.
        # TODO: Call a user-defined callback here.
        if clicked:
            self.sel_entry = entry
        else:
            self.sel_entry = None

        for node in self.tree.root_node:
            if not node.entry:
                continue

            if node.entry != entry:
                node.entry.deselect()

    def on_entry_expanded(self, entry: TreeEntry, expanded: bool) -> None:
        node: Union[TreeNode, None] = self.tree.search(entry)
        if not node:
            raise ValueError("Expanded tree entry does not have a node assigned", repr(entry))

        self.store_entry_expand_state(entry, expanded)
        if expanded:
            # Restore expanded state for all immediate children and their descendants.
            self.restore_descendants(node)
        else:
            # Hide all immediate children and their descendants.
            # Store expanded state for when we expand this node.
            self.hide_descendants(node)

    def restore_descendants(self, node: TreeNode) -> None:
        if not node.entry:
            return

        # If current node is not expanded, we won't need to show its children.
        if not self.entry_expand_states[node.entry]:
            return

        # Show children of current node.
        for child in node.children:
            if child.entry:
                self.show_entry(child.entry)
            self.restore_descendants(child)

    def hide_descendants(self, node: TreeNode) -> None:
        for child in node.children:
            if not child.entry:
                continue
            self.hide_entry(child.entry)
            self.hide_descendants(child)

    def hide_entry(self, entry: TreeEntry) -> None:
        entry.grid_forget()

    def show_entry(self, entry: TreeEntry) -> None:
        self.restore_entry_grid_info(entry)

    def store_entry_grid_info(self, entry: TreeEntry) -> None:
        # See: https://stackoverflow.com/a/37732268
        info: Dict[str, Any] = entry.grid_info()
        self.entry_grid_infos[entry] = info

    def restore_entry_grid_info(self, entry: TreeEntry) -> None:
        if entry not in self.entry_grid_infos:
            raise RuntimeError("Tree entry's grid information not stored", repr(entry))

        info: Dict[str, Any] = self.entry_grid_infos[entry]
        entry.grid(**info)

    def store_entry_expand_state(self, entry: TreeEntry, expanded: bool) -> None:
        self.entry_expand_states[entry] = expanded

    def restore_entry_expand_state(self, entry: TreeEntry) -> None:
        if entry not in self.entry_expand_states:
            raise RuntimeError("Tree entry's grid information not stored", repr(entry))

        node: Union[TreeNode, None] = self.tree.search(entry)
        if not node:
            raise ValueError("Tree entry does not have a node assigned", repr(entry))

        for child in node.children:
            if not child.entry:
                continue
            if self.entry_expand_states[entry]:
                self.show_entry(child.entry)
            else:
                self.hide_entry(child.entry)
