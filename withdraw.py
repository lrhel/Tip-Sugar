from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands

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

    @commands.command()
    async def withdraw(self, ctx, address=None, amount=None):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        embed = await utility.make_embed(ctx,self.bot,color=0xff0000)
        if not str_isfloat(amount) or Decimal(amount) < Decimal('0.5'):
            embed.add_field(
                name=f'invalid amount. (amount must be at least 0.5 {config.currency})',
                value=f'`{amount}`')
        else:
            sendamount = Decimal(str(float(amount))) - \
                        Decimal(str(config.fee)) # Dealing with cases like "001.100" : "float(amount)"
            account = str(ctx.author.id)

            validate = client.validateaddress(address)
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

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdraw(bot))
