import discord
import config
import user_db

async def make_embed(ctx,bot,title='',url='',color=config.default_color):
    owner = await bot.fetch_user(config.owner_id)
    embed = discord.Embed(title=title,url=url,color=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(format='png', size=256))
    embed.set_footer(text=f'Tip Sugar {config.version} [Owner: {owner}]', icon_url=bot.user.avatar_url_as(format='png', size=256))
    return embed

def prefix(bot, msg):
    prefix = (user_db.get_prefix(msg.guild.id))
    return prefix if prefix else (config.prefix.lower(),config.prefix.capitalize())
