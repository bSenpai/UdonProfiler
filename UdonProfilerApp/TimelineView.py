from typing import List

import customtkinter as ctk

from FrameInfo import FrameInfo

from Widgets.TimelineBarPlot.TimelineBarPlotWidget import TimelineBarPlotWidget


class TimelineView(ctk.CTkFrame):
    colors: List[str] = ['#8be9fd', '#ff79c6', '#50fa7b', '#bd93f9', '#ffb86c', '#ff5555', '#f1fa8c', '#6272a4']
    text_color: str = "#282a36"
    font_size: int = 12
    bar_height: float = 0.1

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.timeline_plot: TimelineBarPlotWidget = TimelineBarPlotWidget(self)
        self.timeline_plot.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for i in range(0, 50):
            h = 1 - TimelineView.bar_height - i * TimelineView.bar_height
            c = TimelineView.colors[i % len(TimelineView.colors)]
            self.timeline_plot.add_bar("VeryLongTextLabel", h, TimelineView.bar_height, 5, 15, c,
                                       TimelineView.text_color, TimelineView.font_size)

    def on_frame_info_received(self, frame_info: FrameInfo) -> None:
        self.timeline_plot.clear()

        start = frame_info.samples[0].start_times[0]
        for sample in frame_info.samples:
            # Parent block covers entirety of child blocks.
            if sample.depth < frame_info.max_depth:
                delta: float = sample.end_times[-1] - sample.start_times[0]
                if delta <= 0:
                    continue

                self.timeline_plot.add_bar(sample.name, 1 - TimelineView.bar_height -
                                           sample.depth * TimelineView.bar_height, TimelineView.bar_height,
                                           sample.start_times[0] - start, sample.end_times[-1] - start,
                                           TimelineView.colors[sample.depth % len(TimelineView.colors)],
                                           TimelineView.text_color, TimelineView.font_size)
            else:
                for block in list(zip(sample.start_times, sample.end_times)):
                    if block[1] - block[0] <= 0:
                        continue

                    self.timeline_plot.add_bar(sample.name, 1 - TimelineView.bar_height -
                                               sample.depth * TimelineView.bar_height, TimelineView.bar_height,
                                               block[0] - start, block[1] - start,
                                               TimelineView.colors[sample.depth % len(TimelineView.colors)],
                                               TimelineView.text_color, TimelineView.font_size)

        self.winfo_toplevel().update()

    def on_frame_info_cleared(self) -> None:
        self.timeline_plot.clear()
