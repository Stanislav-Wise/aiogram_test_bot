from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard


router = Router()


@router.message(Command(commands=['start', 'старт']))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выбери, что хочешь сделать: \n\n"
             "Выбрать работу /prof или пройти тестирование /tests",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=['stop', 'стоп']))
@router.message(F.text.lower() == "отмена")
async def cmd_prof(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено ",
        reply_markup=ReplyKeyboardRemove()
    )

