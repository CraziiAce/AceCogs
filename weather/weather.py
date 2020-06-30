from redbot.core import commands
import aiohttp
import asyncio
import json
import discord
import datetime

class Weather(commands.Cog):
    """Get the day's weather or other information"""
    us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.group()
    async def weather(self, ctx):
        """Get the weather of a specified area"""
        pass
    @weather.command()
    async def zip(self, ctx, zip_code:str):
        """Get the weather of a city/town by its zip code"""
        # Code:
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip_code + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
            async with session.get(url) as response:
                weather_response = await response.json()
                localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                localTimeUnix = weather_response['dt'] + weather_response['timezone']
                localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
            embed = discord.Embed(
                    title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                    description=weather_response['weather'][0]['description'],
                    color=0x0276FD,
            )
            embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
            embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
            embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
            embed.set_footer(text='Starry | discord.gg/7mSqpXN', icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
            await ctx.send(embed=embed)
    @weather.command()
    async def city(self, ctx, city_name:str, state_code='NA'):
        """Get the weather of a city/town by its name. State code is US only."""
        # Code:
        if state_code == 'NA':
            async with aiohttp.ClientSession() as session:
                url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
                async with session.get(url) as response:
                    weather_response = await response.json()
                    localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                    sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                    localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                    sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                    localTimeUnix = weather_response['dt'] + weather_response['timezone']
                    localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                embed = discord.Embed(
                        title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                        description=weather_response['weather'][0]['description'],
                        color=0x0276FD,
                )
                embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                embed.set_footer(text='Starry | discord.gg/7mSqpXN', icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                await ctx.send(embed=embed)
        if state_code != 'NA':
            async with aiohttp.ClientSession() as session:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},{us_state_abbrev[state_code]}&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
                    async with session.get(url) as response:
                        weather_response = await response.json()
                        if weather_response['message']="city not found":
                            await ctx.send("An error ocurred: city not found. Please make sure you put in the full state name.")
                            pass
                        localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                        sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                        localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                        sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                        localTimeUnix = weather_response['dt'] + weather_response['timezone']
                        localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                    embed = discord.Embed(
                            title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                            description=weather_response['weather'][0]['description'],
                            color=0x0276FD,
                    )
                    embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text='Starry | discord.gg/7mSqpXN', icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    await ctx.send(embed=embed)
