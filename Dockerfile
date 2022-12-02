FROM python:3.9.7
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
COPY . /bot
CMD python main.py