import time
from django.core.management.base import BaseCommand
from pirc522 import RFID
from drinkdispenser.models import Card


class Command(BaseCommand):
    help = 'NFC Observer'

    def handle(self, *args, **kwargs):
        reader = RFID()

        while True:
            reader.wait_for_tag()
            (error, tag_type) = reader.request()
            if error:
                continue

            print("Tag detected")
            (error, uid) = reader.anticoll()
            if error:
                continue

            print(f"UID: {uid}")
            card: Card = Card.objects.get(uid=uid)
            card.drink.dispense()
            time.sleep(10)

        reader.cleanup()
