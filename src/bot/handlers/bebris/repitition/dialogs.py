import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja, List
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Radio,
    Row,
    Select
)

from . import getters
from .handlers import RepititionBebrisHandler
from bot.handlers.handlers import bebris_dialog_start
from bot.aiogram_dialog.scrolling_group import ScrollingGroupCustom
from bot.handlers.common_handlers import go_back
from bot.handlers.handlers import main_menu 
from bot.states import BebrisTrainDialogSG

handler = RepititionBebrisHandler()

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
                on_click=handler.initialize_lesson
            ),
        ),
        id='lessons_scroll',
        width=8,
        height=1,
        hide_on_single_page=True,
    ),
    Button(Const('Повторить все'), id='all_lessons_btn', on_click=handler.initialize_all_lessons),
    Row(
        Button(Const('⏎ Назад'), id='go_back_btn', on_click=bebris_dialog_start),
        Button(Const('☰ Mеню'), id='main_menu', on_click=main_menu),
    ),
    parse_mode='HTML',
    getter=getters.repeat_lesson_getter,
    state=BebrisTrainDialogSG.repeat_lessons_list
)


initialize_train_lesson_window = Window(
    Jinja('some'),
    Button(Const('Начать'), id='start', on_click=handler.start_repitition_session),
    Radio(
        checked_text=Format('🔘 {item[0]}'),
        unchecked_text=Format('⚪️ {item[0]}'),
        id='radio_reverse_mode',
        item_id_getter=operator.itemgetter(1),
        items=[('RU to EN', '0'), ('EN to RU', '1')],
    ),
    Button(Const('Показать карточки'), id='get_all_cards', on_click=handler.show_all_cards),
    Row(
        Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
        Button(Const('☰ Mеню'), id='main_menu', on_click=main_menu),
    ),
    getter=getters.initialize_lesson_getter,
    state=BebrisTrainDialogSG.initialize_lesson
)


show_cards_window = Window(
    Format('<b>Все карточки:</b>\n'),
    List(
        Jinja('{{ item.position }}. {{ item.front_side }} - {{ item.back_side }}'),
        id='all_cards_scroll',
        items='all_cards'
    ),
    Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    getter=getters.show_all_cards_getter,
    state=BebrisTrainDialogSG.show_cards
)


train_lesson_window = Window(
    Jinja(
        '{{ position }}/{{total_cards}} (#{{ current_card_id }})\n\n'
        '{{ front_text }}\n\n'
        '<tg-spoiler>{{ back_text }}</tg-spoiler>\n\n'
        '🔴 {{ total_wrong_answers }} - {{ total_correct_answers }} 🟢 ({{ accuracy_percent }}%)'
    ),
    Row(
        Button(Const('Не помню'), id='wrong', on_click=handler.next_card_or_completion),
        Button(Const('Помню'), id='correct', on_click=handler.next_card_or_completion),
    ),
    Button(Const('Завершить'), id='lesson_exit', on_click=handler.lesson_exit),
    parse_mode='HTML',
    getter=getters.next_card_getter,
    state=BebrisTrainDialogSG.next_card
)

lesson_exit_window = Window(
    Const('Вы уверены, что хотите выйти?'),
    Button(Const('Да, выйти и сохранить'), id='main_menu', on_click=main_menu),
    Button(Const('⏎ Отмена'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    state=BebrisTrainDialogSG.exit
)

train_results_window = Window(
    Jinja('{{ data }} : {{ data2 }}'),
    parse_mode='HTML',
    getter=getters.train_results_getter,
    state=BebrisTrainDialogSG.results
)


bebris_train_dialog = Dialog(
    train_lessons_list_window,
    initialize_train_lesson_window,
    show_cards_window,
    train_lesson_window, 
    lesson_exit_window,
    train_results_window 
)
