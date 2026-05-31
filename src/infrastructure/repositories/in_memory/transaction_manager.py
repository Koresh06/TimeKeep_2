from src.domain.interfaces.transaction_manager import ITransactionManager


class InMemoryTransactionManager(ITransactionManager):
    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass
