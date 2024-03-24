class AiohttpSessionBuilder:
    def __init__(self):
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()