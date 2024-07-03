FROM python:3.11.9

WORKDIR /app

COPY ./ /app

COPY ./requirements_dev.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]