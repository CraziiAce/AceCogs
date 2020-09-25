from redbot.core import commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

import discord, aiohttp

class Skyblock(commands.Cog):
    """Get Hypixel info"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.playerdb_base_url = "https://playerdb.co/api/player/minecraft/"
        self.hypixel_base_url = "https://api.hypixel.net"
        self.key=("0e1271ff-16ca-430f-b53e-8750d9ff683f")


    async def get_uuid(self, username):
        """A bot function to get the uuid of a player"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.playerdb_base_url}{username}"
            async with session.get(url) as resp:
                resp = await resp.json
            return resp

    @commands.group()
    async def skyblock(self, ctx):
        """Get Hypixel Skyblock info"""
        pass

    @commands.group()
    async def hypixel(self, ctx):
        """Get information for Hypixel as a whole"""

    @hypixel.command(aliases=['online', 'isonline'])
    async def status(self, ctx, username):
        key = await self.bot.get_shared_api_tokens("hypixel")
        online = "is not online"
        if key.get("key") is None:
            await ctx.send('You haven\'t set the Hypixel api key yet! You can do this by doing /api in any Hypixel lobby, and then doing `[p]set api hypixel key <your_key>`.')
            
        else:
            uuid = await self.get_uuid(self, username)

            if uuid['code'] != 'player.found':
                await ctx.send(f"Sorry, an unexpected error occured. `{uuid['code']}`")

            else:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.hypixel_base_url}/status?key={key.get('key')}&uuid={uuid['player']['meta']['raw_id']}"
                    async with session.get(url) as resp:
                        resp = await resp.json
                if resp['session']['online'] == True:
                    online = 'is online'
                embed = discord.Embed(
                title = f"{username} {online}",
                color = await ctx.embed_colour()
            )
        
                embed.set_thumbnail(uuid['player']['meta']['avatar'])
                if online == 'is online':
                    embed.add_field(name="Game info", value=f"**Game:** {resp['session']['gameType']}\n**Mode:** {resp['session']['mode']}\n**Map:** {resp['session']['map']}")
