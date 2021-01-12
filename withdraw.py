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
                name="invalid amount. (amount must be at least 0.5 SUGAR)",
                value=f'`{amount}`')
        else:
            sendamount = Decimal(str(float(amount))) - \
                        Decimal(str(config.fee)) # Dealing with cases like "001.100" : "float(amount)"
            account = str(ctx.author.id)

            validate = client.validateaddress(address)
            if not validate['isvalid']:
                embed.add_field(
                    name="invalid address.",
                    value="`{0}`".format(str(address)))
            elif Decimal(amount) > client.getbalance(account, config.confirm):
                embed.add_field(
                    name="You don't have enough balances.",
                    value="Your balances : ```{0} SUGAR```".format(client.getbalance(account, config.confirm)))
            else:
                try:
                    txid = client.sendfrom(account, address, float(sendamount))
                except:
                    embed.add_field(
                        name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                        value="`{0}`".format(amount))
                    txid = ""
                if len(txid) == 64:
                    tx = client.gettransaction(txid)
                    txfee = tx['fee']
                    client.move(account, "tipsugar_wallet", Decimal(str(config.fee)))
                    client.move("tipsugar_wallet", account, -txfee)
                    embed.add_field(
                        name=f'Withdrawal complete `{sendamount} SUGAR`\nwithdraw fee is `{config.fee} SUGAR`\nPlease check the transaction at the below link.',
                        value=f'Your balances : `{client.getbalance(account, config.confirm)} SUGAR`')
                    embed.add_field(value=f'[{txid}](https://1explorer.sugarchain.org/tx/{txid})')

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdraw(bot))
