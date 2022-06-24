# Pseudo roulette
REST API на django (DRF) для рулетки с 10 цифровыми ячейками и с 1 ячейкой "джекпот".

![](https://github.com/IvanPragma/pseudo-roulette/actions/workflows/django.yml/badge.svg)

## Запуск
- Перейдите в каталог с проектом
- Выполните `cd pseudo_roulette`
- Установите `SECRET_KEY` в свое окружение
  > Windows: `set SECRET_KEY={SECRET_KEY}`
  > 
  > Linux: `export SECRET_KEY={SECRET_KEY}`
- Укажите данные для коннекта к базе данных в `pseudo_roulette/settings.py`
- Запустите тестовый веб-сервер `python manage.py runserver`

## Использование
- Для прокрутки рулетки отправьте `POST` запрос на `http://localhost:8000/scroll/`
  > Запрос должен содержать JSON словарь с ключом: `user_id`
- Для получения кол-во игроков, которое поучаствовало в рулетках отправьте `GET`
  запрос на `http://localhost:8000/stats/players-count/`
  > Ответом будет JSON список раундов, каждый раунд это список,
  > в котором 1-ый элемент это номер раунда, а 2-ой - кол-во игроков
- Для получения списка самых активных пользователей отправьте `GET`
  запрос на `http://localhost:8000/stats/top-players/`
  > Ответом будет JSON список игроков, каждый игрок это словарь с ключами:
  > `user_id`, `rounds_count`, `average_roulette_spins`
