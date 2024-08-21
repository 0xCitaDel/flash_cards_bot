import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Jinja, List
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Radio,
    Row,
    ScrollingGroup,
    Select
)

from . import getters
from . import handlers
from bot.aiogram_dialog.scrolling_group import ScrollingGroupCustom
from bot.handlers.common_handlers import go_back
from bot.handlers.handlers import main_menu 
from bot.states import BebrisTrainDialogSG


train_lessons_list_window = Window(
    Jinja('<b>--- Выбери или введи номер урока ---</b>\n\n'),
    List(
        Jinja('{{ item.emoji }} <b>№{{ item.position }}</b> {{ item.lesson_title }} ({{ item.card_count }} шт.)'),
        page_size=8,
        id='lessons_scroll',
        items='lessons'
    ),
    ScrollingGroupCustom(
        Group(
            Select(
                Jinja('{{ item.position }}'),
                id='lesson_btns',
                items='lessons',
                item_id_getter=lambda x: x['position'],
                on_click=handlers.initialize_lesson
            ),
        ),
        id='lessons_scroll',
        width=8,
        height=1,
        hide_on_single_page=True,
    ),
    Button(Const('Повторить все'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    getter=getters.repeat_lesson_getter,
    state=BebrisTrainDialogSG.repeat_lessons_list
)


initialize_train_lesson_window = Window(
    Jinja('some'),
    getter=getters.initialize_lesson_getter,
    state=BebrisTrainDialogSG.initialize_lesson
)


bebris_train_dialog = Dialog(
    train_lessons_list_window,
    initialize_train_lesson_window
)
