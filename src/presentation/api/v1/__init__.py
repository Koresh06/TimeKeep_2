from fastapi import FastAPI


def include_router(app: FastAPI) -> None:
    from src.presentation.api.v1.auth import router as auth_router
    from src.presentation.api.v1.user import router as user_router
    from src.presentation.api.v1.organization import router as organization_router
    from src.presentation.api.v1.department import router as department_router
    from src.presentation.api.v1.overtime import router as overtime_router
    from src.presentation.api.v1.day_off import router as day_off_router

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(organization_router)
    app.include_router(department_router)
    app.include_router(overtime_router)
    app.include_router(day_off_router)