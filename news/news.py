from redbot.core import commands

from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

import discord
import aiohttp

class News(commands.Cog):
    """Get whats happening in the world right from Discord."""
    news_base_url='https://newsapi.org/v2'
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command()
    async def news(self, ctx, country:str, category:str = None):
        """Get the current news. Country must be two letters, e.g \'us\' or \'fr\'"""
        key = await self.bot.get_shared_api_tokens("newsapi")
        if not key.get("key"):
            await ctx.send("Please set the api key with `[p]set api newsapi key <your key> Go to https://newsapi.org if you need a key.")
            return
        if category:        
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.news_base_url}/top-headlines?country={country}&category={category}', headers={
                    "Authorization":f"Bearer {key.get('get')}"
                }) as resp:
                    resp = await resp.json()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.news_base_url}/top-headlines?country={country}', headers={
                    "Authorization":f"Bearer {key.get('key')}"
                }) as resp:
                    resp = await resp.json()
        embeds = []
        await ctx.send(f"Num of embeds: {len(embeds)}\nResults: {resp['totalResults']}")
        while len(embeds) < resp["totalResults"] - 2:
            embed = discord.Embed()
            embed.title = (resp['articles'][len(embeds)]['title'])
            embed.url = resp['articles'][len(embeds)]["url"]

            embed.description = (resp['articles'][len(embeds)]['description'])

            embed.set_footer(
                text=(
                    f"By {resp['articles'][len(embeds)]['author']} for {resp['articles'][len(embeds)]['source']['name']}"
                )
            )

            embed.set_thumbnail(
                url=(
                    resp['articles'][len(embeds)]['urlToImage']
                )
            )
            embeds.append(embed)
            await ctx.send(f"paginated page {len(embeds)}")
        if len(embeds) == resp["totalResults"]:
            await menu(
                ctx,
                pages=embeds,
                controls=DEFAULT_CONTROLS,
                message=None,
                page=0,
                timeout=30,
            )