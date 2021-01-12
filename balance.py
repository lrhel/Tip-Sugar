import sys

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config
import utility

class Balance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        account = str(ctx.author.id)
        user_name = ctx.author.display_name
        balance = client.getbalance(account, config.confirm)
        unconfirmed_balance = client.getbalance(account, 0) - client.getbalance(account, config.confirm)
        embed = await utility.make_embed(ctx,self.bot,title="**Your balances**",color=0x0043ff)
        embed.add_field(name=f'{balance} SUGAR', value=f'Unconfirmed: {unconfirmed_balance} SUGAR')
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Balance(bot))
