import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, Jinja, List
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
from .handlers import LessonHandler
from bot.aiogram_dialog.scrolling_group import ScrollingGroupCustom
from bot.handlers.common_handlers import go_back
from bot.handlers.handlers import main_menu 
from bot.states import BebrisDialogSG, BebrisTrainDialogSG

handle = LessonHandler()

choice_playlist_window = Window(
    Const('Выбри цвет плейлиста'),
    ScrollingGroup(
        Group(
            Select(
                Format('{item[2]} {item[1]}'),
                id='playlist_btns',
                items='playlists',
                item_id_getter=lambda x: x[0],
                on_click=handle.select_lesson
            ),
        ),
        id='playlist_scroll',
        width=1,
        height=5,
        hide_on_single_page=True,
    ),
    Row(
        Button(Const('⏎ Назад'), id='main_menu', on_click=main_menu),
        Button(Const('↻ Повторение'), id='repeat_mode', on_click=handlers.choice_repeat_mode),
    ),
    getter=getters.playlist_getter,
    state=BebrisDialogSG.start
)


choice_lesson_window = Window(
    Jinja(
        '<b>--- Памятка ---</b>\n\n'
        '<blockquote>Прогресс показывает средний процент правильных ответов за последние три урока.</blockquote>\n\n'
        '🔴 - <i>Прогресс меньше 60%</i>\n'
        '🟠 - <i>Прогресс 60-90%</i>\n'
        '🟢 - <i>Прогресс 90-100%</i>\n\n'
        '<b>--- Выбери или введи номер урока ---</b>\n\n'
    ),
    List(
        Format('{item[3]} <b>№{item[0]}</b>  {item[1]} {item[2]}'),
        page_size=8,
        id='lessons_scroll',
        items='lessons'
    ),
    ScrollingGroupCustom(
        Group(
            Select(
                Format('{item[0]}'),
                id='lesson_btns',
                items='lessons',
                item_id_getter=lambda x: x[0],
                on_click=handle.initialize_lesson
            ),
        ),
        id='lessons_scroll',
        width=8,
        height=1,
        hide_on_single_page=True,
    ),
    TextInput(
        id='age_input',
        on_success=handle.initialize_lesson_from_input
    ),
    Row(
        Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
        Button(Const('☰ Mеню'), id='main_menu', on_click=main_menu),
    ),
    parse_mode='HTML',
    getter=getters.lessons_getter,
    state=BebrisDialogSG.choice_lesson
)


preparation_window = Window(
    Jinja(
        '<blockquote>Обратите внимание: при повторном прохождении одного и того же урока карточки будут представлены в разном порядке.</blockquote>\n\n'
        '{% for card in first_cards %}'
        '{{ card[3] }}. {{ card[1] }} - {{ card[2]}}\n'
        '{% endfor %}'
        '•••\n\n'
        '⚙️ <b>Режимы тренировок:</b>\n'
        'RU2EN - <i>с русского на английский</i>\n'
        'EN2RU - <i>с английского на русский</i>\n'
    ),
    Button(Const('Начать'), id='start', on_click=handle.start_flashcard_session),
    Radio(
        checked_text=Format('🔘 {item[0]}'),
        unchecked_text=Format('⚪️ {item[0]}'),
        id='radio_reverse_mode',
        item_id_getter=operator.itemgetter(1),
        items=[('RU to EN', '0'), ('EN to RU', '1')],
    ),
    Row(
        Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
        Button(Const('Показать карточки'), id='get_all_cards', on_click=handle.show_all_cards),
    ),
    parse_mode='HTML',
    getter=getters.preparation_getter,
    state=BebrisDialogSG.preparation
)


show_all_cards_window = Window(
    Format('<b>Все карточки:</b>\n'),
    List(
        Format('{item[3]}. {item[1]} - {item[2]}'),
        id='all_cards_scroll',
        items='all_cards'
    ),
    Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    getter=getters.show_all_cards_getter,
    state=BebrisDialogSG.show_all_cards
)


flashcard_window = Window(
    Jinja(
        '{{ position }}/{{total_cards}} (#{{ current_card_id }})\n\n'
        '{{ front_text }}\n\n'
        '<tg-spoiler>{{ back_text }}</tg-spoiler>\n\n'
        '🔴 {{ total_wrong_answers }} - {{ total_correct_answers }} 🟢 ({{ accuracy_percent }}%)'
    ),
    Row(
        Button(Const('Не помню'), id='wrong', on_click=handle.next_card_or_completion),
        Button(Const('Помню'), id='correct', on_click=handle.next_card_or_completion),
    ),
    Button(Const('Завершить'), id='lesson_exit', on_click=handle.lesson_exit),
    parse_mode='HTML',
    getter=getters.next_card_getter,
    state=BebrisDialogSG.next_card
)


lesson_exit_window = Window(
    Const('Вы уверены, что хотите выйти?\n\n<i>⚠️  Ваши ответы на текущие карточки</i> <b>не будут сохранены.</b>'),
    Button(Const('Да, выйти без сохранения'), id='main_menu', on_click=main_menu),
    Button(Const('⏎ Отмена'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    state=BebrisDialogSG.lesson_exit
)


conclusion_window = Window(
    Format('{data} = {data2}'),
    getter=getters.conclusion_getter,
    state=BebrisDialogSG.conclusion
)


bebris_dialog = Dialog(
    choice_playlist_window,
    choice_lesson_window,
    preparation_window,
    show_all_cards_window,
    flashcard_window,
    lesson_exit_window,
    conclusion_window
)

choice_train_lesson_window = Window(
    Jinja('<b>--- Выбери или введи номер урока ---</b>\n\n'),
    # List(
    #     Format('{item[3]} <b>№{item[0]}</b>  {item[1]} {item[2]}'),
    #     page_size=8,
    #     id='lessons_scroll',
    #     items='lessons'
    # ),
    # ScrollingGroupCustom(
    #     Group(
    #         Select(
    #             Format('{item[0]}'),
    #             id='lesson_btns',
    #             items='lessons',
    #             item_id_getter=lambda x: x[0],
    #             on_click=handlers.prepare_lesson_data
    #         ),
    #     ),
    #     id='lessons_scroll',
    #     width=8,
    #     height=1,
    #     hide_on_single_page=True,
    # ),
    Button(Const('Повторить все'), id='go_back_btn', on_click=go_back),
    parse_mode='HTML',
    getter=getters.repeat_lesson_getter,
    state=BebrisTrainDialogSG.choice_repeat_lesson
)

bebris_train_dialog = Dialog(choice_train_lesson_window)
