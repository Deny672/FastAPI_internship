To run the application:
You must fill in the .env file, POSTGRES_HOST=localhost
Windows:

git clone https://github.com/Deny672/Meduzzen_Backend_Fastapi cd Meduzzen_Backend_Fastapi pip install pipenv python -m venv venv .\venv\Scripts\activate pip install -r requirements_base.txt alembic upgrade head uvicorn app.main:app --host 127.0.0.1 --port 8056 --reload

Unix system:

git clone https://github.com/Deny672/Meduzzen_Backend_Fastapi cd Meduzzen_Backend_Fastapi pip install pipenv python3 -m venv venv source venv/bin/activate pip install -r requirements_base.txt alembic upgrade head uvicorn app.main:app --host 127.0.0.1 --port 8056 --reload

To run the application in Docker:
You must fill in the .env file, POSTGRES_HOST=db
git clone https://github.com/Deny672/Meduzzen_Backend_Fastap cd Meduzzen_Backend_Fastapi docker compose up docker-compose exec app alembic upgrade head



To run the test
pip install -r requirements_dev.txt
alembic upgrade head
pytest