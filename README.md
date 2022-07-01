# «Продуктовый помощник»

Входные данные:
__http://84.201.152.243__
__login: markushoka@gmail.com__
__pass: mark51__

## Описание:

Foodgram или "Продуктовый помощник" - ресурс, который позволяет пользователям создавать свои рецепты и делиться ими с другими. Зарегистрированные пользователи могут добавлять понравившиеся рецепты в список Избранного, а также имеют возможность собрать свою Корзину, чтобы в дальнейшем загрузить Список покупок в формате PDF.

## Примечания:

- REST API собран в отдельном приложении "*api*" (реализованы запросы к приложению "*recipes*", включающего в себя модели Recipe, Tag, Ingredient, Favorite, Cart).
- У неаутентифицированных пользователей доступ к API должен быть __только на чтение__ общего списка. Остальные действия доступны уже __аутентифицированным пользователям__
- Аутентификация выполняется с помощью __djoser-токена__.
- Аутентифицированный пользователь авторизован на изменение и удаление __своего__ контента; в остальных случаях доступ предоставляется только для чтения. 
- В ответ на запросы POST, PUT и PATCH ваш API __возвращает объект__, который был добавлен или изменён.
- Согласно ТЗ в проекте широко применены __вьюсеты__.

## Установка и запуск проекта:

1. Установите Docker и Docker-compose
```
sudo apt install docker.io
sudo apt-get update
sudo apt-get install docker-compose-plugin
``` 

2. Создайте файл .env в папке со скопированными из репозитория файлами со следующим содержимым:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=#(z2cp#y
```

3. Склонируйте репозиторий
```
git clone https://github.com/MarkMazurov/foodgram-project-react.git
```

4. Перейдите в папку infra и запустите проект:
```
sudo docker-compose up -d --build
```

5. Проведите миграции, загрузите ингредиенты в базу и соберите статику:  (id контейнера - backend)
```
sudo docker-compose exec <CONTAINER ID> python3 manage.py makemigrations
sudo docker-compose exec <CONTAINER ID> python3 manage.py migrate
sudo docker-compose exec <CONTAINER ID> python3 manage.py load_from_csv
sudo docker-compose exec <CONTAINER ID> python3 manage.py collectstatic --no-input
```

6. Создайте суперпользователя для сайта:
```
sudo docker-compose exec <CONTAINER ID> python3 manage.py createsuperuser
```

7. Зайдите в админку сайта и создайте теги рецептов.

### Примеры запросов:

Для взаимодействия с ресурсами настроены следующие эндпоинты:
- `api/users/` (GET, POST): передаём логин, имя, фамилию, почту и пароль - создается новый пользователь.
- `api/users/me/` (GET, POST): данные или изменить о себе.
- `api/users/{user_id}/` (GET): получить данные о другом пользователе (для подписки, просмотра рецептов автора).
- `api/auth/token/login/` (POST): передаём email и пароль, получаем токен (авторизация).
- `api/auth/token/login/` (POST): передаём токен в заголовке, далее - выход из лк.
- `api/recipes/` (GET, POST): получаем список всех рецептов или создаём новый рецепт.
- `api/recipes/{recipes_id}/` (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем рецепт по id.
- `api/tags/` (GET): получаем список всех тегов.
- `api/tags/{tag_id}/` (GET):  получаем информацию о теге по id.
- `api/igredients/` (GET): получаем список всех ингредиентов.
- `api/igredients/{igredient_id}/` (GET):  получаем информацию о ингредиенте по id.
- `api/recipes/{recipes_id}/favorite` (GET, POST): подписаться, отписаться или получить список всех избранных постов.
- `api/recipes/{recipes_id}/cart` (GET, POST): добавить, удалить или получить список всех рецептов в корзине.
- `api/recipes/download_shopping_cart` (GET): получить список ингредиентов в формате pdf.

## Автор проекта:

<h3 align="center"><a href="https://github.com/MarkMazurov" target="_blank">#Марк Мазуров#</a> 
</h3>