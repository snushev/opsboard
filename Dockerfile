
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY ./requirements.txt requirements.txt


RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .


CMD ["uvicorn", "src.opsboard.main:app", "--host", "0.0.0.0", "--port", "8000"]
