from typing import Dict, List, Union

import customtkinter as ctk

from Widgets.Tree.TreeWidget import TreeWidget, TreeColumnConfig
from Src.FrameInfo import FrameInfo
from Src.SampleStatistics import SampleStatistics


class StatisticsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sample_statistics: Dict[str, SampleStatistics] = dict()

        self.tree: TreeWidget = TreeWidget(self)
        self.tree.grid(row=0, column=0, sticky="nsew")

        overview_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Overview",
            minsize=150,
            weight=1
        )

        num_samples_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Sample Count",
            minsize=100,
            weight=0
        )

        min_time_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Min Time (ms)",
            minsize=100,
            weight=0
        )

        max_time_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Max Time (ms)",
            minsize=100,
            weight=0
        )

        avg_time_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Avg Time (ms)",
            minsize=100,
            weight=0
        )

        cols_config: List[TreeColumnConfig] = list()
        cols_config.append(overview_col_config)
        cols_config.append(num_samples_col_config)
        cols_config.append(min_time_col_config)
        cols_config.append(max_time_col_config)
        cols_config.append(avg_time_col_config)

        self.tree.config_tree(cols_config)

        self.sel_sample_name: Union[str, None] = None

        """
        root: Any = self.winfo_toplevel()
        info: Union[FrameInfo, None] = root.get_selected_frame_info()
        if not info:
            info = FrameInfo(0)
            info.add_sample(Sample("/UdonBehaviour,,0,0.400"))
            info.add_sample(Sample("/UdonBehaviour/Func1,/UdonBehaviour,1,0.120"))
            info.add_sample(Sample("/UdonBehaviour/Func1A,/UdonBehaviour/Func1,2,0.050"))
            info.add_sample(Sample("/UdonBehaviour/Func1B,/UdonBehaviour/Func1,2,0.040"))
            info.add_sample(Sample("/UdonBehaviour/Func2,/UdonBehaviour,1,0.150"))
            info.add_sample(Sample("/UdonBehaviour/Func2A,/UdonBehaviour/Func2,2,0.050"))
            info.add_sample(Sample("/UdonBehaviour/Func3,/UdonBehaviour,1,0.100"))
            self.update_statistics(info)
        self.add_items()
        """

        self.tree.render_tree()

    def update_statistics(self, frame_info: FrameInfo) -> None:
        for sample in frame_info.samples:
            name: str = sample.path_name.split("/")[-1]

            if name not in self.sample_statistics:
                self.sample_statistics[name] = SampleStatistics(name)

            self.sample_statistics[name].add_statistic(sample.total_time_ms)

    def add_items(self) -> None:
        for name in self.sample_statistics.keys():
            self.add_item(self.sample_statistics[name])

    def add_item(self, item: SampleStatistics, selected: bool = False) -> None:
        # Clearing tree and re-adding entries freezes application.
        if self.tree.contains_entry(item.name):
            self.tree.update_entry(item.name,
                                   [item.name,
                                    f"{item.num_samples}",
                                    f"{item.min_time:.2f}",
                                    f"{item.max_time:.2f}",
                                    f"{item.avg_time:.2f}"])
        else:
            self.tree.add_entry(item.name,
                                0,
                                [item.name,
                                 f"{item.num_samples}",
                                 f"{item.min_time:.2f}",
                                 f"{item.max_time:.2f}",
                                 f"{item.avg_time:.2f}"],
                                "",
                                default_expand=False,
                                default_select=selected)

    def on_frame_info_received(self, frame_info: FrameInfo) -> None:
        # Save previous frame expand states.
        if not self.tree.body:
            raise RuntimeError("Tree body reference lost")

        # Save previous frame selected entry.
        sel_entry_name: Union[str, None] = None
        if self.tree.body.sel_entry:
            sel_entry_name = self.tree.body.sel_entry.entry_config.name

        self.update_statistics(frame_info)

        # Add new entries to tree.
        for name in self.sample_statistics.keys():
            selected: bool = False
            if sel_entry_name and name == sel_entry_name:
                selected = True
            self.add_item(self.sample_statistics[name], selected=selected)

        self.tree.render_tree()

    def on_frame_info_cleared(self) -> None:
        self.sample_statistics.clear()
        self.sel_sample_name = None
        self.tree.clear_tree()
        self.tree.render_tree()
