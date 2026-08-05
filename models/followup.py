from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Followup:
    """
    Follow-up model for Property Broker CRM
    """

    client_id: int

    followup_date: date

    followup_time: Optional[time] = None

    followup_type: str = "Phone Call"

    discussion_notes: str = ""

    next_followup_date: Optional[date] = None

    reminder: bool = True

    status: str = "Pending"