from redbot.core import commands
import asyncio
import aiohttp
import discord
import urllib.parse

class Animals(commands.Cog):
    """get some random images."""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command(aliases = ['doggo', 'dogg', 'pupper'])
    async def dog(self, ctx):
        """Get a picture of a cute doggo."""
        async with aiohttp.ClientSession() as session:
            url = "https://dog.ceo/api/breeds/image/random"
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send(f'Sorry, but an unexpected error occured with error code `{response.status}`. This could mean the API is rejecting our request.')
                    return
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = "Voilà! A random dog!",
                color = embedColor,
            )
            embed.set_image(url=response['message'])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
    @commands.command()
    async def fox(self, ctx):
        """Get a picture of a cute fox."""
        async with aiohttp.ClientSession() as session:
            url = "https://randomfox.ca/floof/"
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send(f'Sorry, but an unexpected error occured with error code `{response.status}`. This could mean the API is rejecting our request.')
                    return
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = "Voilà! A random fox!",
                color = embedColor,
            )
            embed.set_image(url=response['image'])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
    @commands.command(aliases=['randomaww', 'cuterandom'])
    async def randomcute(self, ctx):
        """Get a random cute image"""
        api_key = await self.bot.get_shared_api_tokens("ksoftsi")
        if api_key.get("api_key") is None:
            await ctx.send('The API key is not set. Set it with `set api ksoftsi api_key <your_api_key_here>`')
        else: 
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ksoft.si/images/random-aww', headers={
                    "Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                    if resp.status != 200:
                        await ctx.send(f'Sorry, but an unexpected error occured with error code `{resp.status}`. This could mean the API is rejecting our request.')
                        return
                    response = await resp.json()
                embedColor = await ctx.embed_colour()
                embed = discord.Embed(
                    title = response['title'],
                    url = response['source'],
                    color = embedColor,
                    description = f"{response['author']} | Can't see the image? [Click Here.]({response['image_url']}) | from {response['subreddit']}"
                )
                embed.set_footer(text=f"{response['upvotes']} 👍 | {response['comments']} 💬")
                embed.set_image(url=response['image_url'])
                await ctx.send(embed=embed)
    @commands.command()
    async def reddit(self, ctx, subreddit:str):
        """Get random images from a subreddit. I know this technically doesn't belong in this cog, but oh well.\nPlease don't include the `r/` infront of the subreddit name."""
        api_key = await self.bot.get_shared_api_tokens("ksoftsi")
        if api_key.get("api_key") is None:
            await ctx.send('The API key is not set. Set it with `set api ksoftsi api_key <your_api_key_here>`')
        else: 
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.ksoft.si/images/rand-reddit/{subreddit}", params={
                    "remove_nsfw": "True"
                    }, headers={"Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                    if resp.status != 200:
                        await ctx.send(f'Sorry, but an unexpected error occured with error code `{resp.status}`. This could mean the API is rejecting our request, or the subreddit is invalid/nsfw.')
                        return
                    response = await resp.json()
                embedColor = await ctx.embed_colour()
                embed = discord.Embed(
                    title = response['title'],
                    url = response['source'],
                    color = embedColor,
                    description = f"{response['author']} | Can't see the image? [Click Here.]({response['image_url']}) | from {response['subreddit']}"
                )
                embed.set_footer(text=f"{response['upvotes']} 👍 | {response['comments']} 💬")
                embed.set_image(url=response['image_url'])
                await ctx.send(embed=embed)
