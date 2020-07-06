from redbot.core import commands
import asyncio
import aiohttp
import discord

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
            embed.set_footer(text=f"r/{response['subreddit']} | Enjoy your dank memes!")
            await ctx.send(embed=embed)
    @commands.command()
    async def supreme(self, ctx, text):
        """Make text look like the Supreme logo. If your text is multiple words, please put in double quotes"""
        embedColor = await ctx.embed_colour()
        embed = discord.Embed(
            color = embedColor,
        )
        embed.set_image(url=f"https://api.alexflipnote.dev/supreme?text={text}")
        embed.set_footer(text=f"Requested by <@!{ctx.author.id}")
        await ctx.send(embed=embed)
