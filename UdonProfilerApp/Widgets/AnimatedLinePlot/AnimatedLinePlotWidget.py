from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Iterable, Iterator, List, Tuple, Union

import customtkinter as ctk

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import numpy as np


class PlotItemType(Enum):
    LINE = 1
    VERTICAL_LINE = 2
    HORIZONTAL_LINE = 3
    FILLED_LINE = 4
    TEXT = 5


@dataclass
class PlotItem:
    item_type: PlotItemType
    item: mpl.artist
    params: Dict[str, Any]

    def __init__(self, item_type: PlotItemType, item: mpl.artist, params: Dict[str, Any]) -> None:
        self.item_type = item_type
        self.item = item
        self.params = params


class AnimatedLinePlotWidget(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 350,
                 height: int = 500,
                 animate_cb: Callable[[], Iterable[str]],
                 mouse_motion_cb: Callable[[Tuple[float, float]], None],
                 mouse_press_cb: Callable[[Tuple[float, float]], None],
                 animation_interval: int = 100,
                 x_range: Tuple[float, float] = (0, 100),
                 y_range: Tuple[float, float] = (0, 100),
                 max_points: int = 100,
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.animate_cb: Callable[[], Iterable[str]] = animate_cb
        self.mouse_motion_cb: Callable[[Tuple[float, float]], None] = mouse_motion_cb
        self.mouse_press_cb: Callable[[Tuple[float, float]], None] = mouse_press_cb
        self.animation_interval: int = animation_interval
        self.x_range: Tuple[float, float] = x_range
        self.y_range: Tuple[float, float] = y_range
        self.max_points: int = max_points

        self.plot_items: Dict[str, PlotItem] = dict()

        self.configure(fg_color=("gray78", "gray28"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        mpl.use("TkAgg")
        plt.style.use("./mplstyles/dracula.mplstyle")

        self.figure: mpl.Figure = plt.figure(dpi=100)

        # Force graph to fill window.
        # Source: https://stackoverflow.com/a/42620544
        self.axes: mpl.axes.Axes = self.figure.add_axes([0, 0, 1, 1])
        self.axes.axis("off")
        self.axes.margins(0)

        self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.animation: FuncAnimation = FuncAnimation(self.figure, self.animate,
                                                      interval=self.animation_interval, blit=True)

        # Bind events.
        # See: https://matplotlib.org/stable/users/explain/event_handling.html
        self.cid_press: int = self.figure.canvas.mpl_connect(
            "button_press_event", lambda event: self.on_mouse_clicked(event))
        self.cid_motion: int = self.figure.canvas.mpl_connect(
            "motion_notify_event", lambda event: self.on_mouse_moved(event))

        self.update_plot_range()

    def animate(self, i: int) -> Iterable[mpl.artist]:
        updated_artist_names: List[str] = list(self.animate_cb())
        updated_artists: List[mpl.artist] = list()
        for artist_name in updated_artist_names:
            if artist_name in self.plot_items:
                if self.plot_items[artist_name].item_type == PlotItemType.FILLED_LINE:
                    # Redraw filled lines.
                    # See: https://stackoverflow.com/a/44413638
                    item: mpl.artist = self.plot_items[artist_name].item
                    params: Dict[str, Any] = self.plot_items[artist_name].params
                    p = self.axes.fill_between(
                        item.get_xdata()[:self.max_points],
                        [params["min_val"]] * self.max_points,
                        item.get_ydata()[:self.max_points],
                        facecolor=params["face_color"],
                        alpha=params["opacity"])
                    updated_artists.append(p)

                updated_artists.append(self.plot_items[artist_name].item)

        return updated_artists

    def on_mouse_moved(self, event) -> None:
        # See: https://stackoverflow.com/a/51349960
        x, y = event.xdata, event.ydata
        self.mouse_motion_cb((x, y))

    def on_mouse_clicked(self, event) -> None:
        x, y = event.xdata, event.ydata
        self.mouse_press_cb((x, y))

    def add_line(self, name: str,
                 x_data: Union[float, List[float], None] = None,
                 y_data: Union[float, List[float], None] = None,
                 param_dict: Union[Dict[str, Any], None] = None) -> None:
        self.remove_line(name)

        if not param_dict:
            param_dict = dict()

        item_type: PlotItemType
        item: mpl.artist
        item_params: Dict[str, Any] = param_dict
        if x_data is not None and y_data is not None:
            item_type = PlotItemType.LINE
            item, = self.axes.plot(x_data, y_data, **param_dict)
        elif x_data is not None:
            item_type = PlotItemType.VERTICAL_LINE
            item = self.axes.axvline(x_data, **param_dict)
        elif y_data is not None:
            item_type = PlotItemType.HORIZONTAL_LINE
            item = self.axes.axhline(y_data, **param_dict)
        else:
            return

        self.plot_items[name] = PlotItem(item_type, item, item_params)

    def update_line(self, name: str, x_data: Union[float, List[float], None] = None,
                    y_data: Union[float, List[float], None] = None) -> None:
        if name not in self.plot_items:
            raise ValueError(f"can't update line {name} - does not exist")

        if self.plot_items[name].item_type == PlotItemType.TEXT:
            raise ValueError(f"can't update item {name} - not a line")

        if x_data:
            self.plot_items[name].item.set_xdata(x_data)

        if y_data:
            self.plot_items[name].item.set_ydata(y_data)

    def fill_line(self, name: str, min_val: float, opacity: float) -> None:
        if name not in self.plot_items:
            raise ValueError(f"can't update line {name} - does not exist")

        if self.plot_items[name].item_type == PlotItemType.TEXT:
            raise ValueError(f"can't update item {name} - not a line")

        x_data: List[float] = self.plot_items[name].item.get_xdata()
        y_data: List[float] = self.plot_items[name].item.get_ydata()

        if len(x_data) < self.max_points or len(y_data) < self.max_points:
            raise RuntimeError(f"can't fill line {name} - not enough points", len(x_data), len(y_data))

        # self.axes.fill_between(x_data[:100], [min_val] * 100, y_data[:100], alpha=opacity)

        item_type: PlotItemType = PlotItemType.FILLED_LINE
        item: mpl.artist = self.plot_items[name].item
        item_params: Dict[str, Any] = self.plot_items[name].params

        item_params["min_val"] = min_val
        item_params["face_color"] = "#8be9fd"
        item_params["opacity"] = opacity

        self.plot_items[name] = PlotItem(item_type, item, item_params)

    def remove_line(self, name: str) -> None:
        # See: https://stackoverflow.com/a/13575495
        if name in self.plot_items and \
            (self.plot_items[name].item_type == PlotItemType.LINE or
             self.plot_items[name].item_type == PlotItemType.VERTICAL_LINE or
             self.plot_items[name].item_type == PlotItemType.HORIZONTAL_LINE):
            self.axes.lines.remove(self.plot_items[name].item)
            del self.plot_items[name]

    def add_text(self, name: str, pos: Tuple[float, float], text: str,
                 param_dict: Union[Dict[str, Any], None] = None) -> None:
        if not param_dict:
            param_dict = dict()

        item_type: PlotItemType = PlotItemType.TEXT
        item: mpl.artist = self.axes.text(*pos, text, **param_dict)
        item_params: Dict[str, Any] = param_dict

        self.plot_items[name] = PlotItem(item_type, item, item_params)

    def remove_text(self, name: str) -> None:
        # See: https://stackoverflow.com/a/26006851
        if name in self.plot_items and self.plot_items[name].item_type == PlotItemType.TEXT:
            self.plot_items[name].item.remove()
            del self.plot_items[name]

    def update_plot_range(self,
                          x_range: Union[Tuple[float, float], None] = None,
                          y_range: Union[Tuple[float, float], None] = None) -> None:
        if x_range is not None:
            self.x_range = x_range

        if y_range is not None:
            self.y_range = y_range

        self.axes.set_xlim(*self.x_range)
        self.axes.set_ylim(*self.y_range)

    def clear(self) -> None:
        self.animation.new_frame_seq()

        # See: https://stackoverflow.com/a/49237860
        self.figure.canvas.restore_region(self.background)
        self.figure.canvas.blit(self.axes.bbox)

    def pause(self) -> None:
        self.animation.pause()

    def resume(self) -> None:
        self.animation.resume()


if __name__ == "__main__":
    # GraphWidget Tests.
    import time
    import random
    from collections import deque


    class AnimatedLinePlotWidgetTest(ctk.CTk):
        def __init__(self) -> None:
            super().__init__()

            self.title("GrpahWidget Test")
            self.geometry("700x350")

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.sel_frame: int = -1

            # See: https://stackoverflow.com/a/65135081
            self.data: deque = deque([], maxlen=200)
            for i in range(0, 200):
                self.data.append(0)
            self.x: float = 0

            self.graph: AnimatedLinePlotWidget = AnimatedLinePlotWidget(
                self,
                animation_interval=25,
                animate_cb=self.on_animate,
                mouse_motion_cb=lambda event: self.on_mouse_moved(event),
                mouse_press_cb=lambda event: self.on_mouse_clicked(event),
            )
            self.graph.grid(row=0, column=0, sticky="nsew")

            param_dict: Dict[str, Any] = dict()
            param_dict["linestyle"] = "--"
            self.graph.add_line("frame time", np.arange(0, 200, 1), [10] * 200, param_dict=param_dict)

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
            self.graph.fill_line("frame time", min(self.data), 0.5)
            self.graph.update_plot_range(y_range=(min(self.data) - 5, max(self.data) + 5))

            return "frame time", "selected frame", "5ms line", "10ms line", "5ms text", "10ms text",\
                   "16ms line", "22ms line", "33ms line", "16ms text", "22ms text", "33ms text"

        def on_mouse_moved(self, coord: Tuple[float, float]) -> None:
            pass

        def on_mouse_clicked(self, coord: Tuple[float, float]) -> None:
            self.sel_frame = int(coord[0])

        def run(self) -> None:
            while True:
                val: float = random.randint(0, 20) * np.sin(self.x)
                self.data.append(val)
                self.x += 0.1
                time.sleep(0.001)
                self.update_idletasks()
                self.update()


    app: AnimatedLinePlotWidgetTest = AnimatedLinePlotWidgetTest()
    app.run()
