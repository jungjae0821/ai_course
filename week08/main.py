"""Tkinter user interface for the parking fee calculator."""

from __future__ import annotations

import json
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any

from calculator import calculate_parking_info


class ParkingApp:
    """Manage parking records and display them in a small Tkinter app."""

    def __init__(self, root: tk.Tk, data_file: str | None = None) -> None:
        self.root = root
        self.root.title("주차 요금 계산기")
        self.root.minsize(620, 360)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        default_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
        self.data_file = data_file or default_data_file
        self.history: list[dict[str, Any]] = self.load_data()
        self.editing_index: int | None = None

        self.setup_ui()
        self.update_list()

    def setup_ui(self) -> None:
        """Build the input form, record list, and action buttons."""
        input_frame = ttk.LabelFrame(self.root, text="주차 정보")
        input_frame.pack(fill=tk.X, padx=12, pady=(12, 8))

        ttk.Label(input_frame, text="입차 시간 (HH:mm)").grid(
            row=0, column=0, padx=(10, 6), pady=10, sticky=tk.W
        )
        self.entry_entry_time = ttk.Entry(input_frame, width=14)
        self.entry_entry_time.grid(row=0, column=1, padx=6, pady=10)

        ttk.Label(input_frame, text="출차 시간 (HH:mm)").grid(
            row=0, column=2, padx=(18, 6), pady=10, sticky=tk.W
        )
        self.entry_exit_time = ttk.Entry(input_frame, width=14)
        self.entry_exit_time.grid(row=0, column=3, padx=6, pady=10)

        self.submit_button = ttk.Button(input_frame, text="계산 및 추가", command=self.submit_record)
        self.submit_button.grid(
            row=0, column=4, padx=(18, 10), pady=10
        )
        self.cancel_edit_button = ttk.Button(
            input_frame, text="수정 취소", command=self.cancel_edit, state=tk.DISABLED
        )
        self.cancel_edit_button.grid(row=0, column=5, padx=(0, 10), pady=10)

        for entry in (self.entry_entry_time, self.entry_exit_time):
            entry.bind("<KeyRelease>", lambda _event, target=entry: self.auto_format_time(target))
            entry.bind("<FocusOut>", lambda _event, target=entry: self.auto_format_time(target))
            entry.bind("<Return>", lambda _event: self.submit_record())

        ttk.Label(input_frame, text="4자리 입력 예: 2300 → 23:00").grid(
            row=1, column=0, columnspan=6, padx=10, pady=(0, 8), sticky=tk.W
        )

        list_frame = ttk.LabelFrame(self.root, text="주차 내역")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.canvas = tk.Canvas(list_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.rows_frame = ttk.Frame(self.canvas)
        self.rows_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.rows_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(self.rows_window, width=event.width),
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.label_total = ttk.Label(footer, text="총 합계: 0원", font=("TkDefaultFont", 11, "bold"))
        self.label_total.pack(side=tk.LEFT)
        ttk.Button(footer, text="내역 저장 (.txt)", command=self.export_to_txt).pack(side=tk.RIGHT)

    def load_data(self) -> list[dict[str, Any]]:
        """Load valid records from data.json, falling back safely if needed."""
        if not os.path.exists(self.data_file):
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        records: list[dict[str, Any]] = []
        for record in data:
            if not isinstance(record, dict):
                continue
            if not all(key in record for key in ("entry", "exit", "duration", "fee")):
                continue
            if not isinstance(record["entry"], str) or not isinstance(record["exit"], str):
                continue
            try:
                duration = int(record["duration"])
                fee = int(record["fee"])
            except (TypeError, ValueError):
                continue
            records.append(
                {
                    "entry": record["entry"],
                    "exit": record["exit"],
                    "duration": duration,
                    "fee": fee,
                }
            )
        return records

    def save_data(self) -> None:
        """Persist all current records as UTF-8 JSON."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.history, file, ensure_ascii=False, indent=2)

    @staticmethod
    def normalize_time_input(value: str) -> str:
        """Convert a four-digit time such as ``2300`` to ``23:00``."""
        value = value.strip()
        if re.fullmatch(r"\d{4}", value):
            return f"{value[:2]}:{value[2:]}"
        return value

    def auto_format_time(self, entry: ttk.Entry) -> None:
        """Add the colon while typing and normalize pasted four-digit input."""
        value = entry.get().strip()
        normalized = self.normalize_time_input(value)
        if re.fullmatch(r"\d{2}", value):
            normalized = f"{value}:"

        if normalized != entry.get():
            entry.delete(0, tk.END)
            entry.insert(0, normalized)
            entry.icursor(tk.END)

    def submit_record(self) -> None:
        """Add a new record or save the record currently being edited."""
        if self.editing_index is None:
            self.add_record()
        else:
            self.save_edit()

    def add_record(self) -> None:
        entry_time = self.normalize_time_input(self.entry_entry_time.get())
        exit_time = self.normalize_time_input(self.entry_exit_time.get())
        self._calculate_and_store(entry_time, exit_time)

    def _calculate_and_store(self, entry_time: str, exit_time: str) -> None:
        """Validate input and add a new record to the history."""

        try:
            duration, fee = calculate_parking_info(entry_time, exit_time)
        except ValueError as exc:
            messagebox.showerror("입력 오류", str(exc))
            return

        self.history.append(
            {
                "entry": entry_time,
                "exit": exit_time,
                "duration": duration,
                "fee": fee,
            }
        )
        self.save_data()
        self.update_list()
        self.entry_entry_time.delete(0, tk.END)
        self.entry_exit_time.delete(0, tk.END)
        self.entry_entry_time.focus_set()

    def start_edit(self, index: int) -> None:
        """Load one existing record into the input fields for editing."""
        if not 0 <= index < len(self.history):
            return

        record = self.history[index]
        self.editing_index = index
        self.entry_entry_time.delete(0, tk.END)
        self.entry_entry_time.insert(0, record["entry"])
        self.entry_exit_time.delete(0, tk.END)
        self.entry_exit_time.insert(0, record["exit"])
        self.submit_button.config(text="수정 저장")
        self.cancel_edit_button.config(state=tk.NORMAL)
        self.entry_entry_time.focus_set()

    def save_edit(self) -> None:
        """Validate and replace the record currently being edited."""
        if self.editing_index is None:
            return

        entry_time = self.normalize_time_input(self.entry_entry_time.get())
        exit_time = self.normalize_time_input(self.entry_exit_time.get())
        try:
            duration, fee = calculate_parking_info(entry_time, exit_time)
        except ValueError as exc:
            messagebox.showerror("입력 오류", str(exc))
            return

        self.history[self.editing_index] = {
            "entry": entry_time,
            "exit": exit_time,
            "duration": duration,
            "fee": fee,
        }
        self.save_data()
        self.cancel_edit()
        self.update_list()

    def cancel_edit(self) -> None:
        """Leave edit mode and clear the input fields."""
        self.editing_index = None
        self.submit_button.config(text="계산 및 추가")
        self.cancel_edit_button.config(state=tk.DISABLED)
        self.entry_entry_time.delete(0, tk.END)
        self.entry_exit_time.delete(0, tk.END)

    def update_list(self) -> None:
        """Refresh every record row and recalculate the total immediately."""
        for child in self.rows_frame.winfo_children():
            child.destroy()

        headers = ("입차 시간", "출차 시간", "주차 시간", "요금", "", "")
        widths = (16, 16, 16, 16, 10, 10)
        for column, (header, width) in enumerate(zip(headers, widths)):
            ttk.Label(self.rows_frame, text=header, width=width, anchor=tk.CENTER).grid(
                row=0, column=column, padx=4, pady=(8, 5), sticky=tk.EW
            )

        total_fee = 0
        for index, record in enumerate(self.history, start=1):
            values = (
                record["entry"],
                record["exit"],
                f'{record["duration"]}분',
                f'{record["fee"]:,}원',
            )
            for column, value in enumerate(values):
                ttk.Label(self.rows_frame, text=value, anchor=tk.CENTER).grid(
                    row=index, column=column, padx=4, pady=4, sticky=tk.EW
                )
            ttk.Button(
                self.rows_frame,
                text="수정",
                command=lambda record_index=index - 1: self.start_edit(record_index),
            ).grid(row=index, column=4, padx=4, pady=2)
            ttk.Button(
                self.rows_frame,
                text="삭제",
                command=lambda record_index=index - 1: self.delete_record(record_index),
            ).grid(row=index, column=5, padx=4, pady=2)
            total_fee += int(record["fee"])

        if not self.history:
            ttk.Label(self.rows_frame, text="저장된 주차 내역이 없습니다.").grid(
                row=1, column=0, columnspan=6, padx=8, pady=18
            )

        for column in range(6):
            self.rows_frame.columnconfigure(column, weight=1)
        self.label_total.config(text=f"총 합계: {total_fee:,}원")

    def delete_record(self, index: int) -> None:
        """Delete one row and persist the updated total."""
        if not 0 <= index < len(self.history):
            return
        del self.history[index]
        if self.editing_index is not None:
            if index == self.editing_index:
                self.cancel_edit()
            elif index < self.editing_index:
                self.editing_index -= 1
        self.save_data()
        self.update_list()

    def export_to_txt(self) -> None:
        """Export all records and their total to a UTF-8 text file."""
        if not self.history:
            messagebox.showwarning("알림", "저장할 내역이 없습니다.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="주차 내역 저장",
        )
        if not file_path:
            return

        total_fee = sum(int(record["fee"]) for record in self.history)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("주차 내역 보고서\n")
            file.write("-" * 50 + "\n")
            for record in self.history:
                file.write(
                    f'입차: {record["entry"]} | 출차: {record["exit"]} | '
                    f'주차: {record["duration"]}분 | 요금: {int(record["fee"]):,}원\n'
                )
            file.write("-" * 50 + "\n")
            file.write(f"총 합계 요금: {total_fee:,}원\n")

        messagebox.showinfo("완료", "파일이 저장되었습니다.")

    def on_close(self) -> None:
        """Save once more when the window is closed."""
        try:
            self.save_data()
        except OSError as exc:
            messagebox.showerror("저장 오류", f"데이터를 저장하지 못했습니다.\n{exc}")
            return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ParkingApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # 콘솔에서 Ctrl+C로 종료할 때 traceback을 표시하지 않습니다.
        root.destroy()
