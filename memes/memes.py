from redbot.core import commands
import asyncio
import aiohttp
import discord
import urllib.parse
import http.client


class Memes(commands.Cog):
    """Retreive the dankest memes Reddit has to offer, and some other stuff"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command(aliases=['meme', 'dankmeme'])
    async def memes(self, ctx):
        """Get the dankest memes Reddit has to offer. Soon, you'll be able to specify by subreddit and number of memes"""
        async with aiohttp.ClientSession() as session:
            url = "https://meme-api.herokuapp.com/gimme"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title= response['title'],
                url = response['postLink'],
                color = embedColor,
            )
            embed.set_image(url=response['url'])
            embed.set_footer(text=f"r/{response['subreddit']} | Requested by {ctx.author.name} | Enjoy your dank memes!")
            await ctx.send(embed=embed)
    @commands.command()
    async def supreme(self, ctx, *, text:str):
        """Make text look like the Supreme logo. If your text is multiple words, please put in double quotes"""
        query = urllib.parse.quote(text)
        embedColor = await ctx.embed_colour()
        embed = discord.Embed(
           color = embedColor,
        )
        embed.set_image(url=f"https://api.alexflipnote.dev/supreme?text={query}")
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
    @commands.command(aliases=['cn', 'chuck'])
    async def chucknorris(self, ctx):
        """Get a random Chuck Norris joke."""
        async with aiohttp.ClientSession() as session:
            url = "https://api.chucknorris.io/jokes/random"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = "Voilà! A Chuck Norris joke!",
                url = response['url'],
                color = embedColor,
                description = response['value']
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
    @comamnds.command(aliases=['txkcd', 'todaysxkcd'])
    async def todayxkcd(self, ctx):
        """Get the day's XKCD comic."""
        async with aiohttp.ClientSession() as session:
            url = "https://xkcd.com/info.0.json"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = response['safe_title'],
                url = f"xkcd.com/{response['num']},
                color = embedColor,
                description = f"XKCD #{response['num']}"
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
