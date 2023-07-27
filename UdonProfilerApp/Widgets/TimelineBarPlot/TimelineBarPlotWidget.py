from typing import List, Tuple

import customtkinter as ctk

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.transforms import Bbox, TransformedBbox


class TimelineBarPlotWidget(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 350,
                 height: int = 500,
                 **kwargs) -> None:
        super().__init__(*args, width=width, height=height, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        mpl.use("TkAgg")
        # plt.style.use("../../mplstyles/dracula.mplstyle")
        plt.style.use("./mplstyles/dracula.mplstyle")

        self.figure: mpl.Figure = plt.figure(dpi=100)
        # self.axes: mpl.axes.Axes = self.figure.add_subplot(111)

        # Force graph to fill window.
        # Source: https://stackoverflow.com/a/42620544
        self.axes: mpl.axes.Axes = self.figure.add_axes([0.025, 0.00625, .95, 0.925])
        self.axes.margins(0)

        self.background = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.canvas: FigureCanvasTkAgg = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

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

        self.canvas.draw()

    def add_bar(self, name: str, y_start: float, height: float, start: float, end: float, facecolor: str,
                textcolor: str, fontsize: int) -> None:
        if start > end or (end - start) == 0:
            raise RuntimeError("bar plot size is invalid", start, end)

        bar = self.axes.broken_barh([(start, end - start)], (y_start, height), facecolors=facecolor, edgecolor="black")
        self.bars.append(bar)

        y_lim_old: Tuple[float, float] = self.axes.get_ylim()
        y_lim_new: Tuple[float, float] = (min(y_lim_old[0], y_start - height), max(y_lim_old[1], y_start + height))
        self.axes.set_ylim(y_lim_new)

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

        self.axes.set_ylim(0, 1)
        self.axes.set_xlim(0, 1)

        self.figure.canvas.restore_region(self.background)
        self.figure.canvas.blit(self.axes.bbox)


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
