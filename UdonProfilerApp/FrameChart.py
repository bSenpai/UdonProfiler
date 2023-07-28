from collections import deque
from typing import Any, Dict, Iterable, List, Tuple

import customtkinter as ctk
import numpy as np

from Widgets.AnimatedLinePlot.AnimatedLinePlotWidget import AnimatedLinePlotWidget
from FrameInfo import FrameInfo


class FrameChart(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        title: str = "Frame Chart"
        self.title = ctk.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, sticky="ew")

        self.sel_frame: int = -1

        # See: https://stackoverflow.com/a/65135081
        self.data: deque = deque([], maxlen=300)
        for i in range(0, 300):
            self.data.append(0)

        self.frame_slice: Tuple[int, int] = (-1, -1)

        self.graph: AnimatedLinePlotWidget = AnimatedLinePlotWidget(
            self,
            height=50,
            animate_cb=self.on_animate,
            mouse_motion_cb=lambda event: self.on_mouse_moved(event),
            mouse_press_cb=lambda event: self.on_mouse_clicked(event),
            animation_interval=25,
            x_range=(0, 300),
            y_range=(0, 70),
            max_points=300
        )
        self.graph.grid(row=1, column=0, sticky="nsew")

        param_dict: Dict[str, Any] = dict()
        # param_dict["linestyle"] = "--"
        self.graph.add_line("frame time", np.arange(0, 300, 1), [0] * 300, param_dict=param_dict)

        self.graph.add_line("1ms line", y_data=1)
        self.graph.add_text("1ms text", (0, 2), "1ms (1000FPS)")

        self.graph.add_line("4ms line", y_data=4)
        self.graph.add_text("4ms text", (0, 5), "4ms (250FPS)")

        self.graph.add_line("5ms line", y_data=5)
        self.graph.add_text("5ms text", (0, 6), "5ms (200FPS)")

        self.graph.add_line("10ms line", y_data=10)
        self.graph.add_text("10ms text", (0, 11), "10ms (100FPS)")

        self.graph.add_line("16ms line", y_data=16)
        self.graph.add_text("16ms text", (0, 17), "16ms (60FPS)")

        self.graph.add_line("22ms line", y_data=22)
        self.graph.add_text("22ms text", (0, 23), "22ms (45FPS)")

        self.graph.add_line("33ms line", y_data=33)
        self.graph.add_text("33ms text", (0, 34), "33ms (30FPS)")

        self.graph.add_line("66ms line", y_data=66)
        self.graph.add_text("66ms text", (0, 67), "66ms (15FPS)")

        self.graph.add_line("selected frame", x_data=self.sel_frame)

    def on_animate(self) -> Iterable[str]:
        self.graph.update_line("frame time", y_data=list(self.data))
        self.graph.update_line("selected frame", x_data=self.sel_frame)
        self.graph.fill_line("frame time", 0, 0.5)
        y_max: float = max(self.data) + 2
        self.graph.update_plot_range(y_range=(0, y_max))

        updated_items: List[str] = list()
        updated_items.append("frame time")
        updated_items.append("selected frame")

        if y_max < 5:
            updated_items.append("1ms line")
            updated_items.append("1ms text")
        elif y_max < 10:
            updated_items.append("5ms line")
            updated_items.append("5ms text")
        elif y_max < 16:
            updated_items.append("5ms line")
            updated_items.append("5ms text")
            updated_items.append("10ms line")
            updated_items.append("10ms text")
        elif y_max < 22:
            updated_items.append("5ms line")
            updated_items.append("5ms text")
            updated_items.append("10ms line")
            updated_items.append("10ms text")
            updated_items.append("16ms line")
            updated_items.append("16ms text")
        elif y_max < 33:
            updated_items.append("10ms line")
            updated_items.append("10ms text")
            updated_items.append("16ms line")
            updated_items.append("16ms text")
            updated_items.append("22ms line")
            updated_items.append("22ms text")
        elif y_max < 66:
            updated_items.append("16ms line")
            updated_items.append("16ms text")
            updated_items.append("22ms line")
            updated_items.append("22ms text")
            updated_items.append("33ms line")
            updated_items.append("33ms text")
        elif y_max < 99:
            updated_items.append("22ms line")
            updated_items.append("22ms text")
            updated_items.append("33ms line")
            updated_items.append("33ms text")
            updated_items.append("66ms line")
            updated_items.append("66ms text")
        else:
            updated_items.append("66ms line")
            updated_items.append("66ms text")

        return iter(updated_items)

    def on_mouse_moved(self, coord: Tuple[float, float]) -> None:
        pass

    def on_mouse_clicked(self, coord: Tuple[float, float]) -> None:
        # Range = [0, 299].
        frame_offset: int = int(coord[0])

        # Always update selected frame so that the chart displays vertical bar on mouse click position.
        self.sel_frame = frame_offset

        if self.frame_slice[1] is -1:
            return

        # Chart is half-full.
        if self.frame_slice[1] < 299:
            # Selection made before chart start position.
            if frame_offset < 299 - self.frame_slice[1]:
                return

            frame_offset = abs((299 - self.frame_slice[1]) - frame_offset)

        root: Any = self.winfo_toplevel()
        frame_num: int = self.frame_slice[0] + frame_offset
        root.control_panel.on_frame_selected_from_chart(frame_num)

    def on_frame_info_received(self, frame_info: FrameInfo, selected: bool = False) -> None:
        # Don't update graph when selecting individual frames. Prevents frame shifting on click.
        if not selected:
            self.data.append(frame_info.frame_time)
            self.frame_slice = (max(frame_info.frame_number - min(self.frame_slice[1], 299), 0),
                                frame_info.frame_number)

    def on_frame_info_cleared(self) -> None:
        self.data.clear()
        for i in range(0, 300):
            self.data.append(0)

        self.frame_slice = (-1, -1)

        self.graph.clear()
        self.sel_frame = -1
