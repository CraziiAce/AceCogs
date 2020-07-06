from redbot.core import commands
import asyncio
import aiohttp
import discord
import urllib.parse

class Animals(commands.Cog):
    """much amaze. very cute. so fur"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command(aliases = ['catto', 'cato', 'gato'])
    async def cat(self, ctx):
        """Get a picture of a cute cat."""
        async with aiohttp.ClientSession() as session:
            url = "https://aws.random.cat/meow"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = "Voilà! A random cat!",
                color = embedColor,
            )
            embed.set_image(url=response['url'])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
    @commands.command(aliases = ['doggo', 'dogg', 'pupper'])
    async def dog(self, ctx):
        """Get a picture of a cute doggo."""
        async with aiohttp.ClientSession() as session:
            url = "https://aws.random.cat/meow"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = "Voilà! A random dog!",
                color = embedColor,
            )
            embed.set_image(url=response['url'])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
