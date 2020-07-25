from redbot.core import checks, commands
import asyncio
import aiohttp
import discord

class Finance(commands.Cog):
    """Get info about stocks/currencies/businesses"""
    tiingo_base_url='https://api.tiingo.com/api/'
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command()
    async def stock(self, ctx, *, stock_ticker:str):
        """Get the price of a US stock."""
        token = await self.bot.get_shared_api_tokens("Tiingo")
        if token.get("token") is None:
                return await ctx.send("The Tiingo API key has not been set. Please set it with `s!set api tiingo token <your token>`")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.tiingo_base_url}iex/{stock_ticker}?token={token.get("token")}') as resp:
                    response = await resp.json()
                if response == '{}':
                    await ctx.send('An unexpected error occured. Are you sure that is a valid, *US* stock ticker?')
                percentage_change_a = response[0]['last'] / response['open']
                percentage_change_b = percentage_change_a - 1
                percentage_change_final = percentage_change_b * 100
                embedColor = await ctx.embed_colour()
                percentage_gain = True
                if percentage_change_final < 0:
                    percentage_gain = False
                embed = discord.Embed(
                    title = f"Stock Data for {stock_ticker}",
                    color = embedColor,
                )
                if percentage_gain:
                    embed.add_field(name='Prices', value=f"Open: ${response[0]['open']}\nHigh: ${response[0]['high']}\nLow: ${response[0]['low']}\nCurrent: ${response[0]['last']}\nPercentage Gain: <:up_arrow:736390019136356442> %{percentage_change_final}")
                if not percentage_gain:
                    embed.add_field(name='Prices', value=f"Open: ${response[0]['open']}\nHigh: ${response[0]['high']}\nLow: ${response[0]['low']}\nCurrent: ${response[0]['last']}\nPercentage Loss: <:down_arrow:736390163839844422> %{percentage_change_final}")
                embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by tiingo.com")
            await ctx.send(embed=embed)
