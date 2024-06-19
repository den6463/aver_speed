# database.py
import sqlite3
from datetime import datetime, timedelta
import random

# Константы
DATABASE_NAME = 'database.db'

def connect_db():
    """
    Подключение к базе данных SQLite и возврат объекта соединения.
    """
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    """
    Создание таблицы cars в базе данных.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_plate TEXT UNIQUE NOT NULL,
        start_speed REAL NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        end_speed REAL,
        avg_speed REAL  -- Добавлено поле для средней скорости
    )
    ''')
    
    conn.commit()
    conn.close()

def add_car(license_plate, start_speed, start_time):
    """
    Добавление новой записи автомобиля в таблицу cars.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO cars (license_plate, start_speed, start_time)
    VALUES (?, ?, ?)
    ''', (license_plate, start_speed, start_time))
    
    conn.commit()
    conn.close()

def update_car_end(car_id, end_time, end_speed, avg_speed=None):
    """
    Обновление информации о завершении поездки автомобиля в таблице cars.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    if avg_speed is None:
        # Рассчитываем среднюю скорость, если не указана
        start_speed, start_time = get_car_info(car_id)[2:4]
        trip_duration = (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).total_seconds() / 3600
        avg_speed = (start_speed + end_speed) / 2
    
    update_query = """
        UPDATE cars
        SET end_time = ?,
            end_speed = ?,
            avg_speed = ?
        WHERE id = ?
    """
    cursor.execute(update_query, (end_time, float(end_speed), float(avg_speed), car_id))
    conn.commit()
    conn.close()

def get_active_cars():
    """
    Получение списка активных машин (которые еще не прибыли в пункт Б).
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM cars
    WHERE end_time IS NULL
    ''')
    
    active_cars = cursor.fetchall()
    conn.close()
    return active_cars

def get_finished_cars():
    """
    Получение списка завершенных поездок (машин, которые прибыли в пункт Б).
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM cars
    WHERE end_time IS NOT NULL
    ''')
    
    finished_cars = cursor.fetchall()
    conn.close()
    return finished_cars

def get_average_speed():
    """
    Расчет средней скорости всех завершенных машин.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT AVG(end_speed) FROM cars
    WHERE end_speed IS NOT NULL
    ''')
    
    avg_speed = cursor.fetchone()[0]
    conn.close()
    return avg_speed

def calculate_end_time_and_speed(start_time, start_speed):
    """
    Генерация случайного времени прибытия в пункт Б (в пределах 60 минут)
    и расчет средней скорости между пунктами А и Б.
    """
    # Генерация случайного времени поездки (от 1 до 60 минут)
    trip_time_minutes = random.randint(1, 60)
    end_time = start_time + timedelta(minutes=trip_time_minutes)
    
    # Расчет средней скорости
    distance = 100  # фиксированное расстояние между A и B в км
    trip_time_hours = trip_time_minutes / 60  # перевод времени в часы
    avg_speed = distance / trip_time_hours
    
    return end_time, avg_speed, trip_time_minutes

def get_car_info(car_id):
    """
    Получение информации о конкретном автомобиле по его ID.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM cars
    WHERE id = ?
    ''', (car_id,))
    
    car_info = cursor.fetchone()
    conn.close()
    return car_info
