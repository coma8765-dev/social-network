ARG VERSION="3.11-alpine3.16"

FROM python:$VERSION as builder

WORKDIR /app


RUN pip install pipenv  && \
    apk add gcc g++ python3-dev libffi-dev

ADD Pipfile* ./
RUN pipenv install --dev --skip-lock

ADD app /app/app

EXPOSE 8000
CMD pipenv run uvicorn app.app:app --host 0.0.0.0
