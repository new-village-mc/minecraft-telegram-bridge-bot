FROM python:3.7.5

ENV APP_DIR=/app
WORKDIR "$APP_DIR"

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

COPY . $APP_DIR/

ENTRYPOINT ["sh", "entrypoint.sh"]
