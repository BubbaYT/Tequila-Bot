import discord
from Tools.scripts.which import msg
from discord.ext import commands
import os
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import asyncio

bot = commands.Bot(command_prefix=".", status=discord.Status.idle, game=discord.Game(name="Booting.."))
print("Bot Online")

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name=" Factions "
                                                        "With Bubba ;D"))
@bot.command()
async def msg(ctx, *, message):
    """: Msges everyone in the discord"""
    if ctx.author.permissions_in(ctx.channel).administrator:
        for i in ctx.guild.members:
            try:
                await i.send(message)
            except:
                pass

@bot.command()
async def send(ctx):
    """: Sends the Apply msg"""
    if ctx.author.permissions_in(ctx.channel).manage_guild:
        await ctx.send("**Tequila is Recruiting .apply to apply @everyone**")
        await ctx.message.delete()



@bot.command()
@commands.has_permissions(manage_guild=True)
async def send2(ctx):
    """: Sends the Timezone msg"""
    await ctx.send("**Make sure to set your timezone above @everyone**")
    await ctx.message.delete()


@bot.command()
async def apply(context):
    """: Apply to join"""
    auth = context.author
    channel = bot.get_channel(523616598955917312)

    await context.send("You have started a application")
    await auth.send("You are applying to join **Tequila**\nYou have 30 seconds to respond")

    def check(m):
        return isinstance(m.channel, discord.DMChannel) and m.author == auth

    answers = []
    questions = {
        'IGN': 'Whats your IGN? (In Game Name)',
        'AGE': 'How old are you?',
        'DISCORD': 'Whats your Discord? Example: Bubba#9125',
        'SCHEMATICA': 'Do you have schematica?',
        'FACTIONS IN ATM': 'Whats factions are you in atm?',
        'FACTIONS BEEN IN': 'What factions have you been in?',
        'HOURS PER WEEKDAY': 'How many hours a day can you play on weekdays?',
        'HOURS PER WEEKEND': 'How many hours a day can you play on weekends?',
        'DO YOU HACK': 'Do you have any hacks?',
        'PVP RATING': 'Rate yourself 1-10 on PvP',
        'CANNONING RATING': 'Rate yourself 1-10 on Cannoning'
    }

    try:
        for q in questions.values():
            await auth.send(q)
            m = await bot.wait_for("message", check=check, timeout=30)
            answers.append(m.content)
    except asyncio.TimeoutError:
        await auth.send("Sorry! You took too long to respond")

    await auth.send('**Your application has been received.'
                    'Thank you for applying.**')

    response = ''
    for i, e in enumerate(questions.keys()):
        response += f'{e}: {answers[i]}\n'

    await channel.send(f'A new application has been received.\n\n{response}')

@bot.command()
async def accept(ctx, user: discord.Member):
    """: Accepts a appicant"""
    if ctx.author.permissions_in(ctx.channel).manage_roles:
     await ctx.send(f"{user.mention} has been accepted to **___Tequila___**")
     await user.send("Welcome to **Tequila** Please dont mute the discord!!!")
     role1 = discord.utils.get(ctx.guild.roles, name = "Wall-Checkers")
     role2 = discord.utils.get(ctx.guild.roles, name = "*")
     role3 = discord.utils.get(ctx.guild.roles, name = "{¤}Recruit")
     await user.add_roles(role1, role2, role3)
     await ctx.message.delete()

@bot.command()
async def reject(ctx, user: discord.Member):
    """: Rejects a applicant"""
    if ctx.author.permissions_in(ctx.channel).manage_roles:
      await ctx.send(f"{user.mention} has been denied from **Tequila**")
      await user.send("You have been rejected.")
      await ctx.message.delete()

@bot.command()
async def prune(ctx, number: int):
      await ctx.channel.purge(limit=number)
      await ctx.send(f"Deleted {number} message(s)")

@bot.command()
async def shit(ctx, member: discord.Member):
    ''': Show em how shitty they are'''
    x = Image.open("pngs/shit.png")
    async with aiohttp.ClientSession() as cs:
        async with cs.get(member.avatar_url_as(format='png')) as r:
            b = io.BytesIO(await r.read())
    # open the pic and give it an alpha channel so it's transparent
    im1 = Image.open(b).convert('RGBA')
    im4 = im1.resize((120, 200))
    # rotate it and expand it's canvas so the corners don't get cut off:
    im2 = im4.rotate(-45, expand=1)

    # note the second appearance of im2, that's necessary to paste without a bg
    x.paste(im2, (200, 655), im2)
    x.save("SHIT.png")
    await ctx.send(file=discord.File("SHIT.png"))
    os.system("rm SHIT.png")
    await ctx.message.delete()

@bot.command()
async def perms(ctx, user: discord.Member = None):
        ': Find what you can do on this server'
        user = ctx.message.author if user is None else user
        if not user:
            user = ctx.author
        mess = []
        for i in user.guild_permissions:
            if i[1]:
                mess.append("\u2705 {}".format(i[0]))
            else:
                mess.append("\u274C {}".format(i[0]))
        embed = discord.Embed(title = f'''{user.name} 's permissions in the server are: ''',description ="\n".join(mess), color = discord.Colour.blue())
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def avatar(ctx, user: discord.Member = None):
        """: Check AVATARS"""
        user = user or ctx.message.author
        embed = discord.Embed(title=f'''{user.name}'s Avatar''', description=f'''{user.name} looks like.....''',color=discord.Colour.blue())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """: Checks the bots ping"""
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"My ping is {ping}ms")

@bot.command()
async def vote(ctx, *, msg):
    """: Starts a vote poll"""
    message = await ctx.send(msg)
    await message.add_reaction(emoji="👍")
    await message.add_reaction(emoji="👎")
    await ctx.message.delete()

@bot.command()
async def user(ctx, member:discord.User = None):
    """: Shows info on yourself"""
    if member == None:
        member = ctx.message.author
        pronoun = "Your"
    else:
        pronoun = "Their"
    name = f"{member.name}#{member.discriminator}"
    status = member.status
    joined = member.joined_at
    await ctx.channel.send(f"{pronoun} name is {name}. {pronoun} status is {status}. They joined at {joined}.")

bot.run("NTI2MzI1NDU2MjkxNjI3MDEw.DwDibQ.l5_sLXOjlzp1x_ZPLNK_R3cvUQo")
