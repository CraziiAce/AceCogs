from .memberlogs import MemberLogs


def setup(bot):
    bot.add_cog(MemberLogs(bot))