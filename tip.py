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

class Tip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tip(self, ctx, mention=None, amount=None):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        embed = await utility.make_embed(ctx,self.bot, color=0xffd800)
        if mention is None or amount is None:
            embed.add_field(
                name="Please check `//help` ",
                value=" :mag: ")
        elif not str_isfloat(amount):
            embed.add_field(
                name="invalid amount.",
                value="`{0}`".format(amount))
        else:
            tipfrom = str(ctx.author.id)
            tipto = str(mention.replace('<@','').replace('>','')).replace('!','')
            amount = Decimal(str(float(amount))) # Dealing with cases like "001.100", ".123" : "float(amount)"

            if amount < Decimal('0.00000001'):
                embed.add_field(
                    name=f'amount must be at least 0.00000001 {config.currency}',
                    value=f'`{amount} {config.currency}`')
            else:
                if len(tipto) != 18 and len(tipto) != 17: # length of discord user id is 18 or 17
                    embed.add_field(
                        name="invalid user.",
                        value="`{0}`".format(str(mention)))
                elif tipfrom == tipto:
                    embed.add_field(
                        name="You cannot tip to yourself.",
                        value=" :thinking: ")
                elif amount > client.getbalance(tipfrom, config.confirm):
                    embed.add_field(
                        name="You don't have enough balances.",
                        value=f'Your balances ```{utility.moneyfmt(client.getbalance(tipfrom, config.confirm))} {config.currency}```')
                else:
                    if tipto == str(self.bot.user.id):
                        try:
                            move_istrue = client.move(tipfrom, config.donation_wallet, float(amount))
                        except:
                            embed.add_field(
                                name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                                value=f'"`{amount}`')
                            move_istrue = False
                        if move_istrue:
                            embed.add_field(
                                name="Thank you for donating!",
                                value=f'```{amount} {config.currency}```')
                    else:
                        try:
                            move_istrue = client.move(tipfrom, tipto, float(amount))
                        except:
                            embed.add_field(
                                name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                                value='`{amount}`')
                            move_istrue = False
                        if move_istrue:
                            embed.add_field(name=f'{ctx.author} tipped to {self.bot.get_user(int(tipto))} `{utility.moneyfmt(amount)} {config.currency}`', value="yay!")
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Tip(bot))
