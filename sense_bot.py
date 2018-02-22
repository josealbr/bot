import sense_hat


class Sense:
    def __init__(self):
        self.sense = sense_hat.SenseHat()

    def humidity(self):
        return self.sense.get_humidity()

    def temperature(self):
        return self.sense.get_temperature()

    def show_text(self, text):
        assert isinstance(text, str), 'Message not string'
        self.sense.show_message(text)
