
FROM python:3.14


WORKDIR /app


COPY ./requirements.txt requirements.txt


RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .


CMD ["fastapi", "run", "src/opsboard/main.py", "--port", "8000"]
