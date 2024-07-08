FROM python:3.11.9

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements_dev.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]