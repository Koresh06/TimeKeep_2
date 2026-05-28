from dishka import Scope, provide, Provider
from src.core.config import AppSettings, settings
from src.core.config.database import PostgresSettings
from src.core.config.security import SecuritySettings


class ConfigProvider(Provider):
    
    @provide(scope=Scope.APP)
    def get_settings(self) -> AppSettings:
        return settings
    
    @provide(scope=Scope.APP)
    def get_security_settings(self, s: AppSettings) -> SecuritySettings:
        return s.security
    
    @provide(scope=Scope.APP)
    def get_db_settings(self, s: AppSettings) -> PostgresSettings:
        return s.db