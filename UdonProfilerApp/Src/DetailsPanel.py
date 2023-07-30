import customtkinter as ctk

from Src.HierarchyView import HierarchyView
from Src.TimelineView import TimelineView
from Src.StatisticsView import StatisticsView
from Src.FrameInfo import FrameInfo


class DetailsPanel(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        title: str = "Details Panel"
        self.title: ctk.CTkLabel = ctk.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, sticky="ew")

        self.tabview: ctk.CTkTabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew")

        self.hierarchy_tabview: ctk.CTkFrame = self.tabview.add("Hierarchy View")
        self.hierarchy_tabview.grid_columnconfigure(0, weight=1)
        self.hierarchy_tabview.grid_rowconfigure(0, weight=1)

        self.timeline_tabview: ctk.CTkFrame = self.tabview.add("Timeline View")
        self.timeline_tabview.grid_columnconfigure(0, weight=1)
        self.timeline_tabview.grid_rowconfigure(0, weight=1)

        self.statistics_tabview: ctk.CTkFrame = self.tabview.add("Statistics View")
        self.statistics_tabview.grid_columnconfigure(0, weight=1)
        self.statistics_tabview.grid_rowconfigure(0, weight=1)

        self.tabview.set("Hierarchy View")

        self.hierarchy_view: HierarchyView = HierarchyView(master=self.hierarchy_tabview)
        self.hierarchy_view.grid(row=0, column=0, sticky="nsew")

        self.timeline_view: TimelineView = TimelineView(master=self.timeline_tabview)
        self.timeline_view.grid(row=0, column=0, stick="nsew")

        self.statistics_view: StatisticsView = StatisticsView(master=self.statistics_tabview)
        self.statistics_view.grid(row=0, column=0, sticky="nsew")

    def on_frame_info_received(self, frame_info: FrameInfo, selected: bool = False) -> None:
        if selected:
            self.hierarchy_view.on_frame_info_received(frame_info)
            self.timeline_view.on_frame_info_received(frame_info)

        self.statistics_view.on_frame_info_received(frame_info)

    def on_frame_info_cleared(self) -> None:
        self.hierarchy_view.on_frame_info_cleared()
        self.timeline_view.on_frame_info_cleared()
        self.statistics_view.on_frame_info_cleared()
