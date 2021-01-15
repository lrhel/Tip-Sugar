from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands

import user_db
import config
import utility

class Withdrawall(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _withdrawall(self, ctx, address):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        account = str(ctx.author.id)
        balance = Decimal(client.getbalance(account, config.confirm))
        embed = await utility.make_embed(ctx,self.bot,color=0xff0000)
        validate = {}
        if balance < Decimal('0.5'):
            embed.add_field(
                name=f'Amount must be at least 0.5 {config.currency}.',
                value=f'Your balances : ```{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}```')
        else:
            amount = balance - Decimal(str(config.fee))
            if address:
                validate = client.validateaddress(address)
            else:
                validate['isvalid'] = False
            if not validate['isvalid']:
                embed.add_field(
                    name="invalid address.",
                    value=f'`{address}`')
            else:
                txid = client.sendfrom(account, address, float(amount))
                tx = client.gettransaction(txid)
                txfee = tx['fee']

                client.move(account, f'{config.withdraw_wallet}', Decimal(str(config.fee)))
                client.move(f'{config.withdraw_wallet}', account, -txfee)

                embed.add_field(
                    name=f'Withdrawal complete `{utility.moneyfmt(amount)} {config.currency}`\nwithdraw fee is `{str(config.fee)} {config.currency}`\nPlease check the transaction at the following link.',
                    value=f'Your balances : `{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}`')
                embed.add_field(name=f'Transaction ID', value=f'[{txid}](https://1explorer.sugarchain.org/tx/{txid})')
        return embed

    @commands.command()
    async def withdrawall(self, ctx, address=None):
        embed = await self._withdrawall(ctx, address)
        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="withdrawall", description=f'Withdraw all of your {config.currency}', guild_ids=config.guilds,
        options=[manage_commands.create_option("address", f'The {config.currency} address to withdraw your balance', SlashCommandOptionType.STRING, True)])
    async def withdrawall_slash(self, ctx: SlashContext, address):
        ctx.author = await self.bot.fetch_user(ctx.author)
        embed = await self._withdrawall(ctx, address)
        await ctx.send(embeds=[embed])



def setup(bot):
    bot.add_cog(Withdrawall(bot))
