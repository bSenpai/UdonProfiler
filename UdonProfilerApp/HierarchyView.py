from typing import Any, Dict, List, Union

import customtkinter as ctk

from Widgets.Tree.TreeWidget import TreeWidget, TreeColumnConfig
from Sample import Sample
from FrameInfo import FrameInfo


class HierarchyView(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tree: TreeWidget = TreeWidget(self)
        self.tree.grid(row=0, column=0, sticky="nsew")

        overview_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Overview",
            minsize=150,
            weight=1
        )

        total_time_percent_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Total",
            minsize=100,
            weight=0
        )

        self_time_percent_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Self",
            minsize=100,
            weight=0
        )

        num_calls_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Calls",
            minsize=100,
            weight=0
        )

        total_time_ms_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Time ms",
            minsize=100,
            weight=0
        )

        self_time_ms_col_config: TreeColumnConfig = TreeColumnConfig(
            name="Self ms",
            minsize=100,
            weight=0
        )

        cols_config: List[TreeColumnConfig] = list()
        cols_config.append(overview_col_config)
        cols_config.append(total_time_percent_col_config)
        cols_config.append(self_time_percent_col_config)
        cols_config.append(num_calls_col_config)
        cols_config.append(total_time_ms_col_config)
        cols_config.append(self_time_ms_col_config)

        self.tree.config_tree(cols_config)

        self.samples_expand_state: Dict[str, bool] = dict()
        self.sel_sample_name: Union[str, None] = None

        root: Any = self.winfo_toplevel()
        info: Union[FrameInfo, None] = root.get_selected_frame_info()
        if not info:
            info = FrameInfo(0)
            info.add_sample(Sample("/UdonBehaviour;;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func1;/UdonBehaviour;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func1/Func1A;/UdonBehaviour/Func1;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func1/Func1B;/UdonBehaviour/Func1;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func2;/UdonBehaviour;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func2/Func2A;/UdonBehaviour/Func2;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
            info.add_sample(Sample("/UdonBehaviour/Func3;/UdonBehaviour;100.00;0.00;1;5.00;0.00;0.00,1.00;1.00,2.00"))
        for i in range(0, len(info.samples)):
            self.add_item(info.samples[i])

        self.tree.render_tree()

    def add_item(self, item: Sample, selected: bool = False) -> None:
        if item.path_name not in self.samples_expand_state:
            self.samples_expand_state[item.path_name] = False

        self.tree.add_entry(
            item.path_name,
            item.depth,
            [
                item.name,
                item.total_time_percent,
                item.self_time_percent,
                item.num_calls,
                item.total_time_ms,
                item.self_time_ms
            ],
            item.parent_path_name,
            default_expand=self.samples_expand_state[item.path_name],
            default_select=selected
        )

    def on_frame_info_received(self, frame_info: FrameInfo) -> None:
        # Save previous frame expand states.
        if not self.tree.body:
            raise RuntimeError("Tree body reference lost")

        for k in self.tree.body.entry_expand_states.keys():
            # This can happen if application cleared frame infos.
            if k.entry_config.name not in self.samples_expand_state:
                self.samples_expand_state[k.entry_config.name] = False

            self.samples_expand_state[k.entry_config.name] = self.tree.body.entry_expand_states[k]

        # Save previous frame selected entry.
        sel_entry_name: Union[str, None] = None
        if self.tree.body.sel_entry:
            sel_entry_name = self.tree.body.sel_entry.entry_config.name

        self.tree.clear_tree()
        self.tree.body.sel_entry = None

        # Add new entries to tree.
        for i in range(0, len(frame_info.samples)):
            selected: bool = False
            if sel_entry_name and frame_info.samples[i].path_name == sel_entry_name:
                selected = True

            self.add_item(frame_info.samples[i], selected)

        self.tree.render_tree()

    def on_frame_info_cleared(self) -> None:
        self.samples_expand_state.clear()
        self.sel_sample_name = None
        self.tree.clear_tree()
        self.tree.render_tree()
