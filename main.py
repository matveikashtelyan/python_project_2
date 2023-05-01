
import asyncio
import src.tgbot.bot
import src.tgbot.variables as V


async def main():
    await V.dispatcher.start_polling(V.bot)

if __name__ == "__main__":
    asyncio.run(main())

