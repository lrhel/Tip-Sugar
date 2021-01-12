from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config
import utility

class Deposit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deposit(self, ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        address = client.getaccountaddress(user_id)
        embed = await utility.make_embed(ctx,self.bot,
            title="**Your deposit address**",
            color=0x0043ff)
        embed.add_field(
            name="Send sugar to this address.",
            value="Click to enlarge the QR code")
        embed.set_thumbnail(url=f'https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={address}')

        await ctx.channel.send(embed=embed)
        await ctx.channel.send(f'```{address}```')

def setup(bot):
    bot.add_cog(Deposit(bot))
