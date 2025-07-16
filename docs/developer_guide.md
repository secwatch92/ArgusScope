# راهنمای توسعه‌دهنده ArgusScope

## استانداردهای کدنویسی
- پیروی از PEP-8
- استفاده از type hints در تمام توابع
- نام‌گذاری متغیرها به انگلیسی و توصیفی

## فرآیند تست
```bash
# اجرای تمام تست‌ها
pytest tests/ --cov=argus_scope

# اجرای تست‌های عملکرد
locust -f tests/load/test_performance.py
```

## خط لوله CI/CD
- تست‌های واحد پس از هر commit
- اسکن امنیتی هفتگی
- استقرار خودکار در محیط staging

## الگوی کامنت‌گذاری
```python
def scan_target(target: str):
    """اجرای اسکن کامل روی هدف مشخص شده

    Args:
        target: دامنه یا IP هدف
    
    Returns:
        dict: نتایج اسکن شامل زیردامنه‌ها و آسیب‌پذیری‌ها
    
    Raises:
        InvalidTargetError: اگر فرمت هدف نامعتبر باشد
    """
```
