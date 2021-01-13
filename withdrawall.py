from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands

import user_db
import config
import utility

# connect to coind

class Withdrawall(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def withdrawall(self, ctx, address=None):
        user_id = str(ctx.author.id)
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        account = str(ctx.author.id)
        balance = Decimal(client.getbalance(account, config.confirm))
        embed = await utility.make_embed(ctx,self.bot,color=0xff0000)
        if balance < Decimal('0.5'):
            embed.add_field(
                name=f'Amount must be at least 0.5 {config.currency}.',
                value=f'Your balances : ```{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}```')
        else:
            amount = balance - Decimal(str(config.fee))
            validate = client.validateaddress(address)

            if not validate['isvalid']:
                embed.add_field(
                    name="invalid address.",
                    value=f'`{address}`')
            else:
                txid = client.sendfrom(account, address, float(amount))
                tx = client.gettransaction(txid)
                txfee = tx['fee']

                client.move(account, f'{config.withdraw_wallet}', Decimal(str(config.frr)))
                client.move(f'{withdraw_wallet}', account, -txfee)

                embed.add_field(
                    name=f'Withdrawal complete `{utility.moneyfmt(amount)} {config.currency}`\nwithdraw fee is `{str(config.fee)} {config.currency}`\nPlease check the transaction at the following link.',
                    value=f'Your balances : `{utility.moneyfmt(client.getbalance(account, config.confirm))} {config.currency}`')
                embed.add_field(name=f'Transaction ID', value=f'[{txid}](https://1explorer.sugarchain.org/tx/{txid})')
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdrawall(bot))
