from typing import List
from pydantic import BaseModel


# -----------------------------------------------------------------------------
# Response from Kinetik stored as a string
# -----------------------------------------------------------------------------
class WebhookResponse(BaseModel):
    result: str


# -----------------------------------------------------------------------------
# Webhook
# -----------------------------------------------------------------------------
class AlertBaselineItem(BaseModel):
    Unit: str
    Value: int


class AlertValueItem(BaseModel):
    Unit: str
    Value: int


class AlertKeyItem(BaseModel):
    DimensionName: str
    DimensionValue: str


# -----------------------------------------------------------------------------
# Structured payload stored as object type `WebhookData`
# -----------------------------------------------------------------------------
class WebhookData(BaseModel):
    EventType: str
    CompanyID: str
    MitigationID: int
    AlarmID: str
    AlarmState: str
    PolicyID: str
    ThresholdID: str
    ActivateSeverity: str
    AlarmStart: str
    AlarmEnd: str
    LastActivate: str
    AlertPolicyName: str
    AlertKey: List[AlertKeyItem]
    AlertValue: AlertValueItem
    AlertBaseline: AlertBaselineItem
    AlertBaselineSource: str
