from __future__ import annotations

from typing import Iterator, List, TextIO, Tuple, Union

import os

import tkinter as tk
import customtkinter as ctk

from Src.Sample import Sample
from Src.FrameInfo import FrameInfo
from Src.FrameChart import FrameChart
from Src.DetailsPanel import DetailsPanel
from Src.ControlPanel import ControlPanel


class UdonProfiler(ctk.CTk):
    frame_begin_symbol: str = "##FRAME_INFO_BEGIN##"
    frame_end_symbol: str = "##FRAME_INFO_END##"
    frame_min: int = 1

    def __init__(self, logfile_name: str) -> None:
        super().__init__()
        self.logfile_name: str = logfile_name

        self.frame_infos: List[FrameInfo] = list()
        self.cur_frame_num: int = UdonProfiler.frame_min - 1
        self.sel_frame_num: int = UdonProfiler.frame_min - 1
        self.is_recording: bool = False
        self.is_running: bool = True

        self.title("Udon Profiler")
        self.geometry("950x950")

        # Layout:
        #   Control Panel
        #   Frame Chart
        #   Details Panel
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1, minsize=350)

        self.control_panel: ControlPanel = ControlPanel(self)
        self.control_panel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.frame_chart: FrameChart = FrameChart(self)
        self.frame_chart.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.details_panel: DetailsPanel = DetailsPanel(self)
        self.details_panel.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Clean exit.
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def run(self) -> None:
        reading_frame: bool = False
        current_frame_info: Union[FrameInfo, None] = None

        logfile: TextIO = open(self.logfile_name, "r")
        lines: Iterator[str] = self.tail(logfile)
        for line in lines:
            # Discard any frames read while recording is paused.
            if not self.is_recording:
                # Clear any frame info that may have been being processed when pause button hit.
                reading_frame = False
                current_frame_info = None
                continue

            # Start reading frame info.
            if UdonProfiler.frame_begin_symbol in line:
                reading_frame = True

                self.cur_frame_num += 1
                current_frame_info = FrameInfo(self.cur_frame_num)
                self.control_panel.on_cur_frame_num_changed(self.cur_frame_num)

                # Initialize frame counter view since it's not set at startup.
                if self.cur_frame_num == UdonProfiler.frame_min:
                    self.control_panel.set_frame_details(UdonProfiler.frame_min, self.cur_frame_num)

                continue

            # Parse remaining frame info.
            if reading_frame:
                # Stop reading frame info.
                if UdonProfiler.frame_end_symbol in line:
                    reading_frame = False

                    if current_frame_info:
                        self.frame_infos.append(current_frame_info)
                        self.frame_chart.on_frame_info_received(current_frame_info)
                        self.details_panel.on_frame_info_received(current_frame_info, selected=False)

                    # Populate frame views since they're empty at startup.
                    if self.cur_frame_num == UdonProfiler.frame_min:
                        self.sel_frame_num = self.cur_frame_num

                        frame_info: Union[FrameInfo, None] = self.get_selected_frame_info()
                        if frame_info:
                            self.details_panel.on_frame_info_received(frame_info, selected=True)

                # Read sample from frame info.
                else:
                    sample: Sample = Sample(line)

                    if current_frame_info:
                        current_frame_info.add_sample(sample)

    def update_loop(self) -> None:
        self.update_idletasks()
        self.update()

    def on_exit(self) -> None:
        self.is_running = False
        tk.Tk.quit(self)

    def tail(self, file: TextIO) -> Iterator[str]:
        """
        generator function that yields new lines in a file
        """

        # seek the end of the file
        file.seek(0, os.SEEK_END)

        # start infinite loop
        while self.is_running:
            # read last line of file
            line: Union[str, None] = file.readline()
            if not line:
                # Run GUI loop if file has not been updated.
                self.update_loop()
                continue

            yield line

    def record(self) -> None:
        self.is_recording = True

    def pause(self) -> None:
        self.is_recording = False

    def prev_frame(self) -> Tuple[int, int]:
        if self.sel_frame_num > UdonProfiler.frame_min:
            self.sel_frame_num -= 1

        return self.change_frame()

    def next_frame(self) -> Tuple[int, int]:
        if self.sel_frame_num < len(self.frame_infos):
            self.sel_frame_num += 1

        return self.change_frame()

    def cur_frame(self) -> Tuple[int, int]:
        self.sel_frame_num = len(self.frame_infos)

        return self.change_frame()

    def goto_frame(self, frame_num: int) -> Tuple[int, int]:
        if frame_num < 0 or frame_num > len(self.frame_infos) - UdonProfiler.frame_min:
            raise RuntimeError(f"can't go to frame {frame_num} - out of range")

        self.sel_frame_num = frame_num + UdonProfiler.frame_min

        return self.change_frame()

    def change_frame(self) -> Tuple[int, int]:
        frame_info: Union[FrameInfo, None] = self.get_selected_frame_info()
        if frame_info:
            self.details_panel.on_frame_info_received(frame_info, selected=True)
            self.frame_chart.on_frame_info_received(frame_info, selected=True)

        return self.sel_frame_num, self.cur_frame_num

    def get_selected_frame_info(self) -> Union[FrameInfo, None]:
        if self.sel_frame_num < UdonProfiler.frame_min:
            return None

        return self.frame_infos[self.sel_frame_num - UdonProfiler.frame_min]

    def clear_frames(self) -> None:
        self.frame_infos.clear()
        self.sel_frame_num = UdonProfiler.frame_min - 1
        self.cur_frame_num = UdonProfiler.frame_min - 1
        self.details_panel.on_frame_info_cleared()
        self.frame_chart.on_frame_info_cleared()


if __name__ == "__main__":
    # See: https://stackoverflow.com/a/29158947
    # See: https://stackoverflow.com/a/59625277
    # See: https://stackoverflow.com/a/3794505
    # See: https://tkdocs.com/tutorial/tree.html
    # See: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
    # See: https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
    # See: https://www.tutorialspoint.com/how-to-clear-items-from-a-ttk-treeview-widget
    # See: https://www.tutorialspoint.com/python/tk_frame.htm
    # See: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
    # See: https://stackoverflow.com/a/21198403
    # See: https://stackoverflow.com/a/61020195
    # See: https://coderslegacy.com/python/tkinter-pack-two-frames-side-by-side/
    # See: https://stackoverflow.com/a/62338378
    # See: https://stackoverflow.com/a/13308493
    # See: https://stackoverflow.com/a/73069099

    from os import path

    # See: https://stackoverflow.com/a/52534405
    #      https://docs.unity3d.com/Manual/LogFiles.html
    log_file: str = path.expandvars(r"%LOCALAPPDATA%\Unity\Editor\Editor.log")

    app: UdonProfiler = UdonProfiler(log_file)
    app.run()
