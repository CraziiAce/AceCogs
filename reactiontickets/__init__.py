from .reactiontickets import ReactionTickets


def setup(bot):
    bot.add_cog(ReactionTickets(bot))