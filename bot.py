import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands, Colour
import time
import json
import os
import io
import socket
import pandas as pd
import aiohttp
import re
import asyncio
from collections import Counter
import numpy as np
from client_run import NORMAL_BOT_KEY
cogs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')

GUILD_ID = 462106215007256576 

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_file_path = None
        self.cog_folder = None
    async def on_ready(self):
        print(f'Logged on as {self.user} \n {time.strftime(("[%d/%m/%Y, %I:%M:%S %p ET]"))}')
        await self.tree.sync()
        try:
            guild = discord.Object(id=GUILD_ID)
            sync = await self.tree.sync(guild=guild)
            print(f'Synced {len(sync)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing command: {e}')
        game = discord.Game("Combines")
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your concerns"))
    async def on_command_error(self, ctx, error):
        user = ctx.message.author
        await ctx.send(error)
        print(f'[{user.guild}]', f'{time.strftime(("[%d/%m/%Y, %I:%M:%S %p ET]"))}', error)


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  
intents.members = True
client = Client(command_prefix="!", intents=intents)
guild = discord.Object(id=GUILD_ID)

@client.tree.command(name='hello', description='Says Hello', guild=guild)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello There!")

@client.tree.command(name='exhaust', description='Shows the stock exhaust system', guild=guild)
async def exhaust(interaction: discord.Interaction):
        with open('ms3exhaust.jpg', 'rb') as f:
            picture = discord.File(f)
        await interaction.response.send_message(f"Heres photo of exhaust - ")
        await interaction.followup.send(file=discord.File('ms3exhaust.jpg'))

@client.tree.command(name='suspension', description='Asks what suspension you should use', guild=guild)
async def suspension(interaction: discord.Interaction):
    embed = discord.Embed(
        title="What's the best suspension for Mazdaspeed!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Best for Lowering and bad road performance", value="Raceland, Godspeed, Maxspeedingrods", inline=True)
    embed.add_field(name="Decent Suspension:", value="Graveyard Performance, BC Racing, Tein, Scale \nShocks: Koni, KYB, Bilstein \nCoils: H&R, Eibach, Corksport, Tein, Swift Sport Spec-R,", inline=True)
    embed.add_field(name="Good Coilovers:", value="Fortune Auto, KW", inline=True)
    embed.add_field(name="Suspension forum:", value="https://mazdaspeeds.org/index.php?threads/the-official-ms3-suspension-thread.15531/", inline=False)
    embed.set_footer(text="These are based off of previous people's feels to each suspension setup, and overall build quality. Less quality will always result in lower street and track performance and better suspension will always have superior adjustability. Please visit forum for more info")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name='turbos', description='Asks what turbo you should use and for what application', guild=guild)
async def turbos(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="What's the best turbo for Mazdaspeed!",
        color=discord.Color.red()
    )
    embed.add_field(name="Stock type performance", value="K04 - OEM \nBNR S1 - OEM equivelent \nBNR S2 - Almost OEM replacement, slightly bigger and better flow", inline=False)
    embed.add_field(name="Slightly bigger", value="BNR S3 - Higher flow rate, better design and power until redline \nCTS4 - Same type as BNR, But takes slightly longer to spool", inline=False)
    embed.add_field(name="Bigger", value="CTS5 - Not recommended, anything higher than BNR S4 or CTS4 it's better to go to Garrett or other turbos", inline=False)
    embed.set_footer(text="Note: BNR S4 will be better in saving your engine if you do not have port injection as the torque will be applied around 1000rpm later, therefore saving your rods.")
    await interaction.followup.send(embed=embed)

@client.tree.command(name='buy_turbos', description='Purchasing turbos', guild=guild)
async def buyturbos(interaction: discord.Interaction):
    BNR_website = "https://bnrturbos.com/collections/mazdaspeed-3-6"
    CS_website = "https://corksport.com/mazdaspeed-3/2010-2013-mazdaspeed-3/2010ms3-power/turbo-system-parts/page-2/"
    await interaction.response.send_message(f"BNR's Website: <{BNR_website}>, \nCorksport's Website: <{CS_website}>")

@client.tree.command(name="vendors", description='Vendors to use when buying parts for Mazdaspeed components', guild=guild)
async def vendors(interaction: discord.Interaction):
    CW_Turbo = "https://www.cwturbochargers.com/"
    Graveyard = "https://www.graveyardperformance.com/"
    DamondMT = "https://damondmotorsports.com/"
    CS = "https://corksport.com/"
    #forte = discord.Member.id(267147762615713793)
    embed = discord.Embed(
        title="Vendors for Mazdaspeed's",
        color=discord.Color.blue()
    )
    embed.add_field(name="Graveyard Performance", value=f"Contact Forte or their website: {Graveyard}", inline=False)
    embed.add_field(name="CW Turbochargers", value=f"Canadian Company, website is: {CW_Turbo}", inline=False)
    embed.add_field(name="Corksport", value=f"Website is: {CS}", inline=False)
    embed.add_field(name="Damond Motorsport", value=f"Website is: {DamondMT}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="manual", description="Manual for Mazdaspeeds", guild=guild)
async def manuals(interaction=discord.Interaction):
    embed = discord.Embed(
        title="Manuals for Mazdaspeeds",
        color=discord.Color.blue()
    )
    ms6 = "https://www.mazdausa.com/siteassets/pdf/owners-optimized/2006/mazdaspeed6/2006-mazdaspeed6-owners-manual.pdf?msockid=3f96a76bfb4167592defb12ffa6e66a0"
    m307 = "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2007_mazdaspeed3_manual_en_optimized.pdf" 
    m308= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2008_mazdaspeed3_manual_en_optimized.pdf"
    m309= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2009_mazdaspeed3_manual_en_optimized.pdf"
    m3010= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2010_mazdaspeed3_manual_en_optimized.pdf"
    m3011= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2011_mazdaspeed3_manual_en_optimized.pdf"
    m3012= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2012_mazdaspeed3_manual_en_optimized.pdf"
    m3013= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2013_mazdaspeed3_manual_en_optimized.pdf"
    embed.add_field(name="Mazdaspeed 6", value=ms6, inline=False)
    embed.add_field(name="Mazdaspeed 3", value=f"2007:{m307} \n2008: {m308} \n2009: {m309} \n2010: {m3010} \n2011: {m3011} \n2012: {m3012} \n2013: {m3013}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="maintenance", description="Recommended Maintenance Schedule", guild=guild)
async def maintenance(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Maintenance Schedule for Mazdaspeeds",
        color=discord.Color.blue()
    )
    embed.add_field(name="3,000 Miles (5,000km)", value="Oil Change \nInspect Fluids \nLook for Leaks", inline=False)
    embed.add_field(name="15,000 miles (25,000km)", value="Change / Clean air filters \nchange brake fluid", inline=False)
    embed.add_field(name="30,000 Miles (50,000km)", value="Check / Replace Spark Plugs (Do Compression test since you are there) \nDrain and Fill Transmission Fluid \n Coolant flush", inline=False)
    embed.add_field(name="50,000 Miles (80,000km) and or\n100,000 Miles (160,000km)", value="Valve Cleaning \nInjector Cleaning / Flow Test \nVVT Check for 07-10 and early model 11's", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="tunefreemods", description="Modifications that do not require a tune on the vehicle", guild=guild)
async def tunefreemods(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Tune Free Mods",
        color=discord.Colour.green()
    )
    embed.add_field(name="Catch Can / PCV Plate", value="", inline=False)
    embed.add_field(name="BPV / Dual Port BPV / BOV", value="A Blow Off Valve will cause your car to run rich when decelerating or shifting, tuners are unable to tune for BOV's", inline=False)    
    embed.add_field(name="Motor Mounts", value="These are highly recommended. Damond or Corksport are good, but Damond has less NVH and may ride better", inline=False)
    embed.add_field(name="Catback / Axleback exhaust system", value="", inline=False)
    embed.add_field(name="Short Throw Shifter / Short Shift Plate", value="Short Shift Plate is not recommended as it can possibly strecth the shifting cables", inline=False)
    embed.add_field(name="Drop in Air Filter", value="", inline=False)
    await interaction.response.send_message(embed=embed)
    # embed.add_field(name="", value="", inline=False)

@client.tree.command(name="tuners", description="List of Tuners who know the platform", guild=guild)
async def tuners(interaction: discord.Interaction):
    speedwiz = 744994903611670538
    embed = discord.Embed(
        title="List of Tuners",
        description="Please use these tuners because the mentioned are knowledgeable with the platform. You can NOT tune these yourself with EcuTek but you can with Versatune. If you are looking to tune your Mazdaspeed, the available tuning options are COBB Accessport, Versatune, and ECUTEK which is no longer supported.",
        colour= discord.Colour.magenta(),
        url="https://mazdaspeeds.org/index.php"
    )
    embed.add_field(name="FreekTune", value="https://www.freektune.com/collections/mazdaspeed/e-tune", inline=False)
    embed.add_field(name="PD Tuning", value="https://www.pd-tuning.com/tuning-request/", inline=False)
    embed.add_field(name="Damond Motorsport", value="https://damondmotorsports.com/collections/tuning", inline=False)
    embed.add_field(name="Stratified Tuning", value="https://www.stratifiedauto.com/index.php?main_page=index&cPath=87", inline=False)
    embed.add_field(name="Edge Autosport", value="https://edgeautosport.com/edge-autosport-etune-mazdaspeed-3-2007-2013-mazdaspeed-6-2006-2007/", inline=False)
    embed.add_field(name="Tuned by Nishan", value="https://www.tunedbynishan.com/support.html", inline=False)
    embed.add_field(name="Versatuner - Self tune or E-Tune", value="https://www.versatuner.com/", inline=False)
    embed.set_footer(text="If you need more information, or have questions, dont hesitate to ping the Speed Wizard's, or Zenith")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="horsepower_goals", description="What are your horsepower goals? Please view this to see what is needed for your goals", guild=guild)
async def horsepower_goals(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Video of Horsepower goals",
        description="Please view the video linked in the title to watch PD Tuning explain what is all needed for certain Horsepower goals",
        colour= discord.Colour.ash_theme(),
        url="https://www.dropbox.com/scl/fi/8dak78nwex3rj8m31bsqf/1548027956239.mp4?rlkey=zctnuhk8owo2xl2mi4b883lzu&e=1&dl=0"
    )
    embed.add_field(name="275-325", value="HPFP, Intake", inline=False)
    embed.add_field(name="330-370", value='Previous + 3" intake, Optional Turbo upgrade', inline=False)
    embed.add_field(name="375-475", value='Previous + 3.5-4" intake, Catted or Catless DP, FMIC, Turbo upgrade, clutch and flywheel, Intake Manifold, Port Injection, Optional Meth, Optional Forged Rotating assembly', inline=False)
    embed.add_field(name="500+", value="Previous + Catless DP, Forged Rotating assembly", inline=False)
    embed.add_field(name="600+", value="Previous + ...", inline=False)
    embed.add_field(name="700-1,000", value="Get a different Car", inline=False)
    embed.set_footer(text="If you need more information, or have questions, dont hesitate to ping Zenith")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="faq", description="FAQ", guild=guild)
async def faq(interaction : discord.Interaction):
    embed = discord.Embed(
        title="FAQ",
        description="",
        colour= discord.Colour.ash_theme(),
        url=""
    )
    with open('HPFP type.jpg', 'rb') as f:
        hpfp = discord.File(f)
    embed.add_field(name="what oil to run?", value="Oil brand doesn't matter too much some are subjectively better than others you can check out this link for all the specifics, mazdaspeeds.org \nhttps://mazdaspeeds.org/index.php?threads/best-engine-oil-all-mod-levels.7931/ \nMost of the time penz plat 5w30 is the best along with Royal purple 5w-30! Please see link for a complete breakdown!", inline=False)
    embed.add_field(name="How do I know if I have hpfp internals already/what company to buy from.", value="you have to take apart the hpfp and look at the valve itself The tip of the valve has different shapes as shown: \nThe best company to buy hpfp internals is usually whatever is one sale at the time as they are all basically the same thing. Company doesn't matter at all through testing just get them upgraded asap!", inline=False)
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=discord.File('HPFP type.jpg'))

@client.tree.command(name="corn", description="Ethanol Fuel", guild=guild)
async def corn(interaction : discord.Interaction):
    await interaction.response.send_message("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHhjNG9kZjl6dGdsdXcwb2FlOHFjeG0yeGtsbmZhNGlwbDNuOXU2diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yUZvqAk6pjIYNlpEdc/giphy.gif")
@client.event
async def on_member_remove(member):
    channel = client.get_channel(1346017386373054486)
    year_left = time.strftime('%d-%m-%Y')
    time_left = time.strftime('%H:%M')
    if channel:
        await channel.send(f'{year_left}\n{time_left}\n{member.name}') 



client.run(NORMAL_BOT_KEY)