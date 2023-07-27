from Widgets.Tree.common import *


class TreeHeaderColumn(ctk.CTkFrame):
    up_down_arrow: str = "\u21C5"
    # Space at end to center.
    up_arrow: str = "\u2191 "
    down_arrow: str = "\u2193 "

    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 name: str = "Name",
                 sort_cb: Callable[[int], None],
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.name: str = name
        self.sort_cb: Callable[[int], None] = sort_cb

        self.configure(fg_color=("gray78", "gray28"))

        # Layout:
        # sort button | column text
        self.grid_columnconfigure(0, weight=0, minsize=15)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1, minsize=32)

        self.btn: ctk.CTkButton = ctk.CTkButton(self, text=TreeHeaderColumn.up_down_arrow, anchor="w",
                                                command=lambda: self.on_btn_clicked(),
                                                fg_color="transparent",
                                                hover=False,
                                                width=20, height=20,
                                                corner_radius=0)
        self.btn.grid(row=0, column=0, padx=(0, 0), sticky="ew")

        self.lbl: ctk.CTkLabel = ctk.CTkLabel(self, text=self.name, anchor="w", fg_color="transparent")
        self.lbl.grid(row=0, column=1, sticky="ew")

        self.btn_state = -1

    def on_btn_clicked(self) -> None:
        self.btn_state = (self.btn_state + 1) % 2

        if self.btn_state == 0:
            self.btn.configure(text=TreeHeaderColumn.up_arrow)
        else:
            self.btn.configure(text=TreeHeaderColumn.down_arrow)

        self.sort_cb(self.btn_state)

    def reset_btn_state(self) -> None:
        self.btn_state = -1
        self.btn.configure(text=TreeHeaderColumn.up_down_arrow)
