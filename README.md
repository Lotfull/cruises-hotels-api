# cruises-hotels-api

### API метод для получения списка отелей с ограничением количества комнат: 
    
    http://185.228.233.249:8002/hotels?room_limit=20
    http://localhost:8000/hotels?room_limit=20

Результат: список отелей в формате JSON
    
    [
        {
            "id": 22,
            "link": "http://hotel-1.com",
            "room_count": 14
        },
        ...
    ]

### API метод для получения списка круизов с сайта https://www.lueftner-cruises.com/en/river-cruises/cruise.html: 
    
    http://185.228.233.249:8002/cruises?num=4
    http://localhost:8000/cruises?num=4

Результат: список круизов в формате JSON
    
    [
        {
            "name": "Magic of Advent on the Rhine",
            "days": 5,
            "itinerary": [
                "Cologne",
                "Koblenz",
                "Rüdesheim",
                "Speyer",
                "Strassbourg",
                "Strassbourg"
            ],
            "dates": [
                {
                    "2020-11-28": {
                        "ship": "MS Amadeus Imperial",
                        "price": 560.15
                    }
                }
            ]
        },
        ...
    ]

Гитхаб репозиторий: https://github.com/Lotfull/cruises-hotels-api

Приложение доступно по ссылке: 185.228.233.249:8002/

Используется Docker

# Launch

## Settings
Настройки API могут быть изменены в файле `.env`

Запуск Django в режиме DEBUG=False если DEBUG=False, по умолчанию DEBUG=True:
   
    DEBUG=True

Имя хоста для удалённого запуска:
   
    HOST_IP=185.228.233.249

Имя хоста для базы данных:
   
    DB_HOST=db
    
Параметры БД:

    POSTGRES_DB=postgres
    POSTGRES_USER=postgres

## Local

    pip3 install -r requirements.txt
    cp -n .env_example .env
    python3 manage.py migrate
    python3 -u manage.py runserver
    
## Docker

    docker-compose up -d
    docker exec $(docker ps -a | grep sintezis_app | awk '{print $1}') python3 manage.py migrate; python3 manage.py fake_db