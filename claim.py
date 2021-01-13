from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from decimal import Decimal
import time

import user_db
import config
import utility

class Claim(commands.Cog):

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _make_claim(self,ctx,client):
        claim = user_db.can_claim(ctx.author.id)
        if claim[0]:
            if client.getbalance(config.faucet_wallet, config.confirm) > config.faucet:
                user_db.update_claim(ctx.author.id)
                client.move(config.faucet_wallet, str(ctx.author.id), float(config.faucet))
                embed = await utility.make_embed(ctx,self.bot, title=":tada: Congratulation :tada:", color=0x4b8b3b)
                embed.add_field(name=f'You got {config.faucet} {config.currency}', value=f'Your balance is now {utility.moneyfmt(client.getbalance(str(ctx.author.id), config.confirm))} {config.currency}')
                return embed
            else:
                return await utility.make_embed(ctx,self.bot, title="Not enough funds", color=0xd0312d)
        else:
            to_wait = (claim[1] + config.faucet_time) - int(time.time())
            return await utility.make_embed(ctx,self.bot, title=f'You have to wait {int(to_wait / 3600):02}:{int(to_wait / 60):02}:{int(to_wait % 60):02}', color=0xd0312d)

    @commands.command()
    async def claim(self,ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        embed = await self._make_claim(ctx,client)
        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="claim", description=f'Claim some Free {config.currency}', guild_ids=config.guilds)
    async def claim_slash(self, ctx: SlashContext):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        ctx.author = await self.bot.fetch_user(ctx.author)
        embed = await self._make_claim(ctx,client)
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Claim(bot))

