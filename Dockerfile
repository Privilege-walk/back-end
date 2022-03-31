FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt
COPY . /code/

ENV PORT=8000
EXPOSE 8000
