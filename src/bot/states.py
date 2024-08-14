from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State()


class BebrisDialogSG(StatesGroup):
    start = State()
    choice_lesson = State()
    preparation= State()
    next_card = State()
    conclusion = State()
