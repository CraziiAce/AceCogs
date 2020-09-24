from .skyblock import Hypixel


def setup(bot):
    bot.add_cog(Hypixel(bot))
