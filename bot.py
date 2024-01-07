import discord
import datetime
import os
import psutil

AUTH_TOKEN = open('access')
AUTH_TOKEN = AUTH_TOKEN.read()

BOT_VERSION = open('version').read()

process = psutil.Process()

cogs_list = [
    'simplexmnc',
    'addressable',
    'datasheetreference',
    'aucpreview',
    'multitone',
    'password'
]

bot = discord.Bot()

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

class InvLink(discord.ui.View):
    def __init__(self, invlink: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite Link", url=invlink, emoji="🔗"))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Simplex 4100ES'))
    print('■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■')
    print('Fire Alarm Community Utility - Written by Angry_Pineapple')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f' - Bot revision: {BOT_VERSION}')
    print('■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■')


@bot.command(description="Sends the bot's latency.")
async def latency(ctx):
    with open('blacklist', 'r') as file:
        GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
    
    if ctx.author.id in GLOBAL_BLACKLIST:
        await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
        print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
    else:
        botLatency = round(bot.latency, 2)
        botLatencyMs = round(bot.latency * 1000, 2)
        await ctx.respond(f":hourglass: Pong! Latency is **{botLatency}** seconds (**{botLatencyMs}** ms)")

@bot.command(description="Invite the bot to your server.")
async def inviteme(ctx):
    with open('blacklist', 'r') as file:
        GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
        
    if ctx.author.id in GLOBAL_BLACKLIST:
        await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
        print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
    else:
        embed = discord.Embed(
            title=f"<:simplex:1092988498736320513> Invite the bot to your server!",
            description=f'<:yellowcheck:1091497847846879324> Open the prompt below and select the server \nyou\'d like to invite the bot to, then press **Authorize**.',
            color=discord.Colour.yellow(),
        )

        now = datetime.datetime.now()
        rtime = now.strftime("%B %d, %Y, %H:%M")
        embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")

        await ctx.respond(embed=embed, view=InvLink('https://discord.com/oauth2/authorize?scope=bot+applications.commands&client_id=1139717804396908595'))

@bot.command(name="botinfo", description="Get bot information and statistics.")
async def botinfo(ctx):
    with open('administrators', 'r') as file:
        GLOBAL_ADMINISTRATORS = [int(line.strip()) for line in file if line.strip()]
        
    if ctx.author.id not in GLOBAL_ADMINISTRATORS:
        await ctx.respond('<:warn:1105998033335898162> You do not have permission to use this command.', ephemeral=True)
        print(f'[{datetime.datetime.now()}] [No Permissions] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they do not have permission to use.')
    else:
        amount = 0
        bot_channels = 0
        members = 0
        guild_info = ''

        for guild in bot.guilds:
            amount += 1
            bot_channels += len(guild.channels)
            members += guild.member_count
            guild_info += f" <:greendot:1129631441286873138> **{guild.name}** - {guild.member_count} Members\n"

        process_create_time = datetime.datetime.fromtimestamp(process.create_time())
        current_time = datetime.datetime.now()
        time_difference = current_time - process_create_time
        
        rounded_seconds = round(time_difference.total_seconds())
        rounded_timedelta = datetime.timedelta(seconds=rounded_seconds)
        
        embed = discord.Embed(
            title="<:simplex:1092988498736320513> Fire Alarm Utilities Bot Info",
            description=f"**Service Information**\n <:greendot:1129631441286873138> Guilds: **{amount}** \n <:greendot:1129631441286873138> Total Channels: **{bot_channels}** \n <:greendot:1129631441286873138> Serving **{members}** members \n\n **Bot Guild Information**\n {guild_info}\n **System Information**\n <:greendot:1129631441286873138> CPU Usage: **{psutil.cpu_percent()}%** \n <:greendot:1129631441286873138> Memory Usage: **{round(process.memory_info().rss / 1024 / 1024, 2)} MB** \n <:greendot:1129631441286873138> Uptime: **{rounded_timedelta}**\n <:greendot:1129631441286873138> Bot Firmware: **{BOT_VERSION}**\n <:greendot:1129631441286873138> DynamiX Firmware: **0.1-ALPHA**",
            color=discord.Color.green()
        )

        now = datetime.datetime.now()
        rtime = now.strftime("%B %d, %Y, %H:%M")
        embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")

        await ctx.respond(embed=embed)

@bot.command(name="blacklist", description="Blacklist a user from using the bot.")
async def blacklist(ctx, user: discord.User):
    with open('administrators', 'r') as file:
        GLOBAL_ADMINISTRATORS = [int(line.strip()) for line in file if line.strip()]
        
    if ctx.author.id not in GLOBAL_ADMINISTRATORS:
        await ctx.respond('<:warn:1105998033335898162> You do not have permission to use this command.', ephemeral=True)
        print(f'[{datetime.datetime.now()}] [No Permissions] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they do not have permission to use.')
    else:
        with open('blacklist', 'a') as f:
            f.write(f'\n{user.id}')

        embed = discord.Embed(
                title=f"",
                description=f'<:check:1081988275851513919> **{user}** (ID: **{user.id}**) has been blacklisted from using the bot.',
                color=discord.Colour.green(),
            )
        
        await ctx.respond(embed=embed)

@bot.command(name="unblacklist", description="Remove a user's blacklist status.")
async def unblacklist(ctx, user: discord.User):
    with open('administrators', 'r') as file:
        GLOBAL_ADMINISTRATORS = [int(line.strip()) for line in file if line.strip()]
        
    if ctx.author.id not in GLOBAL_ADMINISTRATORS:
        await ctx.respond('<:warn:1105998033335898162> You do not have permission to use this command.', ephemeral=True)
        print(f'[{datetime.datetime.now()}] [No Permissions] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they do not have permission to use.')
    else:
        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
        
        if user.id in GLOBAL_BLACKLIST:
            with open('blacklist', 'r') as f:
                lines = f.readlines()
            with open('blacklist', 'w') as f:
                for line in lines:
                    if line.strip("\n") != str(user.id):
                        f.write(line)
            embed = discord.Embed(
                title=f"",
                description=f'<:check:1081988275851513919> **{user}** (ID: **{user.id}**) has been removed from the blacklist',
                color=discord.Colour.green(),
            )
        
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title=f"",
                description=f'<:X_:1152069831638650890> **{user}** (ID: **{user.id}**) is not blacklisted.',
                color=discord.Colour.red(),
            )
        
            await ctx.respond(embed=embed)


@bot.command(name="enroll", description="Enroll into experimental features coming to the bot. NOTE! Features might be removed at any time!")
async def enroll(ctx):
    with open('enrolled', 'a+') as f:
        f.seek(0)
        if str(ctx.author.id) in f.read():
            await ctx.respond('<:warn:1105998033335898162> You are already enrolled into experimental features!', ephemeral=True)
        else:
            f.write(f'\n{ctx.author.id}')

            embed = discord.Embed(
                    title=f"",
                    description=f'<:check:1081988275851513919> You have successfully enrolled into access to experimental features!\n\n <:warn:1105998033335898162> **Experimental features are not guaranteed to work, and may be removed at any time.**',
                    color=discord.Colour.green(),
                )

            await ctx.respond(embed=embed)

bot.run(AUTH_TOKEN)
