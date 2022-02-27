FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip \
&& apt-get update && apt-get install -y graphviz graphviz-dev \
&& apt-get install -y default-jre \
&& apt-get install -y postgresql-client  

COPY ./requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG env=localhost
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
EXPOSE 8888

ARG SEED_DATA=no
ENV SEED_DATA=${SEED_DATA}

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80
