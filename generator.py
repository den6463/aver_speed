# generator.py
import random
import string

def generate_license_plate():
    #Генерирует случайный номер автомобиля в формате '111 AAA 01'.
    numbers = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    region = '{:02d}'.format(random.randint(1, 15))
    return f'{numbers} {letters} {region}'

def generate_random_speed(min_speed=100, max_speed=140):
    #Генерирует случайную скорость
    return random.uniform(min_speed, max_speed)
