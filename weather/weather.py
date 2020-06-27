from redbot.core import commands
import aiohttp
import asyncio

class API(commands.Cog):
    """Interact with various APIs"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def weather(self, ctx, zip_code: int):
        """Get the weather of a city/town by its zip code"""
        # Code:
        return zip_code
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def main():
            async with aiohttp.ClientSession() as session:
                response = await fetch(session, "http://api.openweathermap.org/data/2.5/weather?zip=" + int(zip_code) + "&appid=168ced82a72953d81d018f75eec64aa0")
                await ctx.send(response.content)
