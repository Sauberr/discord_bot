import discord
from discord.ext import commands
import datetime
import asyncio
from datetime import datetime, timedelta
import requests

TOKEN = 'Your Token Bot'

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

#Bot Status
@client.event
async def on_ready():
    await client.tree.sync()
    print('Bot Kesha connected to the server')

    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))


# SLash Commands
@client.tree.command(name='ping', description="Shows bot's latency in ms ")
async def ping(interaction:discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong {bot_latency} ms.")



# Hi
@client.command()
async def hi(ctx:commands.Context):
    author = ctx.message.author
    await ctx.send(f" **{author}** Hi, I'm a bot at this Discord Server.")

# Clear message
    @client.command()
    @commands.has_permissions(administrator=True)
    async def clear(ctx, amount=11):
        await ctx.channel.purge(limit=amount)



# Kick
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    await member.kick(reason=reason)
    emb = discord.Embed(description=f":bomb: User **{member.name}** banned!",color=discord.Color(value=int('FF8C00', 16)))
    emb.add_field(name='Moderator', value=ctx.message.author.mention)
    emb.add_field(name='Reason', value='Not specified')
    await ctx.send(embed=emb)

# Ban
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)
    emb = discord.Embed(description=f":bomb: User **{member.name}** banned!",color=discord.Color(value=int('FF8C00', 16)))
    emb.add_field(name='Moderator', value=ctx.message.author.mention)
    emb.add_field(name='Reason', value='Not specified')
    await ctx.send(embed=emb)


# Unban
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, id):
    user = await client.fetch_user(id)
    emb = discord.Embed(description=f"Unban **{user}**", color=0xFF8C00, timestamp=datetime.now())
    emb.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
    try:
        await ctx.guild.unban(user)
        await ctx.send(embed=emb)
    except:
        emb = discord.Embed(title='Error!', description=f'This user is not banned or I do not have enough rights to execute this command!', color=discord.Color(value=int('FF8C00', 16)))
        await ctx.send(embed=emb)

# Catching errors
@client.event
async def on_command_error(ctx, error):
    emb = discord.Embed(title='Not enough rights', colour=discord.Color.orange())
    if isinstance(error, commands.MissingPermissions):
        emb.add_field(name='Rights', value=f"**{ctx.author.name}** don't have enough rights")
        return ctx.send(embed=emb)
    embed = discord.Embed(title=":warning: Unknown error!", description="**An unknown error has occurred!**", color=0xff0000)
    embed.add_field(name="Error", value=f"**```yaml\n{error}\n```**", inline=False)
    embed.set_footer(text="Please contact the developer to fix this bug.")
    await ctx.send(embed=embed)

# Help
@client.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
    emb = discord.Embed(title='Server command navigation', colour=discord.Color.orange())
    emb.add_field(name='**Clear**', value='Clear chat', inline = False)
    emb.add_field(name='**Ban**', value='Ban user', inline = False)
    emb.add_field(name='**Unban**', value='Unban user', inline = False)
    emb.add_field(name='**Kick**', value='Kick user', inline = False)
    emb.add_field(name='**Mute**', value='Mute user', inline = False)
    emb.add_field(name='**Unmute**', value='Unmute user', inline = False)
    emb.add_field(name='**Tempban**', value='Tempban user', inline=False)
    emb.add_field(name='**On_join**', value='Join to user', inline=False)
    emb.add_field(name='**Cat**', value='Fluffy cats images', inline=False)
    emb.add_field(name='**Dog**', value='Fluffy dogs images', inline=False)
    emb.add_field(name='**Userinfo**', value='UserInformation', inline=False)
    await ctx.send(embed=emb)

#Mute
@client.command(aliases=["m"])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, arg: str = None, *, reason=None):
    if ctx.author.top_role.position < member.top_role.position:
        errmute=discord.Embed(title='Error!',description='You cannot apply this command to yourself or another moderator', color = discord.Color(value = int('FF8C00', 16)))
        return await ctx.send(embed=errmute)
    if ctx.author.top_role.position == member.top_role.position:
        errmutee=discord.Embed(title='Error!',description='You cannot apply this command to yourself or another moderator', color=discord.Color(value = int('FF8C00', 16)))
        return await ctx.send(embed=errmutee)
    amount = int(arg[:-1])
    tip = arg[-1]
    now = datetime.now()
    muterole = discord.utils.get(ctx.guild.roles, id=1079816045973487768)
    if tip == "s":
        if reason is None:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!", color=discord.Color(value=int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline = False)
            emb.add_field(name='Reason', value='Not specified', inline = False)
            emb.add_field(name='Time', value=f"{str(amount)} sec", inline = False)
            delta = timedelta(seconds=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason = f"{ctx.author}: Not specified", atomic=True)
        else:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!", color=discord.Color(value=int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline=False)
            emb.add_field(name='Reason', value=reason, inline = False)
            emb.add_field(name='Time', value=f'{amount} sec.', inline = False)
            delta = timedelta(seconds=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason= f"{ctx.author}: {reason}", atomic = True)
        await ctx.send(embed=emb)
        await asyncio.sleep(amount)
        await member.remove_roles(muterole)
    if tip == "m":
        if reason is None:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!",color = discord.Color(value=int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline = False)
            emb.add_field(name='Reason', value='Not specified', inline=False)
            emb.add_field(name='Time', value=f'{amount} min.', inline=False)
            delta = timedelta(minutes=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason=f"{ctx.author}: Not specified", atomic = True)
        else:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!",color = discord.Color(value=int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline=False)
            emb.add_field(name='Reason', value=reason,inline = False)
            emb.add_field(name='Time', value=f'{amount} min.',inline = False)
            delta = timedelta(minutes=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason=f"{ctx.author}: {reason}", atomic = True)
        await ctx.send(embed = emb)
        await asyncio.sleep(amount * 60)
        await member.remove_roles(muterole)
    if tip == "h":
        if reason is None:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!",color = discord.Color(value=int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention,inline = False)
            emb.add_field(name='Reason', value='Not specified',inline = False)
            emb.add_field(name='Time', value=f'{amount} hours.',inline = False)
            delta = timedelta(hours=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason=f"{ctx.author}: Not specified", atomic = True)
        else:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!", color = discord.Color(value = int('FF8C00', 16)))
            emb.add_field(name='Moderator',value=ctx.message.author.mention,inline = False)
            emb.add_field(name='Reason',value=reason,inline = False)
            emb.add_field(name='Time',value=f'{amount} hours.',inline = False)
            delta = timedelta(hours=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason = f"{ctx.author}: {reason}", atomic = True)
        await ctx.send(embed = emb)
        await asyncio.sleep(amount * 3600)
        await member.remove_roles(muterole)
    if tip == "d":
        if reason is None:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!", color = discord.Color(value = int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline=False)
            emb.add_field(name='Reason', value='Not specified', inline=False)
            emb.add_field(name='Time', value=f'{amount} days.', inline=False)
            delta = timedelta(days=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline = False)
            await member.add_roles(muterole, reason=f"{ctx.author}: Not specified", atomic=True)
        else:
            emb = discord.Embed(description=f":white_check_mark: User **{member.name}** muted!", color = discord.Color(value = int('FF8C00', 16)))
            emb.add_field(name='Moderator', value=ctx.message.author.mention, inline=False)
            emb.add_field(name='Reason', value=reason, inline=False)
            emb.add_field(name='Time', value=f'{amount} days.')
            delta = timedelta(days=amount)
            future = now + delta
            new_time = future.replace(microsecond=0)
            emb.add_field(name='Unmute', value=new_time, inline=False)
        await ctx.send(embed = emb)
        await asyncio.sleep(amount * 86400)
        await member.remove_roles(muterole)

# Unmute
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
    await member.remove_roles(mute_role)
    emb = discord.Embed(description=f"Unmute **{member.mention}**", color=0xFF8C00, timestamp=datetime.now())
    emb.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
    await ctx.send(embed=emb)

# Join_number
@client.event
async def on_member_join(member:discord.Member):
    channel = client.get_channel(776157974179217451)
    role = discord.utils.get(member.guild.roles, id=1079886008981655583)
    emb = discord.Embed(description=f"**{member.name}** joined to us", color=0xFF8C00, timestamp=datetime.now())
    await channel.send(embed=emb)
    await member.add_roles(role)

# Duration
class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return (int(amount), unit)

        raise commands.BadArgument(message='Not a valid duration')

# Tempban
@client.command()
async def tempban(ctx, member: commands.MemberConverter, duration:DurationConverter):
    multiplier = {'s': 1, 'm': 60}
    amount, unit = duration
    emb = discord.Embed(description=f':bomb: {member} has been banned for {amount}{unit}.**!', color=discord.Color(value=int('FF8C00', 16)))
    emb.add_field(name='Moderator', value=ctx.message.author.mention)
    emb.add_field(name='Reason', value='Not specified')
    await ctx.guild.ban(member)
    await asyncio.sleep(amount * multiplier[unit])
    await ctx.guild.unban(member)
    await ctx.send(embed=emb)

# Join to member
@client.command()
async def on_join(ctx, member: discord.Member):
    channel = member.voice.channel
    await channel.connect()
    await ctx.author.move_to(channel)

# Random cats images
@client.command()
async def cat(ctx):
    cat_api = 'Your key api'
    response = requests.get('https://api.thecatapi.com/v1/images/search?&api_key=' + cat_api)
    json_data = response.json()
    emb = discord.Embed(title=':cat:', color=0xFF8C00)
    emb.set_image(url=json_data[0]["url"])
    await ctx.send(embed=emb)

# Random dogs images
@client.command()
async def dog(ctx):
    dog_api = 'Your key api'
    response = requests.get('https://api.thedogapi.com/v1/images/search?api_key=' + dog_api)
    json_data = response.json()
    emb = discord.Embed(title=':dog:', color=0xFF8C00)
    emb.set_image(url=json_data[0]['url'])
    await ctx.send(embed=emb)

# UserInfo
@client.command()
async def userinfo(ctx, member:discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    info_embed = discord.Embed(title=f"{member.name}'s User Information", description='All information about this user', color=discord.Color(value=int('FF8C00', 16)))
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name='Name', value=member.name, inline=False)
    info_embed.add_field(name='Nick Name', value=member.display_name, inline=False)
    info_embed.add_field(name='Discriminator', value=member.discriminator, inline=False)
    info_embed.add_field(name='ID', value=member.id, inline=False)
    info_embed.add_field(name='Top Role', value=member.top_role, inline=False)
    info_embed.add_field(name='Status', value=member.status, inline=False)
    info_embed.add_field(name='Creation Date', value=member.created_at.__format__("%A, %d. %B %Y | %H:%M:%S"), inline=False)
    await ctx.send(embed=info_embed)


client.run(TOKEN)


