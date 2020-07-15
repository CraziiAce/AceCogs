from .messagelog import MessageLog


def setup(bot):
    bot.add_cog(MessageLog(bot))