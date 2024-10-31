from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
class OrderSpent(StatesGroup):
    waiting_for_spent_name = State()
    waiting_for_spent_sum = State()


# Обратите внимание: есть второй аргумент
async def spent_start(message: types.Message, state: FSMContext):
    await message.bot.send_message(message.chat.id,"Введите статью расходов:")
    await state.set_state(OrderSpent.waiting_for_spent_name.state)

async def spent_chosen(message: types.Message, state: FSMContext):
    await state.update_data(spent=message.text.capitalize())
    await state.set_state(OrderSpent.waiting_for_spent_sum.state)
    await message.bot.send_message(message.chat.id,"Введите сумму:")

async def spent_sum_chosen(message: types.Message, state: FSMContext):

    x = re.findall(r'\d+(?:.\d+)?', message.text.lower())
    print(x)
    if (len(x)):
        value = "{0:.2f}".format(float(x[0].replace(',', '.')))
    else:
       await message.answer("Пожалуйста, правильно введите сумму.")
       return

    await state.update_data(spent_sum=value)
    user_data = await state.get_data()
    print(user_data)
    await message.answer(f"Вы внесли в расходы сумму {value}  по статье {user_data['spent'].capitalize()}.\n")
    await state.finish()
def register_handlers_spent(dp: Dispatcher):
    dp.register_message_handler(spent_start, commands="spent", state="*")
    dp.register_message_handler(spent_chosen, state=OrderSpent.waiting_for_spent_name)
    dp.register_message_handler(spent_sum_chosen, state=OrderSpent.waiting_for_spent_sum)
