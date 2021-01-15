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

def str_isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class Withdraw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _withdraw(self, ctx, address, amount):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        embed = await utility.make_embed(ctx,self.bot,color=0xff0000)
        validate = {}
        if not str_isfloat(amount) or Decimal(amount) < Decimal('0.5'):
            embed.add_field(
                name=f'invalid amount. (amount must be at least 0.5 {config.currency})',
                value=f'`{amount}`')
        else:
            sendamount = Decimal(str(float(amount))) - \
                        Decimal(str(config.fee)) # Dealing with cases like "001.100" : "float(amount)"
            account = str(ctx.author.id)
            if address:
                validate = client.validateaddress(address)
            else:
                validate['isvalid'] = False
            if not validate['isvalid']:
                embed.add_field(
                    name="invalid address.",
                    value=f'`{address}`')
            elif Decimal(amount) > client.getbalance(account, config.confirm):
                embed.add_field(
                    name="You don't have enough balances.",
                    value=f'Your balances : ```{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}```')
            else:
                try:
                    txid = client.sendfrom(account, address, float(sendamount))
                except:
                    embed.add_field(
                        name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                        value=f'`{amount}`')
                    txid = ""
                if len(txid) == 64:
                    tx = client.gettransaction(txid)
                    txfee = tx['fee']
                    client.move(account, f'{config.withdraw_wallet}', Decimal(str(config.fee)))
                    client.move(f'{config.withdraw_wallet}', account, -txfee)
                    embed.add_field(
                        name=f'Withdrawal complete `{utility.moneyfmt(sendamount)} {config.currency}`\nwithdraw fee is `{config.fee} {config.currency}`\nPlease check the transaction at the below link.',
                        value=f'Your balances : `{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}`')
                    embed.add_field(name=f'Transaction ID', value=f'[{txid}](https://1explorer.sugarchain.org/tx/{txid})')
        return embed

    @commands.command()
    async def withdraw(self, ctx, address=None, amount=None):
        embed = await self._withdraw(ctx, address, amount)
        await ctx.channel.send(embed=embed)

    @cog_ext.cog_slash(name="withdraw", description=f'Withdraw an amount of your {config.currency}', guild_ids=config.guilds,
        options=[manage_commands.create_option("address", f'The {config.currency} address to withdraw your balance', SlashCommandOptionType.STRING, True), manage_commands.create_option("amount", f'The amount of {config.currency} to withdraw', SlashCommandOptionType.STRING, True)])
    async def withdraw_slash(self, ctx: SlashContext, address, amount):
        ctx.author = await self.bot.fetch_user(ctx.author)
        embed = await self._withdraw(ctx, address, amount)
        await ctx.send(embeds=[embed])


def setup(bot):
    bot.add_cog(Withdraw(bot))
