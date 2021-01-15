from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext

import user_db
import config
import utility

class Deposit(commands.Cog):

    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _deposit(self, ctx):
        client = AuthServiceProxy(f'http://{config.rpc_user}:{config.rpc_password}@{config.ip}:{config.rpc_port}')
        user_id = str(ctx.author.id)
        address = client.getaccountaddress(user_id)
        embed = await utility.make_embed(ctx,self.bot,
            title="**Your deposit address**",
            color=0x0043ff)
        embed.add_field(
            name=f'Send {config.currency} to this address.',
            value="Click to enlarge the QR code")
        embed.set_thumbnail(url=f'https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={address}')
        return [embed, address]

    @commands.command()
    async def deposit(self, ctx):
        r = await self._deposit(ctx)
        await ctx.channel.send(embed=r[0])
        await ctx.channel.send(f'```{r[1]}```')

    @cog_ext.cog_slash(name="deposit", description=f'Get {config.currency} deposit address', guild_ids=config.guilds)
    async def deposit_slash(self, ctx: SlashContext):
        ctx.author = await self.bot.fetch_user(ctx.author)
        r = await self._deposit(ctx)
        await ctx.send(embeds=[r[0]], content=f'```{r[1]}```')

def setup(bot):
    bot.add_cog(Deposit(bot))
