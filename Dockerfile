FROM tensorflow/tensorflow:latest
#FROM python:3.8
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
#RUN pip install tensorflow
RUN pip install -r requirements.txt
EXPOSE 10000

CMD ["python","app.py"]
