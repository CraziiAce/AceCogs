from redbot.core import commands
import aiohttp
import asyncio
import json

class Weather(commands.Cog):
    """Get the day's weather or other information"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def weather(self, ctx, zip_code:str):
        """Get the weather of a city/town by its zip code"""
        # Code:
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip_code + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
            async with session.get(url) as response:
                weather_response = await response.json()
            await ctx.send(f"\n__**Geographical info:**__ \nSpecified City: {weather_response['name']}\nLongitude: {weather_response['coord']['lon']}\nLatitude: {weather_response['coord']['lat']}\n__**Temperature**__ Info:\nCurrent Temp: {weather_response['main']['temp']}\nFeels Like: {weather_response['main']['feels_like']}\nDaily High: {weather_response['main']['temp_max']}\nDaily Low: {weather_response['main']['temp_min']}\n__**Wind Info:")
            embed = discord.Embed(
                    title=f"Weather in {weather_response['name']}",
                    description=zip_code,
                    color=0x0276FD,
            )
                    embed.add_field('Location:',f'**City:** {weather_response['name']}\n**Longitude: {weather_response['coord']['lon']}\n **Latitude:** {weather_response['coord']['lat']}', inline=False)
                
