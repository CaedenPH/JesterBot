import re
import random
import pprint

from disnake.ext import commands
from core import Context
from core.paginator import Paginator


class Crime(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["wanted"])
    async def wanted_criminals(self, ctx: Context) -> None:
        item = random.randint(0, 20)

        async with self.bot.client.get(
            url="https://api.fbi.gov/wanted/v1/list",
            params={"page": random.randint(0, 49)},
        ) as resp:
            json = await resp.json()
            json = json["items"][item]

        data = f"""
{"[reward_text:] " + json['reward_text'] if json['reward_text'] else ''} 
{"[eye_color:] " +  json['eyes'] if json['eyes'] else ''}
{"[nationality:] " + json['nationality'] if json['nationality'] else ''}
{"[age_range:] " + json['age_range'] if json['age_range'] else ''}
{"[caution:] " + json['caution'] if json['caution'] else ''}
{"[url:] " + json['files'][0]['url'] if json['files'][0]['url'] else ''}
{"[possibly_countries:] " + ', '.join(json['possible_countries']) if json['possible_countries'] else ''}
{"[sex:] " + json['sex'] if json['sex'] else ''}
{"[warning_message:] " + json['warning_message'] if json['warning_message'] else ''}
{"[additional_information:] " + json['additional_information'] if json['additional_information'] else ''}
{"[description:] " + json['description'] if json['description'] else ''}
{"[field_offices:] " + ', '.join(json['field_offices']) if json['field_offices'] else ''}
{"[scars_and_marks:] " + json['scars_and_marks'] if json['scars_and_marks'] else ''}
{"[id:] " + json['@id'] if json['@id'] else ''}
{"[occupations:] " + json['occupations'] if json['occupations'] else ''}
{"[hair_colow:] " + json['hair'] if json['hair'] else ''}
"""
        data = re.sub("\n{2,}", "\n", data).strip()
        await ctx.em(
            f"""```yaml
    ++ -- wanted criminal {json['title']} -- ++

{data}

      [real data curated from official FBI sources]```"""
        )

    @commands.command(aliases=["jail"])
    async def jailbase(self, ctx: Context, last_name: str, first_name: str = "") -> None:
        async with self.bot.client.get(
            url=f"https://www.jailbase.com/api/1/search/?source_id=az-mcso&last_name={last_name}&first_name={first_name}"
        ) as resp:
            json = await resp.json()

        choice = random.randint(0, len(json["records"]))
        info = json["records"][choice]
        await ctx.em(
            re.sub(
                "\n{2,}",
                "\n",
                f"""```yaml
    ++ -- Record for {info['name']} -- ++
    
{"[county_state:] " + info['county_state'] if info['county_state'] else ''}
{"[charges:] " + ', '.join(info['charges']) if info['charges'] else ''}
{"[eyes:] " + info['details'][4][1] if info['details'][4][1] else ''}
{"[hair:] " + info['details'][5][1] if info['details'][5][1] else ''}
{"[gender:] " + info['details'][0][1] if info['details'][0][1] else ''}
{"[age at arrest:] " + str(info['details'][1][1]) if info['details'][1][1] else ''}
{"[weight:] " + info['details'][3][1] if info['details'][3][1] else ''} 
{"[height:] " + info['details'][2][1] if info['details'][2][1] else ''}  
{"[ref:] " + info['details'][6][1] if info['details'][6][1] else ''}          
{"[mugshot:] " + info['mugshot'] if info['mugshot'] else ''}
{"[source_id:] " + info['source_id'] if info['source_id'] else ''}         
{"[more_info_url:] " + info['more_info_url'] if info['more_info_url'] else ''}```""",
            )
        )

    @commands.command()
    async def police(self, ctx: Context) -> None:
        async with self.bot.client.get(
            url="https://ukpolicedata.p.rapidapi.com/forces",
            headers={
                "x-rapidapi-host": "ukpolicedata.p.rapidapi.com",
                "x-rapidapi-key": self.bot.RAPID_API_KEY,
            },
        ) as resp:
            json = await resp.json()

        police = ", ".join([json[k]["name"] for k in range(0, len(json))])
        await ctx.em(
            f"""```yaml
        ++ -- All police forces in england -- ++

{police}    

  [Factual information curated from official police data]```"""
        )

    @commands.command()
    async def coordinates(self, ctx: Context, *, poste_code=None) -> None:
        async with self.bot.client.get(
            url=f"http://api.positionstack.com/v1/forward?access_key={self.bot.COORDS_KEY}&query={poste_code}"
        ) as resp:
            json = await resp.json()

        if not json["data"][0]:
            return await ctx.em("Invalid location!")

        await ctx.em(
            f"""```yaml
    ++ -- coordinates for {poste_code} -- ++

[Longitude:] {json['data'][0]['longitude']}
[Latitude:] {json['data'][0]['latitude']}
[Region:] {json['data'][0]['region']}
[Country:] {json['data'][0]['country']}```
            """
        )

    @commands.command(aliases=["searches"])
    async def stop_and_searches(self, ctx: Context, poste_code=None) -> None:
        async with self.bot.client.get(
            url=f"http://api.positionstack.com/v1/forward?access_key={self.bot.COORDS_KEY}&query={poste_code}"
        ) as resp:
            json = await resp.json()

        if not json["data"][0]:
            return await ctx.em("Invalid location!")

        querystring = {
            "lat": json["data"][0]["latitude"],
            "lng": json["data"][0]["longitude"],
        }
        async with self.bot.client.get(
            url="https://ukpolicedata.p.rapidapi.com/stops-street",
            headers={
                "x-rapidapi-host": "ukpolicedata.p.rapidapi.com",
                "x-rapidapi-key": self.bot.RAPID_API_KEY,
            },
            params=querystring,
        ) as resp:
            json = await resp.json()

        if not json:
            return await ctx.em("No crime data for that location!")

        content = f"""```yaml
      ++ -- Stop and search data for {poste_code} -- ++

{pprint.pformat(json)}```"""

        if not len(content) >= 5999:
            return await ctx.em(content)

        pag = Paginator(ctx)
        await pag.paginate(
            content="      " + content[7:-3].strip(),
            name=ctx.author,
            icon_url=ctx.author.avatar.url,
        )

    @commands.command()
    async def crime(self, ctx: Context, poste_code=None) -> None:
        async with self.bot.client.get(
            url=f"http://api.positionstack.com/v1/forward?access_key={self.bot.COORDS_KEY}&query={poste_code}"
        ) as resp:
            json = await resp.json()

        if not json["data"][0]:
            return await ctx.em("Invalid location!")

        querystring = {
            "lat": json["data"][0]["latitude"],
            "lng": json["data"][0]["longitude"],
        }
        async with self.bot.client.get(
            url="https://ukpolicedata.p.rapidapi.com/crimes-street/all-crime",
            headers={
                "x-rapidapi-host": "ukpolicedata.p.rapidapi.com",
                "x-rapidapi-key": self.bot.RAPID_API_KEY,
            },
            params=querystring,
        ) as resp:
            json = await resp.json()

        if not json:
            return await ctx.em("No crime data for that location!")

        content = f"""```yaml
      ++ -- Stop and search data for {poste_code} -- ++

{pprint.pformat(json)}```"""

        if not len(content) >= 5999:
            return await ctx.em(content)

        pag = Paginator(ctx)
        await pag.paginate(
            content="      " + content[7:-3].strip(),
            name=ctx.author,
            icon_url=ctx.author.avatar.url,
        )


def setup(bot: commands.Bot):
    bot.add_cog(Crime(bot))
