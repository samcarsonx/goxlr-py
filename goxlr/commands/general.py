class GeneralCommands:
    async def ping(self):
        """
        Pings the GoXLR Utility daemon
        """
        return await self.send("Ping")

    async def get_status(self):
        return await self.send("GetStatus")
