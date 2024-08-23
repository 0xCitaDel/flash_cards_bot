from aiogram_dialog import DialogManager, ShowMode

from db.database import Database
from services import BebrisService

async def repeat_lesson_getter(dialog_manager: DialogManager, **kwargs):
    lessons = dialog_manager.start_data['lessons']
    return {'lessons': lessons}

async def initialize_lesson_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data['reverse_mode'] = dialog_manager.find('radio_reverse_mode').get_checked()
    flash_cards = dialog_manager.dialog_data['flash_cards']
    return {'flash_cards': flash_cards}

async def next_card_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    """
     Retrieves the next card's data and prepares it for display.       

    :return: A dictionary with the current card's data and statistics.
    """
    # Set the show mode to delete the previous message and send a new one
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    # Retrieve the dialog data
    data = dialog_manager.dialog_data

    # Get the reverse mode and current card index
    mode = int(data['reverse_mode'])
    current_card_index = data['current_card_index']

    # Get the current card's data
    current_card = data['all_cards'][current_card_index]

    return {
        'current_card_id': current_card['flashcard_id'],
        'position': data['position'],
        'front_text': current_card['front_side' if mode else 'back_side'],
        'back_text': current_card['back_side' if mode else 'front_side'],
        'total_cards': data['total_cards'],
        'total_correct_answers': data['total_correct_answers'],
        'total_wrong_answers': data['total_wrong_answers'],
        'accuracy_percent': data['accuracy_percent']
    }


async def train_results_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'data': dialog_manager.dialog_data['correct_answer_ids'],
        'data2': dialog_manager.dialog_data['wrong_answer_ids'],
    }
