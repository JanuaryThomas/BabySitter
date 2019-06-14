FROM python:3.6

RUN adduser -D intelecs
MAINTAINER Intelecs

WORKDIR C:/Users/Administrator/Desktop/InfinityLabs/Projects/OpenHardware/IoTBasedCarTracking/CarCount

COPY requirements.txt requirements.txt
RUN pip install -r requirements
COPY app app
COPY migrations migrations
EXPOSE 5000
CMD ["python",  "manage.py", "runserver"]