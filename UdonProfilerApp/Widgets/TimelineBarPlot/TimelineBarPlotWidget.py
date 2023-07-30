from typing import List, Tuple

import customtkinter as ctk

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.collections import BrokenBarHCollection

from Widgets.NavigationToolbar.NavigationToolbar2CTk import NavigationToolbar2CTk
from Utils.PathResolver import resource_path


class TimelineBarPlotWidget(ctk.CTkFrame):
    # Create scrollable matplotlib frame. Doesn't work?
    # See: https://stackoverflow.com/a/74929672
    """
    def __init__(self, *args,
                 width: int = 350,
                 height: int = 500,
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        mpl.use("TkAgg")
        plt.style.use("./mplstyles/dracula.mplstyle")

        self.figure: mpl.Figure = plt.figure(dpi=74)

        # Force graph to fill window.
        # Source: https://stackoverflow.com/a/42620544
        self.axes: mpl.axes.Axes = self.figure.add_axes([0.025, 0.00625, .95, 0.925])
        self.axes.margins(0)

        self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.x_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal")
        self.x_scrollbar.grid(row=2, column=0, sticky="ew")

        canvas = ctk.CTkCanvas(self, xscrollcommand=self.x_scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        self.x_scrollbar.configure(command=canvas.xview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = ctk.CTkFrame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")

        def _configure_interior(event) -> None:
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.configure(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.configure(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event) -> None:
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

        self.axes.set_ylim(0, 1)
        self.axes.set_xlim(0, 1)
        self.axes.set_yticks([])
        self.axes.set_yticklabels([])

        # Set axes at top of graph.
        # See: https://stackoverflow.com/a/14406447
        self.axes.xaxis.tick_top()
        self.axes.grid(True, axis="x", alpha=0.5)

        self.bars = list()
        self.annotations = list()

        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(self.figure, self.interior)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Allow matplotlib toolbar to work with grid layout.
        # See: https://stackoverflow.com/a/51018685
        self.toolbar_frame = ctk.CTkFrame(self)
        self.toolbar_frame.grid(row=1, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
    """

    def __init__(self, *args,
                 width: int = 350,
                 height: int = 500,
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2), weight=0)

        mpl.use("TkAgg")
        plt.style.use(resource_path("Assets\\dracula.mplstyle"))

        # TODO: Find a more permanent solution to graph size. Dpi of 74 is a temp fix.
        self.figure: mpl.Figure = plt.figure(dpi=65)

        # Force graph to fill window.
        # Source: https://stackoverflow.com/a/42620544
        self.axes: mpl.axes.Axes = self.figure.add_axes([0.025, 0.00625, .95, 0.925])
        self.axes.margins(0)

        self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.axes.set_ylim(0, 1)
        self.axes.set_xlim(0, 1)
        self.axes.set_yticks([])
        self.axes.set_yticklabels([])

        # Set axes at top of graph.
        # See: https://stackoverflow.com/a/14406447
        self.axes.xaxis.tick_top()
        self.axes.grid(True, axis="x", alpha=0.5)

        self.bars = list()
        self.annotations = list()
        self.bar_names = dict()
        self.bar_infos = dict()

        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Remove unnecessary toolbar buttons.
        # See: https://stackoverflow.com/a/59156387
        NavigationToolbar2CTk.toolitems = [t for t in NavigationToolbar2CTk.toolitems if t[0] not in
                                           ('Back', 'Forward', 'Subplots', 'Save')]

        self.toolbar = NavigationToolbar2CTk(self.canvas, self, pack_toolbar=False)
        # print(self.toolbar.configure().keys())
        self.toolbar.configure(background="#282A36")
        for button in self.toolbar.winfo_children():
            button.configure(background="#282A36")
        self.toolbar.grid(row=1, column=0, sticky="ew")
        self.toolbar.update()

        # Scrollbar. Doesn't work?
        # See: https://stackoverflow.com/a/56090565
        # self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal")
        # self.scrollbar.grid(row=2, column=0, sticky="ew")
        # self.scrollbar["command"] = self.canvas.get_tk_widget().xview
        # self.canvas.get_tk_widget()["xscrollcommand"] = self.scrollbar.set

        # Tooltip setup.
        # See: https://stackoverflow.com/a/66501612
        self.tooltip = self.axes.annotate("", xy=(0, 0), xytext=(20, -20), textcoords="offset points", fontsize=12,
                                          bbox=dict(boxstyle="round", fc="#282A36", ec="#F8F8F2", lw=2))

        self.figure.canvas.mpl_connect("motion_notify_event", lambda event: self.on_hover(event))

        self.canvas.draw()

    def add_bar(self, name: str, y_start: float, height: float, start: float, end: float, facecolor: str,
                textcolor: str, fontsize: int) -> None:
        if start > end or (end - start) == 0:
            raise RuntimeError("bar plot size is invalid", start, end)

        bar = self.axes.broken_barh([(start, end - start)], (y_start, height), facecolors=facecolor, edgecolor="black")

        # Store information for tooltip.
        self.bar_names[bar] = name
        if name not in self.bar_infos.keys():
            self.bar_infos[name] = dict()
            self.bar_infos[name]["instances"] = 1
            self.bar_infos[name]["total_duration"] = end - start
        else:
            self.bar_infos[name]["instances"] += 1
            self.bar_infos[name]["total_duration"] += end - start

        self.bars.append(bar)

        # Don't set y lim to allow vertical scrolling. Doing otherwise would force graph to fit all bars in single view.
        # y_lim_old: Tuple[float, float] = self.axes.get_ylim()
        # y_lim_new: Tuple[float, float] = (min(y_lim_old[0], y_start - height), max(y_lim_old[1], y_start + height))
        # self.axes.set_ylim(y_lim_new)

        x_lim_old: Tuple[float, float] = self.axes.get_xlim()
        x_lim_new: Tuple[float, float] = (min(x_lim_old[0], start), max(x_lim_old[1], end))
        self.axes.set_xlim(x_lim_new)

        # Clip text within bar boundaries.
        # See: https://stackoverflow.com/a/27746640
        box: TransformedBbox = TransformedBbox(
            Bbox(
                [[max(start, x_lim_new[0]), y_start],
                 [min(start + end, x_lim_new[1]), y_start + height]]
            ),
            self.axes.transData
        )

        # Center text within bar boundaries.
        # See: https://stackoverflow.com/a/66837165
        annotation = self.axes.annotate(name, xy=(start + (end - start) / 2, y_start + height / 2), color=textcolor,
                                        ha="center", va="center", fontsize=fontsize, clip_box=box)
        self.annotations.append(annotation)

        # Force tkinter to update canvas.
        # See: https://stackoverflow.com/a/30783010
        self.canvas.draw()

    def clear(self) -> None:
        for bar in self.bars:
            bar.remove()

        self.bars.clear()

        for annotation in self.annotations:
            annotation.remove()

        self.annotations.clear()

        self.bar_names.clear()
        self.bar_infos.clear()

        self.axes.set_ylim(0, 1)
        self.axes.set_xlim(0, 1)

        self.figure.canvas.restore_region(self.background)
        self.figure.canvas.blit(self.axes.bbox)

    def update_tooltip(self, bars: BrokenBarHCollection, ind: int, x: float, y: float) -> None:
        # Update tooltip when hovering over bar.
        # See: https://stackoverflow.com/a/66501612
        self.tooltip.xy = (x, y)
        box = bars.get_paths()[ind].get_extents()

        # Prepare tooltip display info. Emulate Unity's tooltip info.
        name: str = self.bar_names[bars]
        duration: float = box.x1 - box.x0
        instances: int = self.bar_infos[name]["instances"]
        total_duration: float = self.bar_infos[name]["total_duration"]
        text = f"{name}\n{duration:.0f}ms"
        if instances > 1:
            text += f"\nTotal:{total_duration:.0f}ms ({instances} Instances)"

        self.tooltip.set_text(text)
        self.tooltip.get_bbox_patch().set_alpha(0.9)

    def on_hover(self, event) -> None:
        # Handle mouse hover event.
        # See: https://stackoverflow.com/a/66501612
        vis = self.tooltip.get_visible()
        if event.inaxes == self.axes:
            for _, bars in enumerate(self.axes.collections):
                bar_contains, ind = bars.contains(event)
                if bar_contains:
                    self.update_tooltip(bars, ind['ind'][0], event.xdata, event.ydata)
                    self.tooltip.set_visible(True)
                    self.figure.canvas.draw_idle()
                    return

        if vis:
            self.tooltip.set_visible(False)
            self.figure.canvas.draw_idle()


if __name__ == "__main__":
    class TimelineBarPlotWidgetTest(ctk.CTk):
        def __init__(self) -> None:
            super().__init__()

            self.title("Timeline Bar Plot Widget Test")
            self.geometry("700x450")

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.bar_plot: TimelineBarPlotWidget = TimelineBarPlotWidget(self)
            self.bar_plot.grid(row=0, column=0, sticky="nsew")

            self.bar_plot.add_bar("VeryLongTextLabel", 20, 4, 10, 80, "tab:blue", "white", 8)
            self.bar_plot.add_bar("VeryLongTextLabel", 20, 4, 300, 350, "tab:blue", "white", 8)

            self.bar_plot.clear()

    app: TimelineBarPlotWidgetTest = TimelineBarPlotWidgetTest()
    app.mainloop()
