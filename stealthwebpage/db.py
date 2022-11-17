from datetime import datetime
from random import random

categories = [{"id": 0, "name": "test_category"}]
users = [{"id": 0, "name": "admin"}]
records = [
        {
            "id":0,
            "user_id": 0,
            "category_id": 0,
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "total": (int)(random()*1000)
        }
]