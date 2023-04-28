flake8 config:
1) install flake8 in you environment
```bash
sudo apt install flake8 -y
```
2) 
flake8 . --ignore=E402,F841,E302,E305,W503 --max-line-length=120 --statistics --show-source --extend-exclude=venv
