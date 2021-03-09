# Hello World Module
## A Helm Chart for an example Mesh for Data module

## Introduction

This helm chart defines a common structure to deploy a Kubernetes job for an M4D module.

The configuration for the chart is in the values file.

## Prerequisites

- Kubernetes cluster 1.10+
- Helm 3.0.0+
- PV provisioner support in the underlying infrastructure.

## Installation

### Add Helm repository

```bash
helm repo add hw-module https://ghcr.io/eletonia/hw-module-chart
helm repo update
```

### Configure the chart

Settings can configured by editing the `values.yaml` directly (need to download the chart first).

### Install the chart

```bash
make helm-verify
```

## Uninstallation

To uninstall/delete the `my-release` deployment:

```bash
make helm-uninstall
```

## Configuration

The following table lists the configurable parameters of the job chart and the default values.

| Parameter                                                                   | Description                                                                                                        | Default                         |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------| ------------------------------- |

TBD
