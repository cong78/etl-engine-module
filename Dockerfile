
FROM python:3.8-slim

WORKDIR /app
COPY hello-world-module.py hello-world-module.py
ENV FORMAT "dummy format"
ENV DATAPATH "dummy datapath"
ENV NAME "dummy data asset name"
ENTRYPOINT ["python3"]
CMD ["hello-world-module.py"]

