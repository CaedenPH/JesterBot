import discord
import json

async def thebed(ctx, title, description='', footer='', author=''):
    theembed = discord.Embed(title=title, description=description, color=xz)
    if footer:
        theembed.set_footer(text=footer)
        if author:
            if author[0:2] == 'AV':
                    tauthor = ' '.split(author)
                    theembed.set_author(icon_url=tauthor[1], name=tauthor[2])

    return theembed
#JSON
def Json(file, data):
    file.truncate(0)
    file.seek(0)
    file.write(json.dumps(data, indent=4))

#EMBED COLOR(HEX)
class Color:
    def __init__(self):
        thecolor= open('./Color.json')
        data = json.load(thecolor)

        self.actualcolor = data['Color']['color']

def color():
    xz = int(Color().actualcolor, 16)
    return xz

class GetUser:
    def __init__(self, file, user="", family=""):
        thefile = open(f'./{file}', 'r+')
        thedata = json.load(thefile)
        if user in thedata:
            theuser = user
            thefamily = thedata[str(user)][family]
        else:
            theuser = False
            thefamily = False
        

        self.file = thefile
        self.data = thedata
        self.theuser = theuser
        self.family = thefamily
        self.append = Json(thefile, thedata)
    def user(self, user=""):
        
        if user in self.data:
            theuser = self.data[str(user)]
           
        else:
            theuser = user
            
        self.user = theuser

