from __future__ import annotations

from Widgets.Tree.common import *

from Widgets.Tree.TreeHeaderColumn import TreeHeaderColumn

if TYPE_CHECKING:
    from Widgets.Tree.TreeColumnConfig import TreeColumnConfig


class TreeHeader(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 cols_config: List[TreeColumnConfig],
                 sort_cb: Callable[[int, int], None],
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.cols_config: List[TreeColumnConfig] = cols_config
        self.sort_cb: Callable[[int, int], None] = sort_cb

        self.configure(fg_color=("gray78", "gray28"))
        self.grid_rowconfigure(0, weight=1)

        self.placeholder_btn: ctk.CTkButton = ctk.CTkButton(self, text="",
                                                            width=0, corner_radius=0,
                                                            fg_color="transparent",
                                                            hover=False,
                                                            state="disabled")
        self.placeholder_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.cols: List[TreeHeaderColumn] = list()
        for i in range(0, len(self.cols_config)):
            self.grid_columnconfigure(i+1, weight=self.cols_config[i].weight, minsize=self.cols_config[i].minsize)

            col: TreeHeaderColumn = TreeHeaderColumn(
                self,
                name=self.cols_config[i].name,
                # Force scope of i variable to lambda expression.
                # Ignore mypy error.
                # See: https://stackoverflow.com/a/938493
                sort_cb=lambda btn_state, col_idx=i: self.on_col_btn_clicked(col_idx, btn_state))

            col.grid(row=0, column=i+1, padx=(5, 5), sticky="ew")

            # See: https://stackoverflow.com/a/60086946
            # self.winfo_toplevel().update()
            # print(col.winfo_width(), col.winfo_reqwidth())

            self.cols.append(col)

    def on_col_btn_clicked(self, col_idx: int, btn_state: int) -> None:
        self.sort_cb(col_idx, btn_state)

    def reset_btn_states(self, ignore_idx: int) -> None:
        """
        Resets column states to prevent multi-sort issues.
        :param ignore_idx: Column to preserve state of.
        """

        for i in range(0, len(self.cols)):
            if i == ignore_idx:
                continue
            self.cols[i].reset_btn_state()
