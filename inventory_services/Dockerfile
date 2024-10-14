FROM python:3.12

LABEL maintainer="hasaanqureshi"

WORKDIR /code

RUN apt-get update && apt-get install -y\
    build-essential\
    libpq-dev\
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry

COPY . /code/

RUN poetry install

EXPOSE 8001

CMD [ "poetry" , "run" , "uvicorn" , "inventory_services.main:app" , "--host" , "0.0.0.0" , "--reload"  ]