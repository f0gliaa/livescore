FROM python:3.12

RUN pip install pymongo
RUN pip install tornado

WORKDIR .

COPY . .

EXPOSE 8888

CMD ["python3", "livescore.py"]