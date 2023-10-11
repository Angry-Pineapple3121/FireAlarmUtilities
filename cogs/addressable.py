import discord
import datetime

from discord.ext import commands
from discord.commands import Option

from PIL import Image, ImageDraw, ImageFont

BOT_VERSION = open('version').read()

class Addressable(commands.Cog):
    print('★ Loaded cog: Simplex Addressable Visualizer')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def visualaddress(
        self,
        ctx,
        address: Option(int, 'The address (1-255) you\'d like to visualize.', required=True, min=1, max=255),
    ):
        """Visualize an address on a Simplex MAPNET or IDNet module."""
        requestTime = datetime.datetime.now()
        print(f'[{requestTime}] [Addressable Visualizer] Requested by {ctx.author} (ID: {ctx.author.id})')

        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
        else:
            try:
                embed = discord.Embed(
                    title=f"<:slash:1150933397179486339> Simplex Addressable Visualizer",
                    description=f'Finished generating image for address **{address}**.',
                    color=discord.Colour.green(),
                )

                addressb = f'{address:b}'

                now = datetime.datetime.now()
                rtime = now.strftime("%B %d, %Y, %H:%M")
                embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")

                #embed.add_field(name=f"SLC Limitations", value=f'<:greendot:1129631441286873138> MAPNET II SLCs can support up to **127** devices per loop. IDNet SLCs can support up to **250** devices per loop.', inline=False)

                # Set image dimensions
                width = 300
                height = 150

                # Set padding and switch dimensions
                padding = 25
                switch_width = 25
                switch_height = 50
                spacing = 10

                # Calculate the total width of the switches and spacing
                total_switch_width = (switch_width + spacing) * 8 - spacing

                # Calculate the starting x-coordinate for the switches
                start_x = (width - total_switch_width) // 2

                # Calculate the starting y-coordinate for the switches
                start_y = (height - switch_height) // 2

                # Binary number representation
                binary_number = addressb[::-1]

                # Create a new blank image with gray background
                image = Image.new('RGB', (width, height), 'gray')

                # Create a drawing object
                draw = ImageDraw.Draw(image)

                # Create a font object for the switch labels
                font = ImageFont.truetype('ARIAL.TTF', 12)

                # Draw the switches based on the binary number
                for i in range(8):
                    # Calculate switch position
                    switch_left = start_x + i * (switch_width + spacing)
                    switch_right = switch_left + switch_width
                    switch_top = start_y
                    switch_bottom = switch_top + switch_height

                    # Determine switch state (ON/OFF)
                    if i < len(binary_number) and binary_number[i] == '1':
                        switch_fill = 'white'  # ON position
                    else:
                        switch_fill = 'beige'  # OFF position

                    if switch_fill == 'white':
                        draw.rectangle([(switch_left, switch_top), (switch_right, (switch_bottom + switch_top) // 2)],
                                       outline='black', fill=switch_fill)
                    else:
                        draw.rectangle([(switch_left, (switch_bottom + switch_top) // 2), (switch_right, switch_bottom)],
                                       outline='black', fill=switch_fill)

                    # Draw the switch number
                    number = str(i + 1)
                    number_width, number_height = draw.textsize(number, font=font)
                    number_x = switch_left + (switch_width - number_width) // 2
                    number_y = switch_bottom + 5  # Padding below the switch
                    draw.text((number_x, number_y), number, fill='black', font=font)

                # Indicate on/off to the left
                draw.text((1, 57), 'ON')
                draw.text((1, 85), 'OFF')

                # Save the image
                image.save('switches.png')

                await ctx.respond(embed=embed, files=[discord.File('switches.png')])
            except Exception as e:
                await ctx.respond('<:warn:1105998033335898162> An error occurred when processing your command. Please contact `Angry_Pineapple#6926` with what you were attempting to do, along with the date and time.', ephemeral=True)
                print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                pass

def setup(bot):
    bot.add_cog(Addressable(bot))