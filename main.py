from core.Bot import JesterBot
from core.main.check import run_check, run_executed, run_precheck

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


    

if __name__ == "__main__":
    bot.run()


