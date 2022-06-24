FROM python:3.9
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY pseudo_roulette/ .
ENV DEBUG=False
ENV SECRET_KEY="SECRET_KEY"
ENV DATABASE_HOST="localhost"
ENV DATABASE_USER="postgres"
ENV DATABASE_PASSWORD="postgres"
ENV DATABASE_NAME="main"
EXPOSE 8000
ENTRYPOINT [ "python", "./manage.py", "runserver" ]