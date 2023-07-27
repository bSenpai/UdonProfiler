from Widgets.Tree.common import *

from Widgets.Tree.TreeWidget import TreeWidget
from Widgets.Tree.TreeColumnConfig import TreeColumnConfig


class TreeWidgetTest(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("TreeWidget Test")
        self.geometry("750x400")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree_widget: TreeWidget = TreeWidget(self)
        self.tree_widget.grid(row=0, column=0, sticky="nsew")

        name_col_config: TreeColumnConfig = TreeColumnConfig("Overview", 150, 1)
        total_col_config: TreeColumnConfig = TreeColumnConfig("Total", 50, 0)
        self_col_config: TreeColumnConfig = TreeColumnConfig("Self", 50, 0)
        calls_col_config: TreeColumnConfig = TreeColumnConfig("Calls", 50, 0)
        time_col_config: TreeColumnConfig = TreeColumnConfig("Time (ms)", 50, 0)
        selfms_col_config: TreeColumnConfig = TreeColumnConfig("Self (ms)", 50, 0)

        self.tree_widget.config_tree([name_col_config, total_col_config, self_col_config, calls_col_config,
                                      time_col_config, selfms_col_config])

        self.tree_widget.add_entry("rootA",
                                   0,
                                   ["rootA", "95%", "20%", 1, 5.00, 2.00],
                                   "")
        self.tree_widget.add_entry("rootA/FuncA",
                                   1,
                                   ["FuncA", "90%", "10%", 10, 4.00, 1.00],
                                   "rootA")
        self.tree_widget.add_entry("rootA/FuncA1",
                                   2,
                                   ["FuncA1WithReallyLongNameThatTakesUpALotOfSpaceLikeWhyIsItStillGoingWhatIsHappening"
                                    "Here", "50%", "2%", 7, 3.00, 1.50],
                                   "rootA/FuncA")
        self.tree_widget.add_entry("rootA/FuncA2",
                                   2,
                                   ["FuncA2", "45%", "10%", 20, 1.00, 2.25],
                                   "rootA/FuncA")
        self.tree_widget.add_entry("rootA/FuncB",
                                   1,
                                   ["FuncB", "10%", "50%", 4, 1.00, 3.00],
                                   "rootA")
        self.tree_widget.add_entry("rootB",
                                   0,
                                   ["rootB", "5%", "0.2%", 1, 3.00, 1.00],
                                   "")
        self.tree_widget.add_entry("rootB/FuncC",
                                   1,
                                   ["FuncC", "100%", "15%", 25, 3.00, 0.50],
                                   "rootB")

        self.tree_widget.render_tree()

        """
        self.tree_widget.clear_tree()

        self.tree_widget.add_entry("rootA",
                                   0,
                                   ["rootA", "95%", "20%", 1, 5.00, 2.00],
                                   "")
        self.tree_widget.add_entry("rootA/FuncA",
                                   1,
                                   ["FuncA", "90%", "10%", 10, 4.00, 1.00],
                                   "rootA")

        self.tree_widget.render_tree()
        """


if __name__ == "__main__":
    app: TreeWidgetTest = TreeWidgetTest()
    app.mainloop()
