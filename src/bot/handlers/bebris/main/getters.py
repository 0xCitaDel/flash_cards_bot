from aiogram_dialog import DialogManager, ShowMode

from db.database import Database
from services import BebrisService


async def playlist_getter(db: Database, **kwargs):
    items = await BebrisService(db).get_playlists()
    return {'playlists': items}


async def lessons_getter(dialog_manager: DialogManager, **kwargs):
    return {'lessons': dialog_manager.dialog_data['lessons']}


async def preparation_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    dialog_manager.dialog_data['reverse_mode'] = dialog_manager.find('radio_reverse_mode').get_checked()
    return {'first_cards': dialog_manager.dialog_data['all_cards'][:3] }


async def show_all_cards_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> dict:
    return {'all_cards': dialog_manager.dialog_data['all_cards']}


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
        'current_card_id': current_card[0],
        'position': data['position'],
        'front_text': current_card[1 if mode else 2],
        'back_text': current_card[2 if mode else 1],
        'total_cards': data['total_cards'],
        'total_correct_answers': data['total_correct_answers'],
        'total_wrong_answers': data['total_wrong_answers'],
        'accuracy_percent': data['accuracy_percent']
    }


async def conclusion_getter(
    dialog_manager: DialogManager,
    **kwargs
):
    data = dialog_manager.dialog_data
    return {
        'data': data['correct_answer_ids'],
        'data2': data['wrong_answer_ids']
    }
