from redbot.core import commands

from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

import discord
import aiohttp
import logging

log = logging.getLogger("red.acecogs.news")

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
        us_state_abbrev = {
            'Poland': 'pl',
            'US': 'us',
            'Britain': 'gb',
            'br': 'gb',
            'England': 'gb',
            'Wales': 'gb',
            'Scotland': 'gb',
        }
        if category:        
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.news_base_url}/top-headlines?country={country}&category={category}&pagesize=100', headers={
                    "Authorization":f"Bearer {key.get('key')}"
                }) as resp:
                    resp = await resp.json()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.news_base_url}/top-headlines?country={country}&pagesize=100', headers={
                    "Authorization":f"Bearer {key.get('key')}"
                }) as resp:
                    resp = await resp.json()
        if resp['status'] != 'ok':
            await ctx.send(f"An unexpected error occured: {resp['code']}. {resp['message']}")
            return
        if resp['totalResults'] == 0:
            await ctx.send("It looks like that country/category is invalid.")
            return
        embeds = []
        try:
            while len(embeds) < resp["totalResults"]:
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
            if len(embeds) == resp["totalResults"]:
                await menu(
                    ctx,
                    pages=embeds,
                    controls=DEFAULT_CONTROLS,
                    message=None,
                    page=0,
                    timeout=30,
                )
            log.debug(f"A news embed with {len(embeds)} pages has been sent.")
        except discord.errors.HTTPException:
            await ctx.send("An unexpected error occurred. This usually means that the API returned an invalid image url")
            log.debug("The news API returned an invalid image!")
