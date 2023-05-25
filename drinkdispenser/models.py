import time
from django.db import models
try:
    import RPi.GPIO as GPIO

except ImportError:
    GPIO = None


class Drink(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def dispense(self):
        for ingredient in self.ingredients.all():
            ingredient.dispense(amount=ingredient.amount)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    gpio_port = models.IntegerField()
    dispense_seconds_per_unit = models.FloatField(help_text='Seconds per ml')

    def __str__(self):
        return self.name

    def dispense(self, amount: int):
        GPIO.setup(self.gpio_port, GPIO.OUT)
        GPIO.output(self.gpio_port, GPIO.HIGH)
        time.sleep(amount * self.dispense_seconds_per_unit)
        GPIO.output(self.gpio_port, GPIO.LOW)


class DrinkIngredient(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='drinks')
    amount = models.IntegerField(help_text='Amount in ml')


class Card(models.Model):
    uid = models.CharField(max_length=200, primary_key=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.uid
