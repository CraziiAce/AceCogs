from redbot.core import commands, checks, Config

import datetime
import discord
class MemberLogs(commands.Cog):
    """Log when members join/leave a server."""\

    def __init(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=7777232377772323, force_registration=True
        )

        self.config.register_guild(channel=None, do_join_logs=True, do_leave_logs=True, join_message=None, leave_message=None, message_channel=None)
    @commands.group()
    @commands.guild_only()
    @commands.admin
    async def memberlog(self, ctx):
        """Log members joining & leaving"""
        pass
    @memberlog.command()
    async def channel(self, ctx, channel:discord.TextChannel = None):
        """Set the channel where member logs will be sent. Use this without a channel to turn off the logs."""
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
        else:
            await self.config.guild(ctx.guild).channel.set(None)
        await ctx.send("User logs successfully turned on.")
    @commands.group()
    @commands.admin
    @commands.guild_only
    async def custommessage(self, ctx):
        """Send a custom message when someone joins/leaves."""
    @custommessage.command
    async def join(self, ctx, join_message:str = None):
        """Set a custom message for users joining the server. If it is left blank, this will be disabled. Use {user} to mention the user that joined the server, and {username} to display the user's username."""
        if join_message:
            await self.config.guild(ctx.guild).message.set(join_message)
        else:
            await self.config.guild(ctx.guild).message.set(None)
    @custommessage.command
    async def leave(self, ctx, leave_message:str = None):
        """Set a custom message for users joining the server. If it is left blank, this will be disabled. Use {user} to mention the user that joined the server, and {username} to display the user's username."""
        if leave_message:
            await self.config.guild(ctx.guild).message.set(leave_message)
        else:
            await self.config.guild(ctx.guild).message.set(None)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        join = await self.config.guild(member.guild).do_joins()
        message = await self.config.guild(member.guild).join_message()
        message_channel = await self.config.guild(member.guild).message_channel
        channel = await self.config.guild(member.guild).channel()
        if not join:
            return
        if not channel:
            return
        time = datetime.datetime.utcnow()
        users_in_guild = len(member.guild.members)
        account_age = (time - member.created_at).days
        user_created = member.created_at.strftime("%Y-%m-%d, %H:%M")

        created_on = f"{user_created} ({account_age} days ago)"

        embed = discord.Embed(
            description=f"{member.mention} ({member.name}#{member.discriminator})",
            colour=discord.Colour.green(),
            timestamp=member.joined_at,
        )
        embed.add_field(name="Total Users:", value=str(users_in_guild))
        embed.add_field(name="Account created on:", value=created_on)
        embed.set_footer(text=f"User ID: {member.id}")
        embed.set_author(
            name=f"{member.name} has joined the guild",
            url=member.avatar_url,
            icon_url=member.avatar_url,
        )
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)
    if message:
        await message_channel.send(message.format(user=User, username=User.name))
        