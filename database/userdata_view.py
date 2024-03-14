from database import userdata_controller
from telebot.types import Message  # noqa
import json


class ConfigView:
    def __init__(self, message: Message):
        self._message = message
        self._current_user = userdata_controller.get(message)

    def show_currency_in_black_list(self) -> str:
        if len(json.loads(self._current_user.bad_list_currency)) == 0:
            bad_list_exchanges = 'У вас нет криптовалют в черном списке!\n'
        else:
            list_symbols = json.loads(self._current_user.bad_list_currency)
            bad_list_exchanges = (f'Криптовалюты в черном списке (Всего: {len(list_symbols)} из 40):\n'
                                  f'{", ".join(*[list_symbols])}\n\n')
        return bad_list_exchanges
