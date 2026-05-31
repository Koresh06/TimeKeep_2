from src.presentation.di.providers.application import ApplicationProvider
from src.presentation.di.providers.cache import CacheProvider
from src.presentation.di.providers.config import ConfigProvider
from src.presentation.di.providers.infrastructure import InfrastructureProvider


def make_base_providers():
    return (
        ConfigProvider(),
        InfrastructureProvider(),
        CacheProvider(),
        ApplicationProvider(),
    )
