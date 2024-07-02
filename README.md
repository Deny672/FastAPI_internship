To run the application:

Windows:

git clone https://github.com/Deny672/Meduzzen_Backend_Fastapi cd Meduzzen_Backend_Fastapi pip install pipenv python -m venv venv .\venv\Scripts\activate pip install -r requirements_base.txt python -m app.main

Unix system:

git clone https://github.com/Deny672/Meduzzen_Backend_Fastapi cd Meduzzen_Backend_Fastapi pip install pipenv python3 -m venv venv source venv/bin/activate pip install -r requirements_base.txt python -m app.main


To run the test
pip install -r requirements_dev.txt
pytest