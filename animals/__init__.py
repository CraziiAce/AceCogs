from .animals import Animals


def setup(bot):
    bot.add_cog(Animals(bot))
