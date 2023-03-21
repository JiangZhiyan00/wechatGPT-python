FROM python:3.9-slim

WORKDIR /usr/local/app/

ENV TZ=Japan

ADD src ./src
ADD requirements.txt /usr/local/app/requirements.txt

#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && $TZ > /etc/timezone
RUN pip3 install -r requirements.txt

EXPOSE 8009

ENTRYPOINT ["python3", "/usr/local/app/src/main.py"]