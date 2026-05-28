from dishka import Scope, provide, Provider

from src.application.mediator import Mediator
from src.application.use_cases.auth.login import LoginCommand, LoginUseCase
from src.application.use_cases.auth.register import RegisterUserCommand, RegisterUserUseCase
from src.application.use_cases.day_off.get_all import GetAllDayOffsUseCase, GetAllDayOffsQuery
from src.application.use_cases.day_off.get_by_id import GetByIdDayOffQuery, GetByIdDayOffUseCase
from src.application.use_cases.day_off.moderate import ModerateDayOffCommand, ModerateDayOffUseCase
from src.application.use_cases.day_off.take import TakeDayOffCommand, TakeDayOffUseCase
from src.application.use_cases.department.create import CreateDepartmentCommand, CreateDepartmentUseCase
from src.application.use_cases.department.get_all import GetAllDepartmentQuery, GetAllDepartmentUseCase
from src.application.use_cases.department.get_by_id import GetDepartmentQuery, GetDepartmentUseCase
from src.application.use_cases.document.generate_report import GenerateReportCommand, GenerateReportUseCase
from src.application.use_cases.organization.create import CreateOrganizationCommand, CreateOrganizationUseCase
from src.application.use_cases.organization.get_all import GetAllOrganizationQuery, GetAllOrganizationUseCase
from src.application.use_cases.organization.get_by_id import GetOrganizationQuery, GetOrganizationUseCase
from src.application.use_cases.overtime.create import CreateOvertimeCommand, CreateOvertimeUseCase
from src.application.use_cases.overtime.delete import DeleteOvertimeRequest, DeleteOvertimeUseCase
from src.application.use_cases.overtime.get_all import GetAllOvertimesQuery, GetAllOvertimesUseCase
from src.application.use_cases.overtime.get_by_id import GetByIdOvertimeQuery, GetByIdOvertimeUseCase
from src.application.use_cases.user.activate_user import ActivateUserCommand, ActivateUserUseCase
from src.application.use_cases.user.delete import DeleteUserRequest, DeleteUserUseCase
from src.application.use_cases.user.get_all import GetAllUsersQuery, GetAllUsersUseCase
from src.application.use_cases.user.get_by_id import GetUserByIdQuery, GetByIdUserUseCase
from src.application.use_cases.user.update_role import UpdateUserRoleCommand, UpdateUserRoleUseCase
from src.application.use_cases.user.update_work_mode import UpdateUserWorkModeCommand, UpdateUserWorkModeUseCase


class ApplicationProvider(Provider):
    
    register_use_case = provide(RegisterUserUseCase, scope=Scope.REQUEST)
    login_use_case = provide(LoginUseCase, scope=Scope.REQUEST)

    get_by_id_user_use_case = provide(GetByIdUserUseCase, scope=Scope.REQUEST)
    get_all_users_use_case = provide(GetAllUsersUseCase, scope=Scope.REQUEST)
    delete_user_use_case = provide(DeleteUserUseCase, scope=Scope.REQUEST)
    active_user_use_case = provide(ActivateUserUseCase, scope=Scope.REQUEST)
    update_user_role_use_case = provide(UpdateUserRoleUseCase, scope=Scope.REQUEST)
    update_user_work_mode_use_case = provide(UpdateUserWorkModeUseCase, scope=Scope.REQUEST)

    create_department_use_case = provide(CreateDepartmentUseCase, scope=Scope.REQUEST)
    get_departmnet_use_case = provide(GetDepartmentUseCase, scope=Scope.REQUEST)
    get_all_departments_use_case = provide(GetAllDepartmentUseCase, scope=Scope.REQUEST)

    create_organization_use_case = provide(CreateOrganizationUseCase, scope=Scope.REQUEST)
    get_organization_use_case = provide(GetOrganizationUseCase, scope=Scope.REQUEST)
    get_all_organizations_use_case = provide(GetAllOrganizationUseCase, scope=Scope.REQUEST)

    create_overtime_use_case = provide(CreateOvertimeUseCase, scope=Scope.REQUEST)
    get_by_id_overtime_use_case = provide(GetByIdOvertimeUseCase, scope=Scope.REQUEST)
    get_all_overtimes_use_case = provide(GetAllOvertimesUseCase, scope=Scope.REQUEST)
    delete_overtime_use_case = provide(DeleteOvertimeUseCase, scope=Scope.REQUEST)

    get_all_day_offs_use_case = provide(GetAllDayOffsUseCase, scope=Scope.REQUEST)
    get_by_id_day_off_use_case = provide(GetByIdDayOffUseCase, scope=Scope.REQUEST)
    take_day_off_use_case = provide(TakeDayOffUseCase, scope=Scope.REQUEST)
    moderate_day_off_use_case = provide(ModerateDayOffUseCase, scope=Scope.REQUEST)

    generate_report_use_case = provide(GenerateReportUseCase, scope=Scope.REQUEST)

    
    @provide(scope=Scope.REQUEST)
    def get_mediator(
        self,
        register: RegisterUserUseCase,
        login: LoginUseCase,

        get_by_id_user: GetByIdUserUseCase,
        get_all_users: GetAllUsersUseCase,
        delete_user: DeleteUserUseCase,
        active_user: ActivateUserUseCase,
        update_user_role: UpdateUserRoleUseCase,
        update_user_work_mode: UpdateUserWorkModeUseCase,

        create_department: CreateDepartmentUseCase,
        get_department: GetDepartmentUseCase,
        get_all_departments: GetAllDepartmentUseCase,

        create_organization: CreateOrganizationUseCase,
        get_organization: GetOrganizationUseCase,
        get_all_organizations: GetAllOrganizationUseCase,

        create_overtime: CreateOvertimeUseCase,
        get_by_id_overtime: GetByIdOvertimeUseCase,
        get_all_overtimes: GetAllOvertimesUseCase,
        delete_overtime: DeleteOvertimeUseCase,

        get_all_day_offs: GetAllDayOffsUseCase,
        get_by_id_day_off: GetByIdDayOffUseCase,
        take_day_off: TakeDayOffUseCase,
        moderate_day_off: ModerateDayOffUseCase,

        generate_report: GenerateReportUseCase,
    ) -> Mediator:
        mediator = Mediator()
        mediator.register(RegisterUserCommand, register)
        mediator.register(LoginCommand, login)
        
        mediator.register(GetUserByIdQuery, get_by_id_user)
        mediator.register(GetAllUsersQuery, get_all_users)
        mediator.register(DeleteUserRequest, delete_user)
        mediator.register(ActivateUserCommand, active_user)
        mediator.register(UpdateUserRoleCommand, update_user_role)
        mediator.register(UpdateUserWorkModeCommand, update_user_work_mode)

        mediator.register(CreateDepartmentCommand, create_department)
        mediator.register(GetDepartmentQuery, get_department)
        mediator.register(GetAllDepartmentQuery, get_all_departments)

        mediator.register(CreateOrganizationCommand, create_organization)
        mediator.register(GetOrganizationQuery, get_organization)
        mediator.register(GetAllOrganizationQuery, get_all_organizations)

        mediator.register(CreateOvertimeCommand, create_overtime)
        mediator.register(GetByIdOvertimeQuery, get_by_id_overtime)
        mediator.register(GetAllOvertimesQuery, get_all_overtimes)
        mediator.register(DeleteOvertimeRequest, delete_overtime)

        mediator.register(GetAllDayOffsQuery, get_all_day_offs)
        mediator.register(GetByIdDayOffQuery, get_by_id_day_off)
        mediator.register(TakeDayOffCommand, take_day_off)
        mediator.register(ModerateDayOffCommand, moderate_day_off)

        mediator.register(GenerateReportCommand, generate_report)

        
        return mediator