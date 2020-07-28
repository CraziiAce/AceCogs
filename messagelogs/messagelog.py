from redbot.core import commands, checks
import discord


class MessageLog(commands.Cog):
    """Log all the messages sent."""
    message_log_pairs = {}
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=['messagelogs', 'logmessages', 'logmessage'])
    @commands.admin()
    @commands.guild_only()
    async def messagelog(self, ctx):
        """Tired of looking in audit logs if someone deleted a vulgar message? Use this in the channel you would like messages to be logged in, and they will all be logged.\nFor larger servers with over 1 message per 10 seconds, *please* don't use this. Reach out to <@!555709231697756160> if this applies to you."""
        guildID = ctx.guild.id
        channelID = ctx.channel.id
        self.message_log_pairs[guildID]=channelID


    @commands.Cog.listener() 
    async def on_message_without_command(self, message):
        if message.guild.id in self.message_log_pairs and message.author.bot == False:
            embed = discord.Embed(
                title = 'Message Sent',
                description = f'Content: {message.content} | [Jump!]({message.jump_url})',
                color = 0x32CD32,
            )
            embed.set_footer(text=f"Sent by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
            channel = self.bot.get_channel(self.message_log_pairs[message.guild.id])
            await channel.send(embed=embed)



    @messagelog.command()
    async def toggle(self, ctx):
        """Please use this in the channel message logs were set up in. If you do not, then the toggle command will not work. Thanks!"""
        toggleID = ctx.guild.id
        if toggleID in self.message_log_pairs:
            del self.message_log_pairs[ctx.guild.id]
            await ctx.send(f"Message logs succesfuly turned off.")
        else:
            await ctx.send("An unexpected error occurred. Are you sure message logs were set up for this channel?")
