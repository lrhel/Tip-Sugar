import discord
from discord.ext import commands

import user_db
import config
import utility

class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if prefix:
            user_db.add_prefix(ctx.message.guild.id, prefix)
            await ctx.channel.send(f'The prefix is set as `{prefix}`')
        else:
            prefix = user_db.get_prefix(ctx.message.guild.id)
            if prefix:
                await ctx.channel.send(f'The prefix is `{prefix[0]}`')
            else:
                await ctx.channel.send(f'This server has no prefix set')

def setup(bot):
    bot.add_cog(Prefix(bot))
