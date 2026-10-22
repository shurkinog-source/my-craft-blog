import os
import requests

def get_first_board_id(headers, base_url):
    """Находит существующую доску или автоматически создаёт тестовую."""
    url = f"{base_url}/v5/boards"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    boards = response.json().get("items", [])
    if not boards:
        print("В Sandbox нет досок, создаём новую...")
        create_resp = requests.post(
            url, headers=headers, json={"name": "Test Board"}
        )
        create_resp.raise_for_status()
        board = create_resp.json()
        print(f"Создана доска: {board.get('name')} (ID: {board.get('id')})")
        return board.get("id")
    print(
        f"Используем доску: '{boards[0].get('name')}' (ID: {boards[0].get('id')})"
    )
    return boards[0].get("id")

def publish_to_pinterest():
    access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
    if not access_token:
        print("Ошибка: Секрет PINTEREST_ACCESS_TOKEN не передан.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    base_url = "https://api-sandbox.pinterest.com"

    try:
        board_id = get_first_board_id(headers, base_url)

        url = f"{base_url}/v5/pins"
        payload = {
            "board_id": board_id,
            "title": "Тестовый пин",
            "description": "Автоматическая публикация через GitHub Actions",
            "link": "https://github.com",
            "media_source": {
                "source_type": "image_url",
                "url": "https://picsum.photos/800/1200",
            },
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("Пин успешно опубликован в Sandbox!")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        if hasattr(e, "response") and e.response is not None:
            print("Ответ сервера:", e.response.text)

if __name__ == "__main__":
    publish_to_pinterest()
