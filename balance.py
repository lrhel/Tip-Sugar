import sys

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext

import config
import utility

class Balance(commands.Cog):

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _balance(self, ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        balance = client.getbalance(user_id, config.confirm)
        unconfirmed_balance = client.getbalance(user_id, 0) - client.getbalance(user_id, config.confirm)
        embed = await utility.make_embed(ctx,self.bot,title="**Your balances**",color=0x0043ff)
        embed.add_field(name=f'{utility.moneyfmt(balance)} {config.currency}', value=f'Unconfirmed: {utility.moneyfmt(unconfirmed_balance)} {config.currency}')
        return embed

    @commands.command()
    async def balance(self, ctx):
        embed = await self._balance(ctx)
        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="balance", description=f'Get your {config.currency} Balance', guild_ids=config.guilds)
    async def balance_clog(self, ctx: SlashContext):
        ctx.author = await self.bot.fetch_user(ctx.author)
        embed = await self._balance(ctx)
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Balance(bot))
