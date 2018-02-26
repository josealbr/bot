from telepot import Bot, DelegatorBot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import telepot
import json
from telepot.loop import MessageLoop
try:
    from sense_bot import Sense
except ImportError as e:
    print(e)


class MyBot(telepot.Bot):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Temperature', callback_data='temp')],
        [InlineKeyboardButton(text='Humidity', callback_data='hum')],
        [InlineKeyboardButton(text='Photo', callback_data='photo')],

    ])

    def __init__(self, settings_file='settings.json'):
        print('Starting Bot...')
        self.settings = self.get_settings(settings_file)
        super().__init__(self.settings['token'])
        self.user_id = self.settings['id']
        try:
            self.sense = Sense()
            self.message(self.handle_sense)
            MessageLoop(self, {'chat': self.handle,
                               'callback_query': self.on_callback_query}).run_forever()
        except Exception as e:
            print(e)
            print('Not in Raspberry or did not detect sense Hat')
            # MessageLoop(self)
            self.message(self.handle)


    @staticmethod
    def get_settings(file):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print('Create settings file')
        except Exception as e:
            print(e)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            print(msg['text'])
            #self.sendMessage(chat_id, msg['text'])
        self.sendMessage(self.user_id, 'Actions', reply_markup=self.keyboard)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            print(msg['text'])
            # self.sendMessage(chat_id, msg['text'])
        self.sendMessage(self.user_id, 'Actions', reply_markup=self.keyboard)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        if query_data == 'temp':
            self.answerCallbackQuery(query_id, text='Getting Temp')
            self.sendMessage(self.user_id, text=str(self.sense.temperature()))
        elif query_data == 'hum':
            self.answerCallbackQuery(query_id, text='Getting Humidity')
            self.sendMessage(self.user_id, text=self.sense.humidity())
        else:
            self.answerCallbackQuery(query_id, text='Got it')

    def handle_sense(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            print(msg['text'])
            self.sense.show_text(msg['text'])

    def message(self, func):
        MessageLoop(self, func).run_as_thread()

    def url_photo_send(self, url):
        self.sendPhoto(self.user_id, url)


if __name__ == '__main__':
    b = MyBot()
    while True:
        pass
