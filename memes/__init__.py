from .memes import Memes


def setup(bot):
    bot.add_cog(Memes(bot))