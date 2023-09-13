from Widgets.Tree.common import *

from Widgets.Tree.TreeHeader import TreeHeader
from Widgets.Tree.TreeBody import TreeBody
from Widgets.Tree.TreeColumnConfig import TreeColumnConfig
from Widgets.Tree.TreeEntry import TreeEntry


class TreeWidget(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 350,
                 height: int = 500,
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.header: Union[TreeHeader, None] = None
        self.body: Union[TreeBody, None] = None

        self.col_configs: List[TreeColumnConfig] = list()
        self.entries: List[TreeEntry] = list()

        # self.configure(fg_color=("gray78", "gray28"))

        # Layout:
        #  _________________________
        # | ^v Label   ^v Label ... |
        # |-------------------------|
        # | +- Item       Value ... |
        # |   +- Item     Value ... |
        # |_________________________|
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=32)
        self.grid_rowconfigure(1, weight=1)

    def config_tree(self, config: List[TreeColumnConfig]) -> None:
        """
        Initialize new tree header and body with provided parameters.
        :param config: Tree column configuration.
        """

        self.header = TreeHeader(master=self, cols_config=config,
                                 sort_cb=lambda col_idx, btn_state: self.on_sort_btn_clicked(col_idx, btn_state))
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.body = TreeBody(master=self, col_configs=config)
        self.body.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def add_column(self, col_name: str, col_size: int, col_weight: int) -> None:
        config: TreeColumnConfig = TreeColumnConfig(col_name, col_size, col_weight)
        self.col_configs.append(config)

    def add_entry(self, name: str, indent: int, data: List[Any], parent_name: str,
                  default_expand: bool = False, default_select: bool = False) -> None:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        self.body.add_entry(name, indent, data, parent_name, default_expand, default_select)

    def update_entry(self, name: str, data: List[Any]) -> None:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        self.body.update_entry(name, data)

    def contains_entry(self, name: str) -> bool:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        return self.body.contains_entry(name)

    def render_tree(self) -> None:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        self.body.draw_tree()

    def clear_tree(self) -> None:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        self.body.delete_entries()

    def on_sort_btn_clicked(self, col_idx: int, btn_state: int) -> None:
        if not (self.header and self.body):
            raise RuntimeError("Tree body not initialized")

        reverse: bool
        if btn_state == 0:
            reverse = False
        else:
            reverse = True

        self.body.sort_by(col_idx, reverse)

        # Clear other column button states to prevent multi-sort issues.
        self.header.reset_btn_states(col_idx)

        self.render_tree()
