FROM python:3.9
# put you docker configuration here

ENV APP flight-delay

RUN mkdir -p ./flight-delay
WORKDIR ./challenge_MLE
COPY . ./

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade typing_extensions
RUN pip install poetry==1.3.2
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

EXPOSE 8080

CMD uvicorn challenge.api:app --host 0.0.0.0 --port 8080 --loop asyncio --log-level warning