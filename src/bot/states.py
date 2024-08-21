from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State()


class BebrisDialogSG(StatesGroup):
    start = State()
    choice_lesson = State()
    preparation = State()
    show_all_cards = State()
    next_card = State()
    lesson_exit= State()
    conclusion = State()

class BebrisTrainDialogSG(StatesGroup):
    repeat_lessons_list = State()
    initialize_lesson = State()
