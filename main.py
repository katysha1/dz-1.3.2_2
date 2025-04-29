import requests
import csv
from statistics import mean

def get_weather_data(cities, api_key):

    url = "http://api.openweathermap.org/data/2.5/weather"
    weather_data = []

    for city in cities:
        try:
            # Формируем параметры запроса
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric',  # Температура в градусах Цельсия
                'lang': 'ru'  # Описание погоды на русском языке
            }

            # Выполняем запрос с таймаутом 5 секунд
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()  # Проверка на HTTP ошибки

            data = response.json()

            # Парсим нужные данные
            weather_entry = {
                'city': city,
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description']
            }

            weather_data.append(weather_entry)

        except requests.exceptions.HTTPError as err:
            print(f"Ошибка для города {city}: {err}")
        except requests.exceptions.RequestException as err:
            print(f"Ошибка соединения для города {city}: {err}")
        except KeyError as err:
            print(f"Ошибка парсинга данных для города {city}: {err}")

    return weather_data


def analyze_weather(data):
    if not data:
        return None

    temps = [entry['temp'] for entry in data]

    return {
        'average_temp': round(mean(temps), 1),
        'max_temp': max(temps, key=lambda x: x),
        'min_temp': min(temps, key=lambda x: x)
    }


def save_to_csv(data, filename='weather_data.csv'):

    if not data:
        print("Нет данных для сохранения")
        return

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['city', 'temp', 'humidity', 'wind_speed', 'description'])
            for row in data:
                writer.writerow([
                    row['city'],
                    row['temp'],
                    row['humidity'],
                    row['wind_speed'],
                    row['description']
                ])
        print(f"Данные сохранены в {filename} (чистый CSV)")
    except IOError as e:
        print(f"Ошибка записи: {e}")

# Пример использования
if __name__ == "__main__":
    API_KEY = 'your key'
    CITIES = ['Москва', 'Лондон', 'Нью-Йорк', 'Токио', 'Париж']

    weather_data = get_weather_data(CITIES, API_KEY)

    if weather_data:

        print("\nТекущая погода в городах:")
        print("=" * 40)
        for entry in weather_data:
            print(f"Город: {entry['city']}")
            print(f"Температура: {entry['temp']}°C")
            print(f"Влажность: {entry['humidity']}%")
            print(f"Скорость ветра: {entry['wind_speed']} м/с")
            print(f"Описание: {entry['description'].capitalize()}")
            print("-" * 40)


        stats = analyze_weather(weather_data)

        # Выводим результаты

        print("\nРезультаты:")
        print(f"Средняя температура: {stats['average_temp']}°C")
        print(f"Максимальная температура: {stats['max_temp']}°C в городе "
              f"{max(weather_data, key=lambda x: x['temp'])['city']}")
        print(f"Минимальная температура: {stats['min_temp']}°C в городе "
              f"{min(weather_data, key=lambda x: x['temp'])['city']}")

        # Сохраняем в CSV
        save_to_csv(weather_data)
    else:
        print("Не удалось получить данные о погоде")
