FROM python:3
ADD ./rest-server /rest-server
WORKDIR /rest-server
RUN pip install -r requirements.txt
CMD ["python", "rest_server.py"]
