import discord
import datetime
import json

from discord.ext import commands
from discord.commands import Option

BOT_VERSION = open('version').read()

class Multitone(commands.Cog):
    print('★ Loaded cog: Multitone Settings Database')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def multitone(
        self,
        ctx,
        device: Option(str, 'The type of device you want to return settings for.', required=True, choices=['Commander 2 or 3', 'Siemens UMMT', 'Wheelock MT', 'System Sensor MA (ADA)', 'System Sensor MAEH (ADA)', 'Gentex GOS or GOT', 'Collectors Controls DUSMC'])
    ):
        """Show all of the settings for a multi-tone fire alarm device."""
        requestTime = datetime.datetime.now()
        print(f'[{requestTime}] [Multitone Settings] Requested by {ctx.author} (ID: {ctx.author.id})')

        # filter out those stupid blacklisted users
        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
        else:
            try:
                embed = discord.Embed(
                    title=f"<:slash:1150933397179486339> Multi-tone Device Settings Lookup",
                    description=f'Displaying all possible tone settings for **{device}**.',
                    color=discord.Colour.green(),
                )

                # open and load the json file to get the data we need
                settings = json.load(open('model_data/device_tones.json'))

                # theoretically this should never get passed invalid data but fuck it ship it
                embed.add_field(name="📝 Device-Specific Information", value=f'```{settings[device]["device_note"]}```', inline=False)
                embed.add_field(name="🚥 Displayed Layout", value=f'```{settings[device]["display_param"]}```', inline=False)

                # support for the 3 devices that use switches
                if device in ['Commander 2 or 3', 'Siemens UMMT', 'Wheelock MT', 'Collectors Controls DUSMC']:
                    # loop through the settings and add them to the embed
                    for setting_type, setting_data in settings[device]["settings"].items():
                        switches = setting_data["switches"]
                        switch_statuses = [status for switch, status in switches.items()]

                        embed.add_field(name=f"» {setting_type}", value=f'```{" ".join(switch_statuses)}```', inline=True)
                
                # support for system sensor shit because they like to be special
                if device in ['System Sensor MA (ADA)', 'System Sensor MAEH (ADA)']:
                    for setting_type, setting_data in settings[device]["settings"].items():
                        tabs = setting_data["clipped_tabs"]

                        embed.add_field(name=f"» {setting_type}", value=f'```{(tabs)}```', inline=True)

                # gentex also likes to be different so they get the same treatment
                if device in ['Gentex GOS or GOT']:
                    for setting_type, setting_data in settings[device]["settings"].items():
                        jumpers = setting_data["removed_jumpers"]

                        embed.add_field(name=f"» {setting_type}", value=f'```{(jumpers)}```', inline=True)

                now = datetime.datetime.now()
                rtime = now.strftime("%B %d, %Y, %H:%M")
                embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")

                await ctx.respond(embed=embed)
            except Exception as e:
                await ctx.respond('<:warn:1105998033335898162> An error occurred when processing your command. Please contact `Angry_Pineapple#6926` with what you were attempting to do, along with the date and time.', ephemeral=True)
                print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                pass

def setup(bot):
    bot.add_cog(Multitone(bot))