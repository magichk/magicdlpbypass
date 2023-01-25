FROM python:3.8-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python", "server.py", "-d", "/data", "-i", "172.17.0.2", "-p", "9443"]
#CMD ["/bin/sh"]
EXPOSE 8080

