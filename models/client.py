from dataclasses import dataclass


@dataclass
class Client:

    full_name: str

    mobile: str

    alternate_mobile: str

    email: str

    city: str

    property_type: str

    location_preferred: str

    budget_min: float

    budget_max: float

    source: str

    status: str

    priority: str

    remarks: str