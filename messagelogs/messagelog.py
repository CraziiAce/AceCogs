from redbot.core import commands
import discord


class MessageLog(commands.Cog):
    """Log all the messages sent."""
    message_log_pairs = {}
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=['messagelogs', 'logmessages', 'logmessage'])
    async def messagelog(self, ctx):
        """Tired of looking in audit logs if someone deleted a vulgar message? Use this in the channel you would like messages to be logged in, and they will all be logged."""
        guildID = ctx.guild.id
        channelID = ctx.channel.id
        self.message_log_pairs[guildID]=channelID


    @commands.Cog.listener() 
    async def on_message_without_command(self, message):
        if message.guild.id in self.message_log_pairs
            embedColor = await ctx.embed_colour()
            embed = discord.Embed(
                title = 'Message Sent',
                description = f'Content: {message.content}',
                color = embedColor,
            )
            embed.set_thumbnail(url=response['url'])
            embed.set_footer(text=f"Sent by {message.author.name}", icon_url=message.author.avatar_url)
            await self.message_log_pairs[message.guild.id].send(embed=embed)



    @messagelogs.command()
    async def toggle(self, ctx):
        """Please use this in the channel message logs were set up in. If you do not, then the toggle command will not work. Thanks!"""
        toggleID = ctx.guild.id
        if toggleID in self.message_log_pairs:
            del self.message_log_pairs[ctx.guild.id]
            await ctx.send(f"Message logs succesfuly turned off.")
        else:
            await ctx.send("An unexpected error occurred. Are you sure message logs were set up for this channel?")
