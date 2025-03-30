from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    start = State()


class BebrisDialogSG(StatesGroup):
    start = State()
    choice_lesson = State()
    preparation = State()
    show_all_cards = State()
    next_card = State()
    lesson_exit = State()
    conclusion = State()


class BebrisTrainDialogSG(StatesGroup):
    repeat_lessons_list = State()
    initialize_lesson = State()
    show_cards = State()
    next_card = State()
    exit = State()
    results = State()
