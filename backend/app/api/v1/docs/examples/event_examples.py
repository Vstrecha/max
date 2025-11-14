"""
Event API Examples
Example request and response data for event endpoints.
"""

from datetime import datetime, timedelta
from uuid import uuid4

# Example event data
event_example = {
    "title": "Мероприятие в парке",
    "body": "Приглашаю всех на прогулку в парке Горького! Будем гулять, общаться и веселиться.",
    "photo": "file_uuid_here",
    "tags": ["Природа", "Спорт"],
    "place": "Парк Горького, Москва",
    "start_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
    "end_date": (datetime.now() + timedelta(days=7, hours=3)).date().isoformat(),
    "price": 0,
    "visability": "G",
    "repeatability": "N",
    "status": "A",
    "telegram_chat_link": "https://t.me/meetup_chat",
}

# Example event update data
event_update_example = {
    "title": "Обновленное мероприятие в парке",
    "body": "Обновленное описание встречи в парке Горького!",
    "tags": ["Природа", "Спорт", "Музыка"],
    "place": "Парк Горького, Москва",
    "price": 100,
}

# Example event response
event_response_example = {
    "id": str(uuid4()),
    "title": "Мероприятие в парке",
    "body": "Приглашаю всех на прогулку в парке Горького! Будем гулять, общаться и веселиться.",
    "photo": "file_uuid_here",
    "photo_url": "https://example.com/photo.jpg",
    "tags": ["Природа", "Спорт"],
    "place": "Парк Горького, Москва",
    "start_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
    "end_date": (datetime.now() + timedelta(days=7, hours=3)).date().isoformat(),
    "price": 0,
    "participants": 1,
    "creator": "user_uuid_here",
    "visability": "G",
    "repeatability": "N",
    "status": "A",
    "telegram_chat_link": "https://t.me/meetup_chat",
    "created_at": datetime.now().isoformat(),
    "updated_at": None,
}

# Example participation data
participation_example = {"participation_type": "P"}  # P: PARTICIPANT

# Example event response with participation
event_with_participation_example = {
    "event": {
        "id": str(uuid4()),
        "title": "Мероприятие в парке",
        "body": "Приглашаю всех на прогулку в парке Горького! Будем гулять, общаться и веселиться.",
        "photo": "file_uuid_here",
        "photo_url": "https://example.com/photo.jpg",
        "tags": ["Природа", "Спорт"],
        "place": "Парк Горького, Москва",
        "start_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7, hours=3)).date().isoformat(),
        "price": 0,
        "creator": "user_uuid_here",
        "visability": "G",
        "repeatability": "N",
        "status": "A",
        "telegram_chat_link": "https://t.me/meetup_chat",
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    },
    "friends_going": 3,
    "friends_of_friends_going": 7,
    "participation_type": "P",
}

# Example event list response
event_list_response_example = {
    "events": [
        {
            "event": {
                "id": str(uuid4()),
                "title": "Мероприятие в парке",
                "body": "Приглашаю всех на прогулку в парке Горького!",
                "photo": "file_uuid_here",
                "photo_url": "https://example.com/photo.jpg",
                "tags": ["Природа", "Спорт"],
                "place": "Парк Горького, Москва",
                "start_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=7, hours=3)).date().isoformat(),
                "price": 0,
                "participants": 1,
                "creator": "user_uuid_here",
                "visability": "G",
                "repeatability": "N",
                "status": "A",
                "telegram_chat_link": "https://t.me/meetup_chat",
                "created_at": datetime.now().isoformat(),
                "updated_at": None,
            },
            "friends_going": 3,
            "friends_of_friends_going": 7,
            "participation_type": "P",
        },
        {
            "event": {
                "id": str(uuid4()),
                "title": "Лекция по истории",
                "body": "Интересная лекция по истории Москвы",
                "photo": None,
                "photo_url": None,
                "tags": ["Лекция", "Музей"],
                "place": "Исторический музей",
                "start_date": (datetime.now() + timedelta(days=14)).date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=14, hours=2)).date().isoformat(),
                "price": 500,
                "participants": 0,
                "creator": "user_uuid_here",
                "visability": "G",
                "repeatability": "N",
                "status": "A",
                "telegram_chat_link": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": None,
            },
            "friends_going": 0,
            "friends_of_friends_going": 2,
            "participation_type": "V",
        },
    ],
    "total": 2,
    "has_more": False,
}
