import json
import os
import requests

def get_first_board_id(headers):
    """Автоматически получает ID первой доски аккаунта."""
    url = "https://api.pinterest.com/v5/boards"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    boards = response.json().get("items", [])
    if not boards:
        raise Exception(
            "На аккаунте Pinterest не найдено ни одной доски. Создайте хотя бы одну доску."
        )
    print(f"Используем доску: '{boards[0]['name']}' (ID: {boards[0]['id']})")
    return boards[0]["id"]

def publish_to_pinterest():
    access_token = os.getenv("PINTEREST_ACCESS_TOKEN")

    if not access_token:
        print("Ошибка: Секрет PINTEREST_ACCESS_TOKEN не передан.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        # Получаем ID доски
        board_id = get_first_board_id(headers)

        # Публикация тестового пина через API v5
        url = "https://api.pinterest.com/v5/pins"
        payload = {
            "board_id": board_id,
            "title": "Тестовый пин",
            "description": "Автоматическая публикация через GitHub Actions",
            "link": "https://github.com",
            "media_source": {
                "source_type": "image_url",
                "url": "https://picsum.photos/800/1200",  # Тестовое изображение высокого разрешения
            },
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Пин успешно опубликован!")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API Pinterest: {e}")
        if hasattr(e, "response") and e.response is not None:
            print("Ответ сервера:", e.response.text)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    publish_to_pinterest()
