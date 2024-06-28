FROM python:3.9-slim

# Install MongoDB tools
RUN apt-get update && apt-get install -y gnupg wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update && apt-get install -y mongodb-org-tools

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python -m app.db.init_db && uvicorn app.main:app --host :: --port ${PORT}"]
