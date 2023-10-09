from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard


router = Router()

available_prof_names = ["Разработчик", "Аналитик", "Тестировщик"]
available_prof_grade = ["Junior", "Middle", "Senior"]


class ChoiceProfNames(StatesGroup):
    choosing_prof_names = State()
    choosing_prof_grade = State()


@router.message(Command('prof'))
async def cmd_prof(message: Message, state: FSMContext):
    await message.answer(
        text="Выбери профессию",
        reply_markup=make_row_keyboard(available_prof_names)
    )
    await state.set_state(ChoiceProfNames.choosing_prof_names)


@router.message(ChoiceProfNames.choosing_prof_names, F.text.in_(available_prof_names))
async def prof_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_prof=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь выбери свой уровень:",
        reply_markup=make_row_keyboard(available_prof_grade)
    )
    await state.set_state(ChoiceProfNames.choosing_prof_grade)


@router.message(ChoiceProfNames.choosing_prof_names)
async def prof_chosen_incorrectly(message: Message):
    await message.answer(
        text='Я не знаю такой профессии.\n\n Выберите одну из списка',
        reply_markup=make_row_keyboard(available_prof_names)
    )


@router.message(ChoiceProfNames.choosing_prof_grade, F.text.in_(available_prof_grade))
async def prof_grade_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} уровень {user_data.get('chosen_prof')}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(ChoiceProfNames.choosing_prof_grade)
async def prof_grade_chosen_incorrectly(message: Message):
    await message.answer(
        text='Я не знаю такого уровня.\n\n Выберите одну из списка',
        reply_markup=make_row_keyboard(available_prof_grade)
    )