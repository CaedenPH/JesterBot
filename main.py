from core.Bot import JesterBot
from core.main.check import run_check, run_executed, run_precheck

import discord, asyncio

bot = JesterBot()

@bot.listen('on_message')
async def _message(message):
    output = await run_precheck(bot, message)
    return output

@bot.check
async def _check(ctx):      
    output = await run_check(bot, ctx)
    return output

@bot.after_invoke
async def executed(ctx):
    await run_executed(bot, ctx)

@bot.command()
async def push(ctx, reason):
    embed = discord.Embed(title="Git push.", description="")
    git_commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", reason],
        ["git", "push"],
    ]

    for git_command in git_commands:
        process = await asyncio.create_subprocess_exec(
            git_command[0],
            *git_command[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        output, error = await process.communicate()
        embed.description += f'[{" ".join(git_command)!r} exited with return code {process.returncode}\n'

        if output:
            embed.description += f"[stdout]\n{output.decode()}\n"
        if error:   
            embed.description += f"[stderr]\n{error.decode()}\n"
    await ctx.send(embed=embed)
    
if __name__ == "__main__":
    bot.run()


