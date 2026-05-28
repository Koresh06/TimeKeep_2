from functools import lru_cache

from fastapi import Depends, HTTPException

from src.domain.enums.role import Role
from src.presentation.dependencies.auth import  UserTokenData, get_current_user


ROLE_HIERARCHY = {
    Role.USER: 0,
    Role.MODERATOR: 1,
    Role.ADMIN: 2,
    Role.SUPER_ADMIN: 3,
}

class RequireRole:
    def __init__(self, min_role: Role) -> None:
        self.min_role = min_role

    async def __call__(
        self,
        current_user: UserTokenData = Depends(get_current_user()),
    ) -> UserTokenData:
        if ROLE_HIERARCHY[current_user.role] < ROLE_HIERARCHY[self.min_role]:
            raise HTTPException(status_code=403, detail="Нет доступа")
        return current_user
    
    
@lru_cache
def get_require_user() -> RequireRole:
    return RequireRole(Role.USER)

@lru_cache
def get_require_moderator() -> RequireRole:
    return RequireRole(Role.MODERATOR)

@lru_cache
def get_require_admin() -> RequireRole:
    return RequireRole(Role.ADMIN)

@lru_cache
def get_require_super_admin() -> RequireRole:
    return RequireRole(Role.SUPER_ADMIN)