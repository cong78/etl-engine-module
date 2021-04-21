
FROM python:3.8-slim

WORKDIR /app
COPY data-stage/etl-engine-module.py etl-engine-module.py
COPY data-stage/vault.py vault.py
COPY data-stage/confDataStage.yaml confDataStage.yaml
COPY data-stage/parameters.json parameters.json

ENV NAME "M4D ETL engine module"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pyyaml && \
    pip install --no-cache-dir requests
ENTRYPOINT ["python3"]
CMD ["etl-engine-module.py"]

