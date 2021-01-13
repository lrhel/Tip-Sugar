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
                name="Amount must be at least 0.5 SUGAR.",
                value=f'Your balances : ```{utility.moneyfmt(client.getbalance(account, config.confirm))} SUGAR```')
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

                client.move(account, "tipsugar_wallet", Decimal(str(config.frr)))
                client.move("tipsugar_wallet", account, -txfee)

                embed = discord.Embed(
                    title="**Block explorer**",
                    url=f'https://1explorer.sugarchain.org/tx/{txid}',
                    color=0x0043ff)
                embed.add_field(
                    name=f'Withdrawal complete `{utility.moneyfmt(amount)} SUGAR`\nwithdraw fee is `{str(config.fee)} SUGAR`\nPlease check the transaction at the above link.',
                    value=f'Your balances : `{utility.moneyfmt(client.getbalance(account, config.confirm))} SUGAR`')

        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdrawall(bot))
