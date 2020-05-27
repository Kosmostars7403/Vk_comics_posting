# Публикация комиксов сообщество Вконтакте
Скрипт создан для скачаивания случайного комикса с [xkcd.com](xkcd.com) и публикации его в сообщество Вконтакте.

### Как установить

Для работы скрипта необходим установленный интерпретатор Python3. Затем загрузите зависимости с помощью "pip"
(либо "pip3", в случае конфликтов с Python2):
```
pip install -r requirements.txt
```
В директории со скриптом создайте файл ".env", в который поместите следующие чувствительные данные:
`VK_USER_TOKEN` - токен пользователя. Для его получения создайте приложение Вконтакте, а затем отправьте запрос
как в документации по ссылке [https://vk.com/dev/implicit_flow_user](implicit_flow_user)
`API_VERSION` - узнайте актуальную версию API (узнать из документации API)
`GROUP_ID` - id вашего сообщества Вконтакте (узнать из адресной строки)

### Как использовать
Для запуска скрипта введите команду
`python vk_comics_posting.py` - для постинга фотографий
После этого проверьте свое сообщество, если все сделано верно - там будет красоваться новый пост.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org).
