import platform

from typing import Any

import customtkinter as ctk


class ControlPanel(ctk.CTkFrame):
    # See: https://en.wikipedia.org/wiki/Media_control_symbols
    if platform.system() == "Windows":
        record_sym: str = "\u23fa"
        back_sym: str = "\u23ea"
        forward_sym: str = "\u23e9"
        end_sym: str = "\u23ed"
    else:
        record_sym: str = "rec"
        back_sym: str = "back"
        forward_sym: str = "fwd"
        end_sym: str = "end"
    recording_color: str = "#EE4B2B"
    paused_color: str = "#FFFFFF"

    def __init__(self, master) -> None:
        super().__init__(master)

        self.profiler: Any = master

        self.do_record: bool = False
        self.sel_frame: int = 0

        self.grid_columnconfigure((0, 3), weight=0)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=0)

        self.record_btn: ctk.CTkButton = ctk.CTkButton(self, text=ControlPanel.record_sym, width=20,
                                                       text_color=ControlPanel.paused_color,
                                                       fg_color="transparent",
                                                       hover=False,
                                                       command=self.on_record_btn_clicked)
        self.record_btn.grid(row=0, column=0)

        self.prev_frame_btn: ctk.CTkButton = ctk.CTkButton(self, text=ControlPanel.back_sym, width=20,
                                                           fg_color="transparent",
                                                           hover=False,
                                                           command=self.on_prev_frame_btn_clicked)
        self.prev_frame_btn.grid(row=0, column=1)

        self.next_frame_btn: ctk.CTkButton = ctk.CTkButton(self, text=ControlPanel.forward_sym, width=20,
                                                           fg_color="transparent",
                                                           hover=False,
                                                           command=self.on_next_frame_btn_clicked)
        self.next_frame_btn.grid(row=0, column=2)

        self.cur_frame_btn: ctk.CTkButton = ctk.CTkButton(self, text=ControlPanel.end_sym, width=20,
                                                          fg_color="transparent",
                                                          hover=False,
                                                          command=self.on_cur_frame_btn_clicked)
        self.cur_frame_btn.grid(row=0, column=3)

        self.frame_details_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Frame: -/-", width=150)
        self.frame_details_label.grid(row=0, padx=5, column=4)

        self.clear_frames_btn: ctk.CTkButton = ctk.CTkButton(self, text="clear", width=20,
                                                             fg_color="transparent",
                                                             hover=False,
                                                             command=self.on_clear_frames_btn_clicked)
        self.clear_frames_btn.grid(row=0, column=5)

        self.prev_frame_btn_enabled: bool = True
        self.next_frame_btn_enabled: bool = True
        self.cur_frame_btn_enabled: bool = True
        self.clear_frames_btn_enabled: bool = True

        # Start with buttons disabled.
        self.disable_prev_frame_btn()
        self.disable_next_frame_btn()
        self.disable_cur_frame_btn()
        self.disable_clear_frames_btn()

    def on_record_btn_clicked(self) -> None:
        self.do_record = not self.do_record
        if self.do_record:
            self.record_btn.configure(text_color=ControlPanel.recording_color)
            self.profiler.record()
        else:
            self.record_btn.configure(text_color=ControlPanel.paused_color)
            self.profiler.pause()

    def on_prev_frame_btn_clicked(self) -> None:
        sel_frame, cur_frame = self.profiler.prev_frame()
        if sel_frame > 0 and cur_frame > 0:
            self.set_frame_details(sel_frame, cur_frame)
            self.update_playback_btn_states(self.sel_frame, cur_frame)

    def on_next_frame_btn_clicked(self) -> None:
        sel_frame, cur_frame = self.profiler.next_frame()
        if sel_frame > 0 and cur_frame > 0:
            self.set_frame_details(sel_frame, cur_frame)
            self.update_playback_btn_states(self.sel_frame, cur_frame)

    def on_cur_frame_btn_clicked(self) -> None:
        sel_frame, cur_frame = self.profiler.cur_frame()
        if sel_frame > 0 and cur_frame > 0:
            self.set_frame_details(sel_frame, cur_frame)
            self.update_playback_btn_states(sel_frame, cur_frame)

    def on_frame_selected_from_chart(self, frame_num: int) -> None:
        sel_frame, cur_frame = self.profiler.goto_frame(frame_num)
        self.set_frame_details(sel_frame, cur_frame)

        # Pause frame chart animation.
        self.do_record = False
        self.record_btn.configure(text_color=ControlPanel.paused_color)
        self.profiler.pause()

    def on_clear_frames_btn_clicked(self) -> None:
        self.profiler.clear_frames()
        self.set_frame_details(0, 0)
        self.update_playback_btn_states(0, 0)

    def on_cur_frame_num_changed(self, cur_frame: int) -> None:
        if cur_frame == self.sel_frame:
            return

        self.set_frame_details(self.sel_frame, cur_frame)
        self.update_playback_btn_states(self.sel_frame, cur_frame)

    def set_frame_details(self, sel_frame: int, cur_frame: int) -> None:
        self.sel_frame = sel_frame

        if sel_frame == 0:
            if cur_frame == 0:
                self.frame_details_label.configure(text=f"Frame: -/-")
            else:
                self.frame_details_label.configure(text=f"Frame: -/{cur_frame}")
        else:
            self.frame_details_label.configure(text=f"Frame: {self.sel_frame}/{cur_frame}")

    def update_playback_btn_states(self, sel_frame: int, cur_frame: int) -> None:
        if sel_frame == 1:
            self.disable_prev_frame_btn()
        else:
            self.enable_prev_frame_btn()

        if sel_frame == cur_frame:
            self.disable_next_frame_btn()
            self.disable_cur_frame_btn()
        else:
            self.enable_next_frame_btn()
            self.enable_cur_frame_btn()

        if cur_frame == 0:
            self.disable_prev_frame_btn()
            self.disable_next_frame_btn()
            self.disable_cur_frame_btn()
            self.disable_clear_frames_btn()
        else:
            self.enable_clear_frames_btn()

    def disable_prev_frame_btn(self) -> None:
        if self.prev_frame_btn_enabled:
            self.prev_frame_btn.configure(state="disabled")
            self.prev_frame_btn_enabled = False

    def enable_prev_frame_btn(self) -> None:
        if not self.prev_frame_btn_enabled:
            self.prev_frame_btn.configure(state="normal")
            self.prev_frame_btn_enabled = True

    def disable_next_frame_btn(self) -> None:
        if self.next_frame_btn_enabled:
            self.next_frame_btn.configure(state="disabled")
            self.next_frame_btn_enabled = False

    def enable_next_frame_btn(self) -> None:
        if not self.next_frame_btn_enabled:
            self.next_frame_btn.configure(state="normal")
            self.next_frame_btn_enabled = True

    def disable_cur_frame_btn(self) -> None:
        if self.cur_frame_btn_enabled:
            self.cur_frame_btn.configure(state="disabled")
            self.cur_frame_btn_enabled = False

    def enable_cur_frame_btn(self) -> None:
        if not self.cur_frame_btn_enabled:
            self.cur_frame_btn.configure(state="normal")
            self.cur_frame_btn_enabled = True

    def disable_clear_frames_btn(self) -> None:
        if self.clear_frames_btn_enabled:
            self.clear_frames_btn.configure(state="disabled")
            self.clear_frames_btn_enabled = False

    def enable_clear_frames_btn(self) -> None:
        if not self.clear_frames_btn_enabled:
            self.clear_frames_btn.configure(state="normal")
            self.clear_frames_btn_enabled = True
