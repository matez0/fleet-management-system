from pydantic import BaseModel

ROUTING_KEY_PENALTY = 'fms.penalty'


class PenaltyMessage(BaseModel):
    driverId: str
    points: int
