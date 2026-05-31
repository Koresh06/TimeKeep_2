from dataclasses import dataclass

from src.domain.entities.day_off import DayOff
from src.domain.entities.department import Department
from src.domain.entities.organization import Organization
from src.domain.entities.user import User


@dataclass(frozen=True)
class DocumentDTO:
    # данные руководителя
    boss_position: str
    boss_rank: str
    boss_full_name: str
    
    # данные организации
    organization_name_genitive: str
    
    # данные отгула
    date_report: str
    date_day_off: str
    info_overtimes: str
    
    # данные сотрудника
    position_user: str
    department_user: str
    rank_user: str
    full_name_user: str

    @classmethod
    def build(
        cls,
        day_off: DayOff,
        user: User,
        organization: Organization,
        boss: User,
        department: Department,
    ) -> "DocumentDTO":
        return cls(
            boss_position=boss.position,
            boss_rank=boss.rank,
            boss_full_name=f"{boss.surname} {boss.first_name[0]}.{boss.patronymic[0]}.",
            organization_name_genitive=organization.name_genitive,
            date_report=day_off.created_at.strftime("%d.%m.%Y"),
            date_day_off=day_off.date_.strftime("%d.%m.%Y"),
            info_overtimes=day_off.format_overtimes_for_document(),
            position_user=user.position,
            department_user=department.name,
            rank_user=user.rank,
            full_name_user=f"{user.surname} {user.first_name[0]}.{user.patronymic[0]}.",
        )