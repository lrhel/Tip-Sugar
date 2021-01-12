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
        prefix = config.prefix(self.bot,ctx.message)
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
            name=f'**{prefix}tip**',
            value=f'Tip specified user. [{prefix}tip @user <amount>] to tip 1 SUGAR',
            inline=True)
        embed.add_field(
            name=f'**{prefix}withdraw**',
            value=f'Withdraw Sugar from your wallet. [{prefix}withdraw ADDRESS AMOUNT]',
            inline=True)
        embed.add_field(
            name=f'**{prefix}withdrawall**',
            value=f'Withdraw all Sugar from your wallet. [{prefix}withdrawall ADDRESS]',
            inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
