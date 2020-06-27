from redbot.core import commands

class Weather(commands.Cog):
    """Retreive weather for an area based on zip code (us only for now)"""

    @commands.command()
    async def weather(self, ctx, zip_code: [str]):
        """Get the weather of a city/town by its zip code"""
        # Code:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + str(zip_code) + "&appid=168ced82a72953d81d018f75eec64aa0")
        await ctx.send(response.content)