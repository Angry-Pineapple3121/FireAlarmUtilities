import discord
import datetime
import glob
import re

from discord.ext import commands
from discord.commands import Option

BOT_VERSION = open('version').read()

# initialize the device lists for each type of device
file_pattern = 'model_data/devices/*.txt'
file_list = glob.glob(file_pattern) # Get a list of all files matching the pattern

devicetype = {}

for file_path in file_list:
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read the content and remove leading/trailing whitespace
        filename = file_path.split('/')[-1]  # Extract the filename from the file path
        devicetype[filename] = content

# setup the master list for autocomplete
MASTER_LIST = []

with open ('model_data/all_models.txt', 'r') as f:
    for line in f:
        MASTER_LIST.append(line.strip())

async def get_model(ctx: discord.AutocompleteContext):
    """Returns a list of models that start with the given value."""
    search_value = ctx.value.lower()  # Convert to lowercase for case-insensitive search
    matching_models = [model for model in MASTER_LIST if model.lower().startswith(search_value)]

    return matching_models

class SimplexMNC(commands.Cog):
    print('★ Loaded cog: Simplex Model Number Checker')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def simplexmnc(
        self,
        ctx,
        model: Option(str, 'The model number of the Simplex device you want to check.', required=True, autocomplete=get_model),
    ):
        """Checks which type of Simplex device a model number is."""
        requestTime = datetime.datetime.now()
        print(f'[{requestTime}] [Simplex MNC] Requested by {ctx.author} (ID: {ctx.author.id}) with model number {model}')

        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
        else:
            try:
                embed = discord.Embed(
                    title=f"<:slash:1150933397179486339> Simplex Model Number Checker",
                    description=f'Finished checking model number **{model}**.',
                    color=discord.Colour.red(),
                )
    
                now = datetime.datetime.now()
                rtime = now.strftime("%B %d, %Y, %H:%M")
                embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")
    
                # regex for normal & es models
                normalRegex = '[0-9]{4}-[0-9]{4}'
                esRegex = '^[0-9A-Z]+(?:-[A-Z]+)*(?:-[A-Z]+-[A-Z]+)?(?:-[A-Z]+)?$'
                
                # we want to check if the model number is a valid 'normalRegex' model or 'esRegex' model
                if not re.match(normalRegex, model) and not re.match(esRegex, model):
                    await ctx.respond('<:warn:1105998033335898162> The model number you entered is not in the model number database.', ephemeral=True)
                    return 
                
                # horrible code coming!!!
                if model in devicetype['truenac.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```TrueNAC```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```Requires any Simplex panel which can support addressable notification (IDNAC is backwards-compatible). Can also be used with a TrueAlert Addressable Controller.```', inline=False)
                    await ctx.respond(embed=embed)
                elif model in devicetype['es.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```ES Addressable```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```Requires a modern Simplex panel with IDNAC that can support TrueAlertES addressable devices.```', inline=False)
                    await ctx.respond(embed=embed)
                elif model in devicetype['freerun.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```Free Run```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```Doesn\'t require any special panels or tools to run, only 24 volts DC.```', inline=False)
                    await ctx.respond(embed=embed)
                elif model in devicetype['selectable.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```Selectable```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```The user can choose to use the device in free run mode or in SmartSync mode using a switch located on the front of the unit.```', inline=False)
                    await ctx.respond(embed=embed)
                elif model in devicetype['smartsync.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```SmartSync```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```Requires a SmartSync compatible controller to operate. Examples of this are Simplex panels with QALERT NAC setting, a SmartSync module, 4009 IDNet NAC Extender, or Collectors Controls DUSMC.```', inline=False)                
                    await ctx.respond(embed=embed)
                elif model in devicetype['syncable.txt']:
                    embed.add_field(name=f"<:simplex:1092988498736320513> Device Type", value=f'```Syncable```', inline=True)
                    embed.add_field(name=f":information_source: Categorization Information", value=f'```Horn will operate when power is applied, but the strobe will flash only when power is removed.```', inline=False)
                    await ctx.respond(embed=embed)
                
                #embed.add_field(name=f"Important Note", value=f'<:reddot:1106010327662993549> Avoid running modern Simplex devices on FWR, filtered DC is advised. Running TrueAlert devices on FWR may damage them.', inline=False)
    
                else:
                    await ctx.respond('Sorry, but I couldn\'t find the data for that model number. I only have data for **Simplex TrueAlert** devices.', ephemeral=True)
            except Exception as e:
                await ctx.respond('<:warn:1105998033335898162> An error occurred when processing your command. Please contact `Angry_Pineapple#6926` with what you were attempting to do, along with the date and time.', ephemeral=True)
                print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                pass

def setup(bot):
    bot.add_cog(SimplexMNC(bot))