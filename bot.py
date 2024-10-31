import asyncio
import logging
import config

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage



#from app.config_reader import load_config
from handlers.earned import register_handlers_earned
from handlers.spent import register_handlers_spent
#from app.handlers.common import register_handlers_common

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/spent", description="Добавить расход"),
        BotCommand(command="/earned", description="Добавить доход"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    #config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    #register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_earned(dp)
    register_handlers_spent(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
