from redbot.core import commands, checks, Config, modlog

from typing import Optional
from datetime import datetime
import discord



class ReactionTickets(commands.Cog):
    """Dav's ticketer cog, but with reactions so i can test it and then make a pr."""
    async def red_delete_data_for_user(self,*,requester,user_id):
        # This cog stores no EUD
        return

    def __init__(self, bot):
        self.config = Config.get_conf(self, 200730042020, force_registration=True)
        default_guild = {
            "channel": None,
            "use_counter": False,
            "closed_category": None,
            "open_category": None,
            "current_ticket": 0,
            "role": None,
            "message": "Your ticket has been created. You can add information by typing in this channel. \n\nA member of the ticket-handling-team will be with you as soon as they can.",
            "active": [],
            "modlog": True,
            "closed": [],
            "react_message": None,
        }
        self.config.register_guild(**default_guild)
        self.bot = bot

    @staticmethod
    async def register_casetypes():
        new_types = [
            {
                "name": "ticket_created",
                "default_setting": True,
                "image": "\N{BALLOT BOX WITH BALLOT}\N{VARIATION SELECTOR-16}",
                "case_str": "Ticket created",
            }
        ]
        await modlog.register_casetypes(new_types)

    @commands.group()
    @checks.admin()
    async def reactticket(self, ctx):
        """All reaction tickets settings."""
        pass

    @reactticket.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the ticket-management channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(f"Channel has been set to {channel.mention}.")

    @reactticket.command()
    async def role(self, ctx, role: discord.Role):
        """Set the role for ticket managers."""
        await self.config.guild(ctx.guild).role.set(role.id)
        await ctx.send(f"Ticket manager role has been set to {role.mention}.")

    @reactticket.group()
    async def category(self, ctx):
        """Set the categories for open and closed tickets."""

    @category.group()
    async def open(self, ctx, category: discord.CategoryChannel):
        """Set the category for open tickets."""
        await self.config.guild(ctx.guild).open_category.set(category.id)
        await ctx.send(f"Category for open tickets has been set to {category.mention}")

    @category.group()
    async def closed(self, ctx, category: discord.CategoryChannel):
        """Set the category for closed tickets."""
        await self.config.guild(ctx.guild).closed_category.set(category.id)
        await ctx.send(f"Category for closed tickets has been set to {category.mention}")

    @reactticket.command()
    async def message(self, ctx, *, message: str):
        """Set the message that is shown at the start of each ticket channel."""
        await self.config.guild(ctx.guild).message.set(message)
        await ctx.send(f"The message has been set to ``{message}``.")

    @reactticket.command()
    async def counter(self, ctx, true_or_false: bool):
        """Toggle if the ticket channels should be named using a user's name and ID or counting upwards starting at 0."""
        await self.config.guild(ctx.guild).use_counter.set(true_or_false)
        await ctx.send(
            "The counter has been {}.".format("enabled" if true_or_false else "disabled")
        )

    @reactticket.command()
    async def modlog(self, ctx, true_or_false: bool):
        """Decide if ticketer should log to modlog."""
        await self.config.guild(ctx.guild).modlog.set(true_or_false)
        await ctx.send(
            "Logging to modlog has been {}.".format("enabled" if true_or_false else "disabled")
        )

    @reactticket.command()
    async def purge(self, ctx, are_you_sure: Optional[bool]):
        if are_you_sure:
            async with self.config.guild(ctx.guild).closed() as closed:
                for channel in closed:
                    try:
                        channel_obj = ctx.guild.get_channel(channel)
                        if channel_obj:
                            await channel_obj.delete(reason="Ticket purge")
                        closed.remove(channel)
                    except discord.Forbidden:
                        await ctx.send(
                            f"I could not delete channel ID {channel} because I don't have the required permissions."
                        )
                    except discord.NotFound:
                        closed.remove(channel)
                    except discord.HTTPException:
                        await ctx.send("Something went wrong. Aborting.")
                        return
        else:
            await ctx.send(
                f"This action will permanently delete all closed ticket channels.\nThis action is irreversible.\nConfirm with ``{ctx.clean_prefix}ticketer purge true``"
            )

    @reactticket.command()
    async def close(self, ctx):
        """Close a ticket."""
        settings = await self.config.guild(ctx.guild).all()
        active = settings["active"]
        success = False
        print("ctx.channel.id")
        print(active)
        print(await self.config.guild(ctx.guild).active())
        if ctx.channel.id in active:
            new_embed = (
                await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
            ).embeds[0]
            new_embed.add_field(
                name=datetime.utcnow().strftime("%H:%m UTC"),
                value=f"Ticket closed by {ctx.author.name}#{ctx.author.discriminator}",
            )
            new_embed.timestamp = datetime.utcnow()
            await (
                await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
            ).edit(
                embed=new_embed, delete_after=10,
            )
            await ctx.send(embed=new_embed)
            await ctx.send(
                "This ticket can no longer be edited using ticketer.", delete_after=30
            )
            await ctx.channel.edit(
                category=ctx.guild.get_channel(settings["closed_category"]),
                name=f"{ctx.channel.name}-c-{datetime.utcnow().strftime('%B-%d-%Y-%H-%m')}",
                overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                        manage_messages=True,
                    ),
                },
            )
            await ctx.send("Ticket closed.")
            active.remove(ticket)
            async with self.config.guild(ctx.guild).closed() as closed:
                closed.append(ticket[0])
            success = True
        if not success:
            await ctx.send("This is not a ticket channel.")
        await self.config.guild(ctx.guild).active.set(active)

    @reactticket.command()
    @checks.mod()
    async def update(self, ctx, ticket: Optional[discord.TextChannel] = None, *, update: str):
        """Update a ticket. This is visible to all participants of the ticket."""
        if ticket is None:
            channel = ctx.channel
        else:
            channel = ticket
        settings = await self.config.guild(ctx.guild).all()
        active = settings["active"]
        for ticket in active:
            if channel.id in ticket:
                await channel.edit(
                    topic=f'{channel.topic}\n\n{ctx.author.name}#{ctx.author.discriminator}:"{update}"'
                )
                await ctx.send("Ticket updated.", delete_after=10)
            else:
                ctx.send(f"{channel.mention} is not a ticket channel.")

    @reactticket.command()
    @checks.mod()
    async def note(self, ctx, ticket: discord.TextChannel, *, note: str):
        """Add a staff-only note to a ticket."""
        channel = ticket
        for ticket in await self.config.guild(ctx.guild).active():
            if channel.id in ticket:
                message = await ctx.guild.get_channel(
                    await self.config.guild(ctx.guild).channel()
                ).fetch_message(ticket[1])
                new_embed = message.embeds[0]
                new_embed.add_field(
                    name=f"{ctx.author.name}#{ctx.author.discriminator}", value=note
                )
                new_embed.timestamp = datetime.utcnow()
                await message.edit(embed=new_embed)
                await ctx.send("Note added.", delete_after=10)
            else:
                await ctx.send("This is not a ticket channel.")
    @reactticket.command()
    @checks.mod()
    async def start(self, ctx):
        """Start the reaction ticket system"""
        channel = self.bot.get_channel(await self.config.guild(ctx.guild).channel())
        embed = discord.Embed(
            title="Support tickets",
            description="testing something"
        )
        msg = await channel.send(embed=embed)
        await self.config.guild(ctx.guild).react_message.set(msg.id)
    async def _check_settings(self, ctx: commands.Context) -> bool:
        settings = await self.config.guild(ctx.guild).all()
        count = 0
        if settings["channel"]:
            count += 1
        else:
            await ctx.send("Management channel not set up yet.")
        if settings["closed_category"]:
            count += 1
        else:
            await ctx.send("Category for closed tickets not set up yet.")
        if settings["open_category"]:
            count += 1
        else:
            await ctx.send("Category for open tickets not set up yet.")
        if settings["role"]:
            count += 1
        else:
            await ctx.send("Ticket manager role not set up yet.")
        if count == 4:
            return True
        else:
            return False
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        author = payload.member
        settings = await self.config.guild(guild).all()
        channel = self.bot.get_channel(settings["channel"])
        message = await channel.fetch_message(settings["react_message"])
        try:
            if settings["react_message"] == payload.message_id:
                if settings["modlog"]:
                    await modlog.create_case(
                        self.bot,
                        guild,
                        datetime.now(),
                        action_type="ticket_created",
                        user=author,
                        moderator=author,
                        reason="User reacted to a ticket message.",
                    )
                overwrite = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    author: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                    ),
                    guild.get_role(settings["role"]): discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        embed_links=True,
                        attach_files=True,
                        manage_messages=True,
                    ),
                }
                ticketchannel = await guild.create_text_channel(
                    f"Ticket - {author.name}#{author.discriminator}",
                    overwrites=overwrite,
                    category=guild.get_channel(settings["open_category"]),
                )
                await message.remove_reaction(payload.emoji, author)
                await ticketchannel.send(settings["message"])
                settings["active"].append(ticketchannel.id)
                print(settings["active"])
        except KeyError:
            print(f'A user reacted to a reactionticket in a guild with ID {guild.id}, but it isn\'t set up!')
