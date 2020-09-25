from .skyblock import Skyblock


def setup(bot):
    bot.add_cog(Skyblock(bot))
