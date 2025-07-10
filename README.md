# TCG

```
tcg_project/
│   requirements.txt
│
├───backend
│   │   admin.py
│   │   apps.py
│   │   __init__.py
│   │
│   ├───core
│   │       config.py
│   │
│   ├───engine
│   │       core_loop.py
│   │
│   ├───migrations
│   │       __init__.py
│   │
│   ├───models
│   │       ability.py
│   │       card.py
│   │       character.py
│   │       deck.py
│   │       deck_card.py
│   │       match.py
│   │       users.py
│   │       __init__.py
│   │
│   ├───registry
│   │       effects.py
│   │
│   ├───schemas
│   │       ability.py
│   │       card.py
│   │       character.py
│   │       deck.py
│   │       deck_card.py
│   │       match.py
│   │       users.py
│   │
│   └───services
│           ability_service.py
│           card_service.py
│           character_service.py
│           deck_card_service.py
│           deck_service.py
│           match_service.py
│           user_service.py
│
├───data
├───frontend_desktop
│   │   main.py
│   │
│   ├───assets
│   ├───controllers
│   └───windows
├───frontend_web
│   │   manage.py
│   │
│   ├───dbbridge
│   │   │   admin.py
│   │   │   apps.py
│   │   │   models.py
│   │   │   tests.py
│   │   │   views.py
│   │   │   __init__.py
│   │   │
│   │   └───migrations
│   │           __init__.py
│   │
│   └───frontend_web
│           asgi.py
│           settings.py
│           urls.py
│           wsgi.py
│           __init__.py
│
└───scripts
        seed.py
```
