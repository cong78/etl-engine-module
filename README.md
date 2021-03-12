# ETL Engine Module
## A Helm Chart for an example Mesh for Data module

## Introduction

This module is used in the project of [the-mesh-for-data](https://github.com/IBM/the-mesh-for-data) for interacting with ETL engines, such as Data Stage, to schedule, run and manage the ETL jobs as a client. 

### Data Stage Integration:
For the first integration with Data Stage, it will use the [Data Stage API](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.ds.fd.doc/topics/rest_api.html#run) to run the job and get the job status. 


## Prerequisites

- Kubernetes cluster 1.10+
- Helm 3.0.0+

## Installation

### Modify values in Makefile

In `Makefile`:
- Change `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `DOCKER_HOSTNAME`, `DOCKER_NAMESPACE`, `DOCKER_TAGNAME`, `DOCKER_IMG_NAME`, and `DOCKER_CHART_IMG_NAME` to your own preferences.

### Build Docker image for Python application
```bash
make docker-build
```

### Push Docker image to your preferred container registry
```bash
make docker-push
```

### Configure the chart

- Settings can configured by editing the `values.yaml` directly.
- Modify repository in `values.yaml` to your preferred Docker image. 
- Modify copy/read action as needed with appropriate values. 

### Login to Helm registry
```bash
make helm-login
```

### Lint and install Helm chart
```bash
make helm-verify
```

### Push the Helm chart

```bash
make helm-chart-push
```

## Uninstallation
```bash
make helm-uninstall
```

## Deploy M4D application which triggers module (WIP)
1. In `etl-engine-module.yaml`:
    * Change `spec.chart.name` to your preferred chart image.
    * Define `flows` and `capabilities` for your module. 

2. Deploy `M4DModule` in `m4d-system` namespace:
```bash
oc project m4d-system
oc create -f etl-engine-module.yaml
```
3. In `m4dapplication.yaml`:
    * Change `metadata.name` to your application name.
    * Define `appInfo.purpose`, `appInfo.role`, and `spec.data`
    * This ensures that a copy is triggered:
    ```yaml
    copy:
      required:true
    ```
4.  Deploy `M4DApplication` in `default` namespace:
```bash
oc project default
oc create -f m4dapplication.yaml
```
5.  Check if `M4DApplication` successfully deployed:
```bash
oc describe M4DApplication etl-engine-module-test
```

6.  Check if module was triggered in `m4d-blueprints`:
```bash
oc project m4d-blueprints
oc get job
oc get pods
```
If you are using the `etl-engine-module` image, you should see this in the `oc logs` of your completed Pod:
```
$ oc logs rel1-etl-engine-module-z9vnl

Hello World Module!

Connection name is s3

Connection format is parquet

Connection credential location is /v1/m4d/dataset-creds/m4d-test-bucket

S3 bucket is m4d-test-bucket

S3 endpoint is s3.eu-gb.cloud-object-storage.appdomain.cloud

COPY SUCCEEDED
```


