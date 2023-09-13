from __future__ import annotations

from Widgets.Tree.common import *

if TYPE_CHECKING:
    from Widgets.Tree.TreeEntryConfig import TreeEntryConfig


class TreeEntry(ctk.CTkFrame):
    default_color: str = "transparent"
    selected_color: str = "#4682B4"
    collapsed_sym: str = "\u2bc8"
    expanded_sym: str = "\u2bc6"

    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 entry_config: TreeEntryConfig,
                 col_minsizes: List[int],
                 col_weights: List[int],
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.entry_config: TreeEntryConfig = entry_config
        self.col_minsizes: List[int] = col_minsizes
        self.col_weights: List[int] = col_weights

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure(0, weight=0, minsize=25)
        self.grid_rowconfigure(0, weight=1, minsize=32)

        self.expand_btn: ctk.CTkButton = ctk.CTkButton(self, text=TreeEntry.collapsed_sym,
                                                       command=lambda: self.on_expanded(),
                                                       width=20, height=20, corner_radius=0,
                                                       fg_color="transparent",
                                                       hover=False)
        self.expand_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.labels: List[ctk.CTkLabel] = list()
        for i in range(0, len(self.entry_config.data)):
            self.grid_columnconfigure(i + 1, weight=self.col_weights[i], minsize=self.col_minsizes[i])

            lbl: ctk.CTkLabel
            if i == 0:
                # Indent first column to signify tree structure.
                lbl = ctk.CTkLabel(self, text=" " * self.entry_config.indent * 5 +
                                              (self.entry_config.data[i]), anchor="w", corner_radius=0)
            else:
                lbl = ctk.CTkLabel(self, text=str(self.entry_config.data[i]), anchor="center", corner_radius=0)
            # Force column contents to fit.
            # lbl.grid(row=0, column=i+1, padx=(5, max(10, self.col_minsizes[i] -
            #                                          len(str(self.entry_config.data)) * 4 - 5)), sticky="ew")
            lbl.grid(row=0, column=i+1, padx=(5, 5), sticky="ew")
            lbl.bind("<Button>", lambda event: self.on_clicked())
            self.labels.append(lbl)

            # See: https://stackoverflow.com/a/60086946
            # self.winfo_toplevel().update()
            # print(lbl.winfo_width(), lbl.winfo_reqwidth())

        self.selected = False
        self.expanded = False

    def on_clicked(self) -> None:
        if not self.selected:
            self.select()
        else:
            self.deselect()

        self.entry_config.click_cb(self, self.selected)

    def on_expanded(self) -> None:
        self.expanded = not self.expanded

        if self.expanded:
            self.expand_btn.configure(text=TreeEntry.expanded_sym)
        else:
            self.expand_btn.configure(text=TreeEntry.collapsed_sym)

        self.entry_config.expand_cb(self, self.expanded)

    def select(self) -> None:
        self.selected = True
        self.configure(fg_color=TreeEntry.selected_color)

    def deselect(self) -> None:
        self.selected = False
        self.configure(fg_color=TreeEntry.default_color)

    def disable_expand(self) -> None:
        self.expand_btn.configure(fg_color=TreeEntry.default_color)
        self.expand_btn.configure(state="disabled")
        self.expand_btn.configure(text="")

    def update_entry(self, data: List[Any]) -> None:
        self.entry_config.data = data

        for i in range(0, len(self.labels)):
            lbl: ctk.CTkLabel = self.labels[i]
            if i == 0:
                # Indent first column to signify tree structure.
                lbl.configure(text=" " * self.entry_config.indent * 5 + (self.entry_config.data[i]))
            else:
                lbl.configure(text=self.entry_config.data[i])
