from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re

class OrderEarned(StatesGroup):
    waiting_for_earned_name = State()
    waiting_for_earned_sum = State()


# Обратите внимание: есть второй аргумент
async def earned_start(message: types.Message, state: FSMContext):
    await message.bot.send_message(message.chat.id,"Введите статью дохода:")
    await state.set_state(OrderEarned.waiting_for_earned_name.state)

async def earned_chosen(message: types.Message, state: FSMContext):
    await state.update_data(earned=message.text.capitalize())
    await state.set_state(OrderEarned.waiting_for_earned_sum.state)
    await message.bot.send_message(message.chat.id,"Введите сумму:")

async def earned_sum_chosen(message: types.Message, state: FSMContext):

    x = re.findall(r'\d+(?:.\d+)?', message.text.lower())
    print(x)
    if (len(x)):
        value = "{0:.2f}".format(float(x[0].replace(',', '.')))
    else:
       await message.answer("Пожалуйста, правильно введите сумму.")
       return

    await state.update_data(earned_sum=value)
    user_data = await state.get_data()
    print(user_data)
    await message.answer(f"Вы внесли в доходы сумму {value}  по статье {user_data['earned'].capitalize()}.\n")
    await state.finish()
def register_handlers_earned(dp: Dispatcher):
    dp.register_message_handler(earned_start, commands="earned", state="*")
    dp.register_message_handler(earned_chosen, state=OrderEarned.waiting_for_earned_name)
    dp.register_message_handler(earned_sum_chosen, state=OrderEarned.waiting_for_earned_sum)
