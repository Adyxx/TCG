# TCG


tcg_project/
│
├── backend/                   # Shared game logic and DB (used by both frontends)
│   ├── game/                  # Game rules, battle systems, effects, etc.
│   │   ├── __init__.py
│   │   ├── engine/
│   │   ├── models/
│   │   ├── registry/
│   │   └── utils/
│   └── db/                    # Django models, migrations, shared schemas
│       ├── __init__.py
│       ├── models.py
│       └── ...
│
├── frontend_desktop/          # PySide6 game client
│   ├── main.py
│   ├── windows/
│   └── assets/
│
├── frontend_web/              # Django web client
│   ├── manage.py
│   └── tcg_web/
│       ├── settings.py
│       ├── urls.py
│       └── apps/
│           └── game/
│               ├── views.py
│               ├── templates/
│               └── ...
│
├── data/                      # Optional: YAML/CSV test decks, characters
├── scripts/                   # Populate DB, export deck, etc.
├── tests/
├── requirements.txt
└── README.md
