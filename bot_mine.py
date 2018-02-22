from telepot import Bot
import telepot
import json
from telepot.loop import MessageLoop
try:
    from sense_bot import Sense
except ImportError as e:
    print(e)


class MyBot(Bot):

    def __init__(self, settings_file='settings.json'):
        print('Starting Bot...')
        self.settings = self.get_settings(settings_file)
        super().__init__(self.settings['token'])
        self.user_id = self.settings['id']
        try:
            self.sense = Sense()
            self.message(self.handle_sense)
        except Exception as e:
            print(e)
            print('Not in Raspberry')
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
            self.sendMessage(chat_id, msg['text'])

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
