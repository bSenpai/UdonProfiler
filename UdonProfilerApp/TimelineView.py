import customtkinter as ctk

from FrameInfo import FrameInfo

from Widgets.TimelineBarPlot.TimelineBarPlotWidget import TimelineBarPlotWidget


class TimelineView(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.timeline_plot: TimelineBarPlotWidget = TimelineBarPlotWidget(self)
        self.timeline_plot.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        '''
        colors = ["tab:blue", "tab:orange", "tab:purple", "tab:red"]
        for i in range(0, 50):
            h = 0 - i * 2
            c = colors[i % len(colors)]
            self.timeline_plot.add_bar("VeryLongTextLabel", h, 2, 5, 15, c, "yellow", 8)
        '''

    def on_frame_info_received(self, frame_info: FrameInfo) -> None:
        self.timeline_plot.clear()

        colors = ["tab:blue", "tab:orange", "tab:purple", "tab:red"]
        start = frame_info.samples[0].start_times[0]
        for sample in frame_info.samples:
            # Parent block covers entirety of child blocks.
            if sample.depth < frame_info.max_depth:
                delta: float = sample.end_times[-1] - sample.start_times[0]
                if delta <= 0:
                    continue

                self.timeline_plot.add_bar(sample.name, 0 - sample.depth * 2, 2,
                                           sample.start_times[0] - start, sample.end_times[-1] - start,
                                           colors[sample.depth % len(colors)], "yellow", 8)
            else:
                for block in list(zip(sample.start_times, sample.end_times)):
                    if block[1] - block[0] <= 0:
                        continue

                    self.timeline_plot.add_bar(sample.name, 0 - sample.depth * 2, 2,
                                               block[0] - start, block[1] - start,
                                               colors[sample.depth % len(colors)], "yellow", 8)

        self.winfo_toplevel().update()

    def on_frame_info_cleared(self) -> None:
        self.timeline_plot.clear()
