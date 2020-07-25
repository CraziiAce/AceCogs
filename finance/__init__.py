from .finance import Finance


def setup(bot):
    bot.add_cog(Finance(bot))