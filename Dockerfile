FROM python:3.6.13

RUN pip3 install Flask==1.1.2 \
                 hotqueue==0.2.8 \
                 matplotlib==3.3.4 \
                 redis==3.5.3

COPY ./source /app/

WORKDIR /app
ENTRYPOINT ["python"]



