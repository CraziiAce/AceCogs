from redbot.core import commands
import asyncio
import aiohttp
import discord

class Music(commands.Cog):
    """Get info about musicians/songs"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command()
    async def lyrics(self, ctx, *, song_name:str):
        """Get the lyrics of a specified song."""
        api_key = await self.bot.get_shared_api_tokens("ksoftsi")
        if api_key.get("api_key") is None:
                return await ctx.send("The ksoft.si API key has not been set. Please set it with `s!set api ksoftsi <api_key>")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.ksoft.si/lyrics/search', params={
                    "q":song_name
                    }, headers={"Authorization": f"Bearer {api_key.get('api_key')}"}) as resp:
                    response = await resp.json()
                embedColor = await ctx.embed_colour()
                embed = discord.Embed(
                    title = f"{response['data'][0]['name']} by {response['data'][0]['artist']}",
                    color = embedColor,
                    description = response['data'][0]['lyrics']
                )
                embed.set_thumbnail(url=response['data'][0]['album_art'])
                embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by KSoft.SI")
            await ctx.send(embed=embed)
