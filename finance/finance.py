from redbot.core import checks, commands, errors
import asyncio
import aiohttp
import discord

class Finance(commands.Cog):
    """Get info about stocks/currencies/businesses"""
    iex_base_url='https://cloud.iexapis.com/stable/'
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command()
    async def stock(self, ctx, *, stock_ticker:str):
        """Get the price of a US stock."""
        token = await self.bot.get_shared_api_tokens("iex")
        if token.get("token") is None:
                return await ctx.send("The IEX API key has not been set. Please set it with `s!set api iex token <your token>`")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.iex_base_url}stock/{stock_ticker}/book?token={token.get("token")}', params={
                    "format":"json"
                }) as resp:
                    response = await resp.json()
                if response == '{}':
                    await ctx.send('An unexpected error occured. Are you sure that is a valid, *US* stock ticker?')
                percentage_change_a = response['quote']['latestPrice'] / response['quote']['open']
                percentage_change_b = percentage_change_a - 1
                percentage_change_final = percentage_change_b * 100
                embedColor = await ctx.embed_colour()
                percentage_gain = True
                if percentage_change_final < 0:
                    percentage_gain = False
                embed = discord.Embed(
                    title = f"Stock Data for {response['quote']['companyName']}",
                    color = embedColor,
                )
                if percentage_gain:
                    embed.add_field(name='Prices', value=f"Open: ${response['quote']['open']}\nHigh: ${response['quote']['high']}\nLow: ${response['quote']['low']}\nCurrent: ${response['quote']['latestPrice']}\nPercentage Gain: <:up_arrow:736390019136356442> %{percentage_change_final}")
                if not percentage_gain:
                    embed.add_field(name='Prices', value=f"Open: ${response['quote']['open']}\nHigh: ${response['quote']['high']}\nLow: ${response['quote']['low']}\nCurrent: ${response['quote']['latestPrice']}\nPercentage Loss: <:down_arrow:736390163839844422> %{percentage_change_final}")
                embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by IEX Cloud")
            await ctx.send(embed=embed)
    @commands.command(aliases=['companyprofile', 'cprofile', 'companyinfo'])
    async def company(self, ctx, stock_ticker:str):
        """Get information about a publicly traded company."""
        token = await self.bot.get_shared_api_tokens("iex")
        if token.get("token") is None:
                return await ctx.send("The IEX API key has not been set. Please set it with `s!set api iex token <your token>`")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.iex_base_url}stock/{stock_ticker}/company?token={token.get("token")}', params={
                    "format":"json"
                }) as resp:
                    response = await resp.json()
                if resp.status != 200:
                    await ctx.send(f'Sorry, but an unexpected error occured with error code `{resp.status}`. This could mean the API is rejecting our request, or the stock ticker is invalid.')
                else:
                    if not response['companyName']:
                        await ctx.send('Sorry, but I could not find data for that company')
                    else:
                        embedColor = await ctx.embed_colour()
                        embed = discord.Embed(
                            title = f"Company Data for {response['companyName']}",
                            color = embedColor,
                            description = f"{response['description']}\nTraded on the {response['exchange']}.",
                            url = response['website']
                        )
                        if not response['address2']:
                            embed.add_field(name=f"Company Data for {response['companyName']}", value=f"**CEO:** {response['CEO']}\n**SEC name:** {response['securityName']}\n**Industry:** {response['sector']}\n**Employees:** {response['employees']}\n**Address:** \n{response['companyName']}\n{response['address']}\n{response['city']}, {response['state']} {response['zip']}")
                        await ctx.send(embed=embed)
