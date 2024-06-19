# Импорт необходимых модулей и функций
from flask import Flask, render_template, jsonify, request, logging
from datetime import datetime, timedelta
from generator import generate_license_plate, generate_random_speed
import database as db

app = Flask(__name__)

# Создание таблиц при запуске приложения
db.create_tables()

@app.route('/')
def index():
    cars = db.get_active_cars()  # Получение списка активных автомобилей
    finished_cars = db.get_finished_cars()  # Получение списка завершенных поездок
    return render_template('index.html', cars=cars, finished_cars=finished_cars)

@app.route('/start', methods=['POST'])
def start():
    active_cars = db.get_active_cars()
    if len(active_cars) < 10:
        license_plate = generate_license_plate()  # Генерация номера автомобиля
        start_speed = generate_random_speed()  # Генерация начальной скорости
        start_time = datetime.now()  # Получение текущего времени
        
        # Расчет времени прибытия в пункт B, средней скорости и времени поездки
        end_time, avg_speed, trip_time_minutes = db.calculate_end_time_and_speed(start_time, start_speed)
        
        # Добавление записи о новом автомобиле в базу данных
        db.add_car(license_plate, start_speed, start_time.isoformat())
        
        # Обновление информации о времени и средней скорости
        car_id = db.get_active_cars()[-1][0]  # Получение ID только что добавленного автомобиля
        db.update_car_end(car_id, end_time.isoformat(), avg_speed)
        
        return jsonify({
            "message": "Car started",
            "car": license_plate,
            "trip_time_seconds": trip_time_minutes
        }), 200
    return jsonify({"message": "Maximum number of cars reached"}), 400

@app.route('/end/<string:car_id>', methods=['POST'])
def end_car(car_id):
    try:
        print(f"Attempting to finish car with ID: {car_id}")
        if request.json:
            end_speed = float(request.json.get('end_speed', 0.0))
            end_time = datetime.now()

            # Логика обновления данных в базе данных
            db.update_car_end(car_id, end_time.isoformat(), end_speed)

            print(f"Successfully finished car with ID: {car_id}")
            return jsonify({"message": f"Car with ID {car_id} finished", "end_speed": end_speed}), 200
        else:
            print("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400
    except Exception as e:
        print(f"Error finishing car {car_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400



@app.route('/generate-end-speed')
def generate_end_speed():
    """
    Генерация случайной конечной скорости в заданном диапазоне.
    """
    min_speed = 100
    max_speed = 140
    end_speed = generate_random_speed(min_speed, max_speed)
    
    # Дополнительная проверка, чтобы убедиться, что end_speed находится в заданном диапазоне
    end_speed = max(min(end_speed, max_speed), min_speed)
    
    print(f"Generated End Speed: {end_speed} km/h")
    return jsonify({"end_speed": end_speed}), 200

@app.route('/average-speed')
def average_speed():
    """
    Расчет средней скорости всех завершенных поездок.
    """
    avg_speed = db.get_average_speed()
    return jsonify({"average_speed": avg_speed or 0})

@app.route('/about')
def about():
    """
    Отображение страницы "О проекте".
    """
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
