import os
from aiograpi import Client

SESSION_ID = os.getenv("SESSION_ID")

# ""

class InstaClient:
    def __init__(self):
        self.client = Client()

class InstaClient:
    def __init__(self):
        self.client = Client()

    async def connect(self):
        await self.client.login_by_sessionid(SESSION_ID)

        print("✅ Instagram logged in successfully")

        return self.client