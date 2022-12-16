FROM    alpine:latest AS alpine_local
RUN     apk add wget
ENV     WORKDIR="/usr/local/"
WORKDIR ${WORKDIR}

FROM    python:3.11 AS python_local
RUN     pip install --upgrade pip

FROM    alpine_local AS influxdb
ARG     RELEASE
RUN     wget -qO- "https://dl.influxdata.com/influxdb/releases/influxdb${RELEASE}-linux-amd64.tar.gz" | tar -xzf -
WORKDIR ${WORKDIR}/influxdb2-2.0.9-linux-amd64/
RUN     cp influx influxd /usr/local/bin
EXPOSE  8086
CMD     ["/bin/sh", "-c", "influxd"]

FROM    alpine_local AS activemq
ARG     RELEASE
RUN     apk add openjdk17-jre
RUN     wget -qO- "https://archive.apache.org/dist/activemq/${RELEASE}/apache-activemq-${RELEASE}-bin.tar.gz" | tar -xzf -
WORKDIR ${WORKDIR}/apache-activemq-${RELEASE}
RUN     sed -i 's/127\.0\.0\.1/0\.0\.0\.0/g' conf/jetty.xml
EXPOSE  8161
CMD     ["/bin/sh", "-c", "bin/activemq console"]

FROM    python_local AS ticker
WORKDIR ${WORKDIR}/python
COPY    requirements.txt .
RUN     pip install -r requirements.txt
COPY    main.py .
CMD     ["/usr/local/bin/python", "main.py"]