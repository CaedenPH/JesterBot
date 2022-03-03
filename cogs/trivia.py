import disnake
import random
import re
import asyncio
import datetime

from disnake.ext import commands
from core import Context
from core import JesterBot


class Trivia(commands.Cog):
    def __init__(self, bot: JesterBot):
        self.bot = bot
        self.token = "..."

    async def replace_token(self) -> None:
        async with self.bot.client.get(url="https://opentdb.com/api_token.php?command=request") as resp:
            json = await resp.json()
            self.token = json["token"]

    async def get_question(self):
        async with self.bot.client.get(url=f"https://opentdb.com/api.php?amount=1&token={self.token}") as resp:
            json = await resp.json()
        if json["response_code"] == 3:
            await self.replace_token()
            return await self.get_question()
        output = json["results"][0]

        choices = [re.sub("&.*?;", "", k) for k in output["incorrect_answers"]]
        choices.append(re.sub("&.*?;", "", output["correct_answer"]))

        random.shuffle(choices)
        choices = [f"{chr(i)}) {e}" for i, e in enumerate(choices, start=97)]
        for (i, v) in enumerate(choices):
            if v.endswith(re.sub("&.*?;", "", output["correct_answer"])):
                answer = v[0]

        spaces = "".join([" " for i in range(0, 36 - len(", ".join(choices)))])
        return (
            f"""```yaml
    ++ -- {re.sub('&.*?;', '', output['question'])} -- ++

                Your choices are:
{spaces if spaces else ''}{', '.join(choices)}

[category]: {output['category']}
[difficulty]: {output['difficulty']}

        [send the letter corresponding to the answer]```""",
            answer,
        )

    @commands.command(aliases=["question"])
    async def trivia_question(self, ctx: Context) -> None:
        (content, answer) = await self.get_question()
        await ctx.em(content)

        msg = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author)

        if msg.content.lower() == answer:
            return await ctx.em("Thats the correct answer!")
        await ctx.em(f"Incorrect answer - the right answer was `{answer}`")

    @commands.command(aliases=["start", "trivia_start"])
    async def trivia_play(self, ctx: Context) -> None:
        await ctx.em(
            """```yaml
    ++ -- Starting the trivia game! -- ++ 

[Stop the game:] Type 'end' to end the game. 
[How to play:] The bot sends the question, waits 30 seconds for responses. When the bot sends the message you respond with the letter corresponding with the answer.
[Change your answer:] 
    - If you want to change your answer you have to type; 'change <letter>' and replace <letter> with the new letter you want. 
    - Eg you send 'a' as the answer, but you want to change it to be 'b' so you send 'change b'```  """
        )

        input_dict = {}
        run = False
        num = 0

        while True:
            (content, answer) = await self.get_question()
            bot_msg = await ctx.em(content)

            try:
                time = datetime.datetime.utcnow()
                msg = await self.bot.wait_for(
                    "message", check=lambda m: m.channel == ctx.channel and not m.author.bot, timeout=30
                )

                while True:
                    if msg.author == ctx.author and msg.content.lower() == "end":
                        return await ctx.em("Game ending...")

                    if msg.author.name in input_dict:
                        if not input_dict[msg.author.name]["answer"]:
                            input_dict[msg.author.name]["answer"] = msg.content.lower()
                        if msg.content.lower().startswith("change"):
                            input_dict[msg.author.name]["answer"] = msg.content[7].lower()

                    else:
                        input_dict[msg.author.name] = {"score": 0, "answer": msg.content.lower()}

                    run = True
                    msg = await self.bot.wait_for(
                        "message",
                        check=lambda m: m.channel == ctx.channel and not m.author.bot,
                        timeout=30 + (time - datetime.datetime.utcnow()).total_seconds(),
                    )

            except asyncio.TimeoutError:
                if not run:
                    num += 1
                    await bot_msg.delete()

                    if num == 2:
                        break

                    await ctx.em(
                        "```yaml\nNo one responded in time! If no one responds on the next round the game ends```",
                        delete_after=60,
                    )

                else:
                    correct = [k for k in input_dict if input_dict[k]["answer"] == answer]
                    sorted_dict = dict(sorted(input_dict.items(), key=lambda k: k[1]["score"], reverse=True))
                    for k in correct:
                        input_dict[k]["score"] += 1
                    leaderboard = "\n".join([f"      - {k}: {[input_dict[k]['score']]}" for k in sorted_dict])

                    await ctx.em(
                        f"""```yaml
    ++ -- The answer was {answer.upper()} -- ++ 

{"[Correct:] " + ', '.join(correct) if correct else "No one got it right!"}
[Leaderboard:] 
{leaderboard if leaderboard else "No one answered"}```""",
                        delete_after=30,
                    )

                    for k in input_dict:
                        input_dict[k]["answer"] = ""
                    run = False
                    num = 0

        await ctx.em("```yaml\nThanks for playing!```")


def setup(bot: JesterBot) -> None:
    bot.add_cog(Trivia(bot))
