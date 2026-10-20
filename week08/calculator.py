"""Parking fee calculation logic.

This module intentionally contains no GUI code so that the rules can be
tested independently from the Tkinter application.
"""

import math
import re
from datetime import datetime


FREE_MINUTES = 30
UNIT_MINUTES = 10
UNIT_FEE = 500
MAX_FEE = 20_000
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def parse_time(time_str: str) -> datetime:
    """Parse a time written strictly in ``HH:mm`` format."""
    if not isinstance(time_str, str) or not TIME_PATTERN.fullmatch(time_str):
        raise ValueError("시간 형식이 잘못되었습니다. HH:mm 형식을 사용하세요.")

    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError as exc:
        raise ValueError("시간 형식이 잘못되었습니다. HH:mm 형식을 사용하세요.") from exc


def calculate_parking_info(entry_time_str: str, exit_time_str: str) -> tuple[int, int]:
    """Return the parking duration in minutes and the corresponding fee.

    The application accepts times for one calendar day. Therefore an exit
    time equal to or earlier than the entry time is rejected instead of being
    interpreted as the following day.
    """
    entry_time = parse_time(entry_time_str)
    exit_time = parse_time(exit_time_str)

    if exit_time <= entry_time:
        raise ValueError("출차 시간은 입차 시간보다 이후여야 합니다.")

    duration_minutes = int((exit_time - entry_time).total_seconds() // 60)

    if duration_minutes < FREE_MINUTES:
        return duration_minutes, 0

    paid_minutes = duration_minutes - FREE_MINUTES
    fee = math.ceil(paid_minutes / UNIT_MINUTES) * UNIT_FEE
    return duration_minutes, min(fee, MAX_FEE)
