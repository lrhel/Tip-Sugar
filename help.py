import discord
from discord.ext import commands

import user_db
import config
import utility

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        user_id = str(ctx.author.id)
        user_name = ctx.author.name
        prefix = utility.prefix(self.bot, ctx.message)[0]
        embed = await utility.make_embed(ctx, self.bot,
            title=f'**Sugar Bot Command List:**',
            color=0x7152b6)
        embed.add_field(
            name=f'**{prefix}info**',
            value=f'Show Sugar Core wallet/blockchain info.',
            inline=True)
        embed.add_field(
            name=f'**{prefix}balance**',
            value=f'Show your Sugar balances.',
            inline=True)
        embed.add_field(
            name=f'**{prefix}deposit**',
            value=f'Show your Sugar deposit address.',
            inline=True)
        embed.add_field(
            name=f'**{prefix}tip** @user *<amount>*',
            value=f'Tip specified user.',
            inline=True)
        embed.add_field(
            name=f'**{prefix}withdraw** *<address>* *<amount>*',
            value=f'Withdraw Sugar from your wallet.',
            inline=True)
        embed.add_field(
            name=f'**{prefix}withdrawall** *<address>*',
            value=f'Withdraw all Sugar from your wallet.',
            inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
