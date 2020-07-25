
from redbot.core import checks, commands
import asyncio
import aiohttp
import discord

class Finance(commands.Cog):
    """Get info about stocks/currencies/businesses"""
    finnhub_base_url='https://finnhub.io/api/v1/'
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command()
    async def stock(self, ctx, *, stock_ticker:str):
        """Get the price of a US stock."""
        api_key = await self.bot.get_shared_api_tokens("finnhub")
        if api_key.get("api_key") is None:
                return await ctx.send("The Finnhub API key has not been set. Please set it with `s!set api finnhub api_key <your api key>`")
        else:
            stock_ticker.upper()
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.finnhub_base_url}quote?symbol={stock_ticker}&') as resp:
                    response = await resp.json()
                if response == '{}':
                    await ctx.send('An unexpected error occured. Are you sure that is a valid, *US* stock ticker?')
                percentage_change_a = response['c'] / response['o']
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
                    embed.add_field(name='Prices', value=f"Open: ${response['o']}\nHigh: ${response['h']}\nLow: ${response['l']}\nCurrent: ${response['c']}\nPercentage Gain: <:up_arrow:736390019136356442> %{percentage_change_final}")
                if not percentage_gain:
                     embed.add_field(name='Prices', value=f"Open: ${response['o']}\nHigh: ${response['h']}\nLow: ${response['l']}\nCurrent: ${response['c']}\nPercentage Loss: <:down_arrow:736390163839844422> %{percentage_change_final}")
                embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by finnhub.io")
            await ctx.send(embed=embed)
