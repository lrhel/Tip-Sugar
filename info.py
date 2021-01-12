from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config
import utility

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)

        block = client.getblockchaininfo()['blocks']
        hash_rate = round(client.getnetworkhashps() / 1000, 4)
        difficulty = client.getblockchaininfo()['difficulty']
        connection = client.getnetworkinfo()['connections']
        client_version = client.getnetworkinfo()['subversion']
        blockchain_size = round(client.getblockchaininfo()['size_on_disk'] / 1000000000, 3)

        embed = await utility.make_embed(ctx,self.bot,
            title="**Sugarchain info**",
            color=0x0043ff)
        embed.add_field(
            name="__Current block height__",
            value="`{0}`".format(block),
            inline=True)
        embed.add_field(
            name="__Network hash rate__",
            value="`{0} KH/s`".format(hash_rate),
            inline=True)
        embed.add_field(
            name="__Difficulty__",
            value="`{0}`".format(difficulty),
            inline=True)
        embed.add_field(
            name="__Connection__",
            value="`{0}`".format(connection),
            inline=True)
        embed.add_field(
            name="__Client Version__",
            value="`{0}`".format(client_version),
            inline=True)
        embed.add_field(
            name="__Block chain size__",
            value="`About {0} GB`".format(blockchain_size),
            inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
