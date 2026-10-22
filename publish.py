import os
import requests

def publish_to_pinterest():
    # Получаем токен и ID приложения из переменных окружения
    access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
    app_id = os.getenv("PINTEREST_APP_ID")

    if not access_token:
        print("Ошибка: Токен доступа не найден.")
        return

    # Пример данных для создания Пина
    url = "https://api.pinterest.com/v1/pins/"
    payload = {
        "access_token": access_token,
        "board": "ваш_id_доски",  # Вам нужно указать ID вашей доски
        "note": "Автоматическая публикация из блога",
        "image_url": "https://example.com/image.jpg",  # Ссылка на изображение
        "link": "https://example.com",  # Ссылка на источник
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Пин успешно опубликован!", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при публикации: {e}")

if __name__ == "__main__":
    publish_to_pinterest()
