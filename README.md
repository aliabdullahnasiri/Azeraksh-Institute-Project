# Azeraksh Institute Project 


## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate # on Windows: .venv\Scripts\activate
pip install -r requirements.txt


# Set environment (Flask auto-loads .env)
export FLASK_APP=manage.py # Windows: set FLASK_APP=manage.py


# Initialize database
flask db init
flask db migrate -m "init"
flask db upgrade


# Run
flask run
```
