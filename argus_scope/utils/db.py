# مسیر فایل: argus_scope/utils/db.py
# یک کارخانه کوچک برای ساختن و تحویل دادن مدیر پایگاه داده.
# این کار به ما کمک می‌کند تا کد تمیزتر و قابل تست‌تری داشته باشیم.

import os
from functools import lru_cache
from argus_scope.database.db_manager import DatabaseManager

# رشته اتصال از متغیرهای محیطی خوانده می‌شود.
MONGO_URI = os.getenv("DATABASE_URL", "mongodb://mongodb:27017/")

@lru_cache()
def get_db_manager() -> DatabaseManager:
    """
    یک نمونه از DatabaseManager را با استفاده از کش ایجاد و برمی‌گرداند
    تا از ساخت نمونه‌های متعدد جلوگیری شود.
    """
    return DatabaseManager(connection_uri=MONGO_URI)
