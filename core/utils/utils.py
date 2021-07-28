import discord
import json


#JSON
def Json(file1, data1):
    file1.truncate(0)
    file1.seek(0)
    file1.write(json.dumps(data1, indent=4))    

#EMBED COLOR(HEX)
class Color:
    def __init__(self):
        thecolor= open('./dicts/Color.json')
        data = json.load(thecolor)

        self.actualcolor = data['Color']['color']

def thecolor():
    xz = int(Color().actualcolor, 16)
    return xz

class Cmds:
    def __init__(self, grab):
        x = False
        File = open('./dicts/Cmds.json')
        F_data = json.load(File)
        for key in F_data:
            if grab == key:
                x = True
        if x:
            
            
            self.chelp = F_data[grab]['help'].capitalize()
        else:
            self.chelp = "No help"
            

async def thebed(ctx, title, description='', **kwargs):
    theembed = discord.Embed(title=title, description=description, color=thecolor())
    author = kwargs.get('a')
    icon_url = kwargs.get('i_u')
    footer = kwargs.get('f')
    thumbnail = kwargs.get('t')
    image = kwargs.get('i')
    if footer:
        theembed.set_footer(text=footer)
    if author:
        theembed.set_author(name=author)
        if icon_url:
            theembed.set_author(name=author, icon_url=icon_url)
    if thumbnail:
        theembed.set_thumbnail(url=thumbnail)
    if image:
        theembed.set_image(url=image)
    await ctx.send(embed=theembed)

