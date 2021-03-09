
FROM python:3.8-slim

WORKDIR /app
COPY hello-world-module.py hello-world-module.py
ENV FORMAT "dummy format"
ENV DATAPATH "dummy datapath"
ENV NAME "dummy data asset name"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pyyaml
ENTRYPOINT ["python3"]
CMD ["hello-world-module.py"]

