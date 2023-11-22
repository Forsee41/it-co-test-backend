FROM python:3.11-alpine

WORKDIR /app
RUN mkdir it_co_test
RUN mkdir migrations
COPY it_co_test it_co_test
COPY migrations migrations
COPY requirements.txt .
COPY alembic.ini .
COPY run.py .
COPY run.sh .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x run.sh
CMD [ "./run.sh"] 
