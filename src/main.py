import sys
sys.dont_write_bytecode = True

import asyncio

from aiogram import Bot
from loguru import logger

from bot.dispatcher import get_dispatcher
from bot.structures.data_structure import TransferDataWithEngine
from config import settings
from db.database import create_async_engine


async def app():

    bot = Bot(token=settings.bot.BOT_TOKEN)
    dp = get_dispatcher() 
    
    await dp.start_polling(
        bot,
        **TransferDataWithEngine(
            engine=create_async_engine(url=settings.db.create_connection_url())
        )
    )


def main():

    try:
        logger.warning('Bot was starting')
        asyncio.run(app())

    except (KeyboardInterrupt, SystemExit):
        # logger.warning('Bot was stopping')
        print('here error')


if __name__ == '__main__':
    main()
