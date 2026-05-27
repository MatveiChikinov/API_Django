# Учёт сельхозтехники с графиками ТО

REST API для учёта сельскохозяйственной техники и управления техническим обслуживанием.
Разработано на Django REST Framework в рамках учебного задания.

## Стек
- Python 3.10+
- Django 4.2+
- DRF + SimpleJWT + drf-spectacular + drf-extensions
- SQLite (dev) / PostgreSQL (prod)

## Запуск
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver