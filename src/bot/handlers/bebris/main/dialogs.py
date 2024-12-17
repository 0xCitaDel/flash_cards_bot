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

from bot.handlers.bebris.repitition.handlers import RepititionBebrisHandler

from . import getters
from .handlers import MainBebrisHandler
from bot.aiogram_dialog.scrolling_group import ScrollingGroupCustom
from bot.handlers.common_handlers import go_back
from bot.handlers.handlers import main_menu 
from bot.states import BebrisDialogSG

handler = MainBebrisHandler()

choice_playlist_window = Window(
    Const('Выбри цвет плейлиста'),
    ScrollingGroup(
        Group(
            Select(
                Jinja('{{ item.emoji }}  {{ item.playlist_name }}'),
                id='playlist_btns',
                items='playlists',
                item_id_getter=lambda x: x['id'],
                on_click=handler.select_lesson
            ),
        ),
        id='playlist_scroll',
        width=1,
        height=8,
        hide_on_single_page=True,
    ),
    Button(
        Const('💭 Карточки для повторения'),
        id='repeat_mode',
        on_click=RepititionBebrisHandler().select_repeat_lessons
    ),
    Row(
        Button(Const('⏎ Назад'), id='main_menu', on_click=main_menu),
        Button(Const('Помощь'), id='main_menu', on_click=main_menu),
    ),
    getter=getters.playlist_getter,
    state=BebrisDialogSG.start
)


choice_lesson_window = Window(
    Jinja(
        '<b>--- Памятка ---</b>\n\n'
        '<blockquote>Прогресс показывает средний процент правильных ответов за последние три урока.</blockquote>\n\n'
        '🔴 - <i>Прогресс меньше 50%</i>\n'
        '🟠 - <i>Прогресс 50-70%</i>\n'
        '🟡 - <i>Прогресс 70-90%</i>\n'
        '🟢 - <i>Прогресс 90-100%</i>\n\n'
        '<b>--- Выбери или введи номер урока ---</b>\n\n'
    ),
    List(
        Jinja(
            '{{ item.accuracy_emoji }} <b>№{{ item.pos }}</b> '
            '{{ item.lesson_title }} ({{ item.lesson_number }} lesson) {{ item.accuracy }}'
        ),
        page_size=21,
        id='lessons_scroll',
        items='lessons'
    ),
    ScrollingGroupCustom(
        Group(
            Select(
                Jinja('{{ item.pos }}'),
                id='lesson_btns',
                items='lessons',
                item_id_getter=lambda x: x['id'],
                on_click=handler.initialize_lesson
            ),
        ),
        id='lessons_scroll',
        width=7,
        height=3,
        hide_on_single_page=True,
    ),
    TextInput(
        id='age_input',
        on_success=handler.initialize_lesson_from_input
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
    Button(Const('Начать'), id='start', on_click=handler.start_flashcard_session),
    Radio(
        checked_text=Format('🔘 {item[0]}'),
        unchecked_text=Format('⚪️ {item[0]}'),
        id='radio_reverse_mode',
        item_id_getter=operator.itemgetter(1),
        items=[('RU to EN', '0'), ('EN to RU', '1')],
    ),
    Row(
        Button(Const('⏎ Назад'), id='go_back_btn', on_click=go_back),
        Button(Const('Показать карточки'), id='get_all_cards', on_click=handler.show_all_cards),
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
        Button(Const('Не помню'), id='wrong', on_click=handler.next_card_or_completion),
        Button(Const('Помню'), id='correct', on_click=handler.next_card_or_completion),
    ),
    Button(Const('Завершить'), id='lesson_exit', on_click=handler.lesson_exit),
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
    Jinja(
        '🏆 Вы завершили тренировку!\n\n'
        'Ваша статистика:\n'
        '- 🍏 Верных ответов: {{ total_correct_answers }}\n'
        '- ✖️ Ошибок: {{ total_wrong_answers }}\n'
        '- 🎯 Точность: {{ accuracy_percent }}%\n\n'
        'Продолжайте в том же духе!'
    ),
    Button(Const('☰ Mеню'), id='main_menu', on_click=main_menu),
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
