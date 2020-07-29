from redbot.core import commands, checks, Config

import datetime
import discord
class MemberLogs(commands.Cog):
    """Log when members join/leave a server."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=7777232377772323, force_registration=True
        )

        self.config.register_guild(channel=None, do_join_logs=True, do_leave_logs=True, join_message=None, leave_message=None, message_channel=None)
    @commands.group()
    @commands.guild_only()
    @commands.admin()
    async def memberlog(self, ctx):
        """Log members joining & leaving"""
        pass
    @memberlog.command()
    async def channel(self, ctx, log_channel: discord.TextChannel = None):
        """Set the channel where member logs will be sent. Use this without a channel to turn off the logs."""
        if log_channel:
            await self.config.guild(ctx.guild).channel.set(log_channel.id)
            await ctx.send("User logs successfully turned on.")
        else:
            await self.config.guild(ctx.guild).channel.set(None)
            await ctx.send("User logs successfully turned off.")
    @commands.group()
    @commands.admin()
    @commands.guild_only()
    async def custommessage(self, ctx):
        """Send a custom message when someone joins/leaves."""
    @custommessage.command()
    async def join(self, ctx, *, join_message: str = None):
        """Set a custom message for users joining the server. If it is left blank, this will be disabled. Use {user} to mention the user that joined the server, and {username} to display the user's username."""
        if join_message:
            await self.config.guild(ctx.guild).join_message.set(join_message)
            await ctx.send(f"Join message succesfully set to {join_message}")
        else:
            await self.config.guild(ctx.guild).join_message.set(None)
            await ctx.send("Join message turned off.")
    @custommessage.command()
    async def leave(self, ctx, *, leave_message: str = None):
        """Set a custom message for users joining the server. If it is left blank, this will be disabled. Use {user} to mention the user that joined the server, and {username} to display the user's username."""
        if leave_message:
            await self.config.guild(ctx.guild).leave_message.set(leave_message)
            await ctx.send(f"Leave message succesfully set to {leave_message}")
        else:
            await self.config.guild(ctx.guild).leave_message.set(None)
            await ctx.send("Leave message turned off.")
    @custommessage.command()
    async def message_channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel where member logs will be sent. Use this without a channel to turn off the logs."""
        if channel:
            await self.config.guild(ctx.guild).message_channel.set(channel.id)
            await ctx.send("ustom messages successfully turned on.")
        else:
            await self.config.guild(ctx.guild).channel.set(None)
            await ctx.send("Custom messages successfully turned off.")
    @commands.Cog.listener()
    async def on_member_join(self, member):
        join = await self.config.guild(member.guild).do_join_logs()
        message = await self.config.guild(member.guild).join_message()
        message_channel = await self.config.guild(member.guild).message_channel()
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
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave = await self.config.guild(member.guild).do_leave_logs()
        message = await self.config.guild(member.guild).leave_message()
        message_channel = await self.config.guild(member.guild).message_channel()
        channel = await self.config.guild(member.guild).channel()
        if not leave:
            return
        if not channel:
            return
        time = datetime.datetime.utcnow()
        users = len(member.guild.members)
        embed = discord.Embed(
            description=f"{member.mention} ({member.name}#{member.discriminator})",
            colour=discord.Colour.red(),
            timestamp=time,
        )
        embed.add_field(name="Total Users:", value=str(users))
        embed.set_footer(text=f"User ID: {member.id}")
        embed.set_author(
            name=f"{member.name} has left the guild",
            url=member.avatar_url,
            icon_url=member.avatar_url,
        )
        embed.set_thumbnail(url=member.avatar_url)
        await message_channel.send(embed=embed)
        if message:
            await message_channel.send(message.format(user=User, username=User.name))
