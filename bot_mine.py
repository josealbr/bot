from telepot import Bot
import telepot
import json
from telepot.loop import MessageLoop


class MyBot(Bot):

    def __init__(self):
        print('Starting Bot...')
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            print('Create settings file')
            exit()
        except Exception as e:
            print(e)
            exit()
        super().__init__(self.settings['token'])
        self.user_id = self.settings['id']

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            print(msg['text'])
            #self.sendMessage(chat_id, msg['text'])

    def message(self):
        MessageLoop(self, self.handle).run_forever()

    def url_photo_send(self, url):
        self.sendPhoto(self.user_id, url)


if __name__ == '__main__':
    b = MyBot()