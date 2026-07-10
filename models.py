from enum import StrEnum
from pydantic import BaseModel


class CallerType(StrEnum):
    STANDARD_CUSTOMER = "standard_customer"
    WARRANTY_CUSTOMER = "warranty_customer"
    WARRANTY_REP = "warranty_rep"
    SPAM = "spam"


class CallSummary(BaseModel):
    caller_type: CallerType

    caller_name: str | None = None
    callback_phone: str | None = None
    service_address: str | None = None

    appliance_type: str | None = None
    appliance_issue: str | None = None
    appliance_brand: str | None = None

    company_name: str | None = None
    call_outcome: str | None = None
