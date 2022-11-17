from datetime import datetime
from random import random

categories = [{"id": 0, "name": "test_category"}]
users = [{"id": 0, "name": "admin"}]
records = [
        {
            "id":0,
            "userId": 0,
            "categoryId": 0,
            "date_time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "total": (int)(random()*1000)
        }
]