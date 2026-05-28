from typing import Protocol

from src.domain.entities.day_off import DayOff
from src.domain.entities.user import User
from src.domain.entities.organization import Organization



class IDocumentGenerator(Protocol):
    async def generate_day_off_document(
    self,
        day_off: DayOff,
        user: User,
        organization: Organization,
        boss: User,
    ) -> bytes:
        ...