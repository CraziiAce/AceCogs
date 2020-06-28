from redbot.core import commands
import aiohttp
import asyncio

class Weather(commands.Cog):
    """Get the day's weather"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def weather(self, ctx, zip_code: str):
        """Get the weather of a city/town by its zip code"""
        # Code:
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip_code + "&appid=168ced82a72953d81d018f75eec64aa0"
            async with session.get(url) as response:
                await ctx.send(await "Longitude:" + response.text.coord.lon() + "\nLatitude:" + response.text.coord.lat())
