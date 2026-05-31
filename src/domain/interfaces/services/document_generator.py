from typing import Protocol

from src.application.dtos.document import DocumentDTO


class IDocumentGenerator(Protocol):
    async def generate_day_off_document(self, dto: DocumentDTO) -> bytes: ...