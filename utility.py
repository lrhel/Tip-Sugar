import discord
import config
import user_db

from decimal import Decimal

async def make_embed(ctx,bot,title='',url='',color=config.default_color):
    owner = await bot.fetch_user(config.owner_id)
    embed = discord.Embed(title=title,url=url,color=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(format='png', size=256))
    embed.set_footer(text=f'Tip {config.currency} {config.version} [Owner: {owner}]', icon_url=bot.user.avatar_url_as(format='png', size=256))
    return embed

def prefix(bot, msg):
    prefix = (user_db.get_prefix(msg.guild.id))
    return prefix if prefix else (config.prefix.lower(),config.prefix.capitalize())

# From https://docs.python.org/3/library/decimal.html#recipes under PSF License Agreement and Zero-Clause BSD license
def moneyfmt(value, places=8, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))
