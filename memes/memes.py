from redbot.core import commands
import asyncio
import aiohttp
import discord
import urllib.parse
import http.client
import time


class Memes(commands.Cog):
    """Retreive the dankest memes Reddit has to offer, and some other stuff"""
    automeme_pairs = {}
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(aliases=['meme', 'dankmeme'])
    async def memes(self, ctx):
        """Get the dankest memes Reddit has to offer. Soon, you'll be able to specify by subreddit and number of memes"""
        api_key = await self.bot.get_shared_api_tokens("ksoftsi")
        if api_key.get("api_key") is None:
            await ctx.send('The API key is not set. Set it with `set api ksoftsi api_key <your_api_key_here>`')
        else: 
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ksoft.si/images/random-meme', headers={"Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                    response = await resp.json()
                embedColor = await ctx.embed_colour()
                embed = discord.Embed(
                    title = response['title'],
                    url = response['source'],
                    color = embedColor,
                    description = f"{response['author']} | Can't see the image? [Click Here.]({response['image_url']})"
                )
                embed.set_footer(text=f"{response['upvotes']} 👍 | {response['comments']} 💬")
                embed.set_image(url=response['image_url'])
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

    @commands.command(aliases=['txkcd', 'todaysxkcd'])
    async def todayxkcd(self, ctx):
        """Get the day's XKCD comic."""
        async with aiohttp.ClientSession() as session:
            url = "https://xkcd.com/info.0.json"
            async with session.get(url) as response:
                response = await response.json()
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = response['safe_title'],
                url = f"https://xkcd.com/{response['num']}",
                color = embedColor,
                description = f"XKCD #{response['num']}"
            )
            embed.set_image(url=response['img'])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def automeme(self, ctx, delay:int):
        """Tired of manually typing in the `meme` command automatically? Use automeme in the channel you want memes to be posted, and the will automatically be delivered from Reddit."""
        channelID = ctx.channel.id
        if delay < 20:
            await ctx.send('Due to ratelimits placed on my bot, the delay must be over 20 secs. Thanks!')
        else:
            self.automeme_pairs[channelID]=delay
            while channelID in self.automeme_pairs:
                api_key = await self.bot.get_shared_api_tokens("ksoftsi")
                if api_key.get("api_key") is None:
                    await ctx.send('The API key is not set. Set it with `[p]set api ksoftsi api_key <your_api_key_here>`')
                else: 
                    async with aiohttp.ClientSession() as session:
                        async with session.get('https://api.ksoft.si/images/random-meme', headers={"Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                            response = await resp.json()
                        embedColor = await ctx.embed_colour()
                        embed = discord.Embed(
                            title = response['title'],
                            url = response['source'],
                            color = embedColor,
                            description = f"{response['author']} | Can't see the image? [Click Here.]({response['image_url']})"
                        )
                        embed.set_footer(text=f"{response['upvotes']} 👍 | {response['comments']} 💬")
                        embed.set_image(url=response['image_url'])
                        await ctx.send(embed=embed)
                await asyncio.sleep(self.automeme_pairs[channelID])

    @automeme.command()
    async def toggle(self, ctx):
        """Please use this in the channel automeme was set up in. If you do not, then the toggle command will not work. Thanks!"""
        toggleID = ctx.channel.id
        if toggleID in self.automeme_pairs:
            del self.automeme_pairs[ctx.channel.id]
            await ctx.send(f"Automeme succesfuly turned off for <#{toggleID}>")
        else:
            await ctx.send("An unexpected error occurred. Are you sure automeme was set up for this channel?")
    @commands.command()
    async def wikihow(self, ctx):
        """Get a random Wikihow meme"""
        api_key = await self.bot.get_shared_api_tokens("ksoftsi")
        if api_key.get("api_key") is None:
            await ctx.send('The API key is not set. Set it with `[p]set api ksoftsi api_key <your_api_key_here>`')
        else: 
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ksoft.si/images/random-wikihow', headers={"Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                    response = await resp.json()
                embedColor = await ctx.embed_colour()
                embed = discord.Embed(
                    title = response['title'],
                    url = response['article_url'],
                    color = embedColor,
                    description = f"Can't see the image? [Click Here.]({response['url']})"
                )
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discrimator}")
                embed.set_image(url=response['url'])
                await ctx.send(embed=embed)
    @commands.command()
    async def pornhub(self, ctx, text1, text2):
        """Make text look like the pornhub logo."""
        embedColor = await ctx.embed_colour()
        embed = discord.Embed(
            color = embedColor
        )
        embed.set_image(url=f"https://api.alexflipnote.dev/pornhub?text={text1}&text2={text2}")
        await ctx.send(embed=embed)
