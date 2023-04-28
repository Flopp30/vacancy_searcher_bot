### Local development
#### flake8 config:
1) install flake8 in your environment
```bash
sudo apt install flake8 -y
```
2) add flake8 command in pre-commit file
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
4) ** Default DB setting (no need to specify in .env)
    ```python
    DB_DRIVER = "postgresql+asyncpg"
    DB_HOST = "localhost"
    DB_PORT="5432"
    DB_NAME = "ja_bot"
    DB_USER = "admin"
    DB_PASSWORD = "password"
    ```


