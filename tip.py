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

class Tip(commands.Cog):

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _tip(self, ctx, embed, user, amount):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        if not str_isfloat(amount):
            embed.add_field(
                name="invalid amount.",
                value="`{0}`".format(amount))
        else:
            tipfrom = str(ctx.author.id)
            amount = Decimal(str(float(amount))) # Dealing with cases like "001.100", ".123" : "float(amount)"

            if amount < Decimal('0.00000001'):
                embed.add_field(
                    name=f'amount must be at least 0.00000001 {config.currency}',
                    value=f'`{amount} {config.currency}`')
            else:
                if len(user) != 18 and len(user) != 17: # length of discord user id is 18 or 17
                    embed.add_field(
                        name="invalid user.",
                        value="`{0}`".format(str(mention)))
                elif tipfrom == user:
                    embed.add_field(
                        name="You cannot tip to yourself.",
                        value=" :thinking: ")
                elif amount > client.getbalance(tipfrom, config.confirm):
                    embed.add_field(
                        name="You don't have enough balances.",
                        value=f'Your balances ```{utility.moneyfmt(client.getbalance(tipfrom, config.confirm))} {config.currency}```')
                else:
                    if user == str(self.bot.user.id):
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
                            move_istrue = client.move(tipfrom, user, float(amount))
                        except:
                            embed.add_field(
                                name="invalid amount.\n(You can not specify the einth decimal place or smaller than that.)",
                                value=f'`{amount}`')
                            move_istrue = False
                        if move_istrue:
                            embed.add_field(name=f'{ctx.author} tipped to {self.bot.get_user(int(user))} `{utility.moneyfmt(amount)} {config.currency}`', value="yay!")
        return embed

    @commands.command()
    async def tip(self, ctx, mention=None, amount=None):
        embed = await utility.make_embed(ctx,self.bot, color=0xffd800)
        if mention is None or amount is None:
            embed.add_field(
                name=f'Please check `{utility.prefix(self.bot, ctx.message)[0]}help`',
                value=" :mag: ")
        else:
            embed = await self._tip(ctx, embed, str(mention.replace('<@','').replace('>','')).replace('!',''), amount)
        await ctx.channel.send(embed=embed)


    @cog_ext.cog_slash(name="tip", description=f'Tip someone with some {config.currency}', guild_ids=config.guilds,
        options=[manage_commands.create_option("user", "The user to tip", SlashCommandOptionType.USER, True), manage_commands.create_option("amount", f'The amount of {config.currency} to tip', SlashCommandOptionType.STRING, True)])
    async def tip_clog(self, ctx: SlashContext, user, amount):
        ctx.author = await self.bot.fetch_user(ctx.author)
        embed = await utility.make_embed(ctx,self.bot, color=0xffd800)
        embed = await self._tip(ctx, embed, str(user.id), amount)
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Tip(bot))
