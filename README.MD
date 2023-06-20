## Run app
1) Create ```.env``` file in project directory
    ```bash
    touch .env
    ```
2) By default, you only need to designate <strong>POSTGRES HOST</strong> and telegram key. <a href="https://t.me/BotFather">Bot Father</a> 
    ```
    TG_BOT_KEY=your key by BotFather
    POSTGRES_HOST=postgres_db
    ```
3) Need check database url in ```alembic.ini``` on 61 line.
   ```
   sqlalchemy.url = postgresql+asyncpg://admin:password@postgres_db:5432/ja_bot
   ```
4) Run ```docker-compose.yaml```
   ```bash
   docker-compose up
   ```

## Local development
#### Environment variables
1) Create ```.env``` file in project directory
    ```bash
    touch .env
    ```
2) By default, you only need to designate telegram key <a href="https://t.me/BotFather">Bot Father</a>
    ```
    TG_BOT_KEY=your key by BotFather
   
    ```
3) ** Other optional variables you can check in ```.env.sample```
    ```bash
    cat .env.sample
    ```
4) ** Default DB setting (FOR LOCAL DEVELOPMENT)
    ```python
   POSTGRES_DRIVER=postgresql+asyncpg
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=ja_bot
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=password
    ```
#### How to start
1) Create db
   ```bash
   docker-compose -f docker-compose-pg-only.yaml up
   ```
2) Need check database url in ```alembic.ini``` on 61 line.
   ```
   sqlalchemy.url = postgresql+asyncpg://admin:password@localhost:5432/ja_bot
   ```
3) In project directory
   ```bash
   make migrate
   python3 -m bot
   ```
#### FAST API app
1) In project directory:
   ```
   uvicorn app.main:app --reload
   ```
2)  http://127.0.0.1:8000/profile/<profile_id>

## flake8 config:
1) install flake8 in your environment
   ```bash
   sudo apt install flake8 -y
   ```
2) add flake8 command in git pre-commit file (```.git/hooks/pre-commit```)
   ```bash
   nano .git/hooks/pre-commit
   ```
   ```
   #!/bin/sh
   flake8 . --ignore=E402,F841,E302,E305,W503 --max-line-length=120 --statistics --show-source --extend-exclude=venv
   ```
   ```bash
   chmod +x .git/hooks/pre-commit
   ```