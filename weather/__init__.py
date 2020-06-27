from .weather import API


def setup(bot):
    bot.add_cog(API(bot))
