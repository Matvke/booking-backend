# booking-backend
Сервис для записи на прием к специалисту. API для Telegram-бота
## Запуск тестов
1) Перейти в директорию src `cd src`
2) Заупустить тесты `pytest`

## Запуск приложения
1) Перейти в директорию src `cd src`
2) Применить миграции `alembic upgrade head`
3) Запустить сервер `uvicorn app.main:app`
