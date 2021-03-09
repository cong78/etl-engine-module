export DOCKER_USERNAME ?= eletonia
export DOCKER_PASSWORD ?= 
export DOCKER_HOSTNAME ?= ghcr.io
export DOCKER_NAMESPACE ?= eletonia
export DOCKER_TAGNAME ?= latest

DOCKER_IMG_NAME ?= hw-module
DOCKER_CHART_IMG_NAME ?= hw-module-chart
DOCKER_FILE ?= Dockerfile
DOCKER_CONTEXT ?= .

APP_IMG ?= ${DOCKER_HOSTNAME}/${DOCKER_NAMESPACE}/${DOCKER_IMG_NAME}:${DOCKER_TAGNAME}
CHART_IMG ?= ${DOCKER_HOSTNAME}/${DOCKER_NAMESPACE}/${DOCKER_CHART_IMG_NAME}:${DOCKER_TAGNAME}

.PHONY: docker-all
docker-all: docker-build docker-push

.PHONY: docker-build
docker-build:
	docker build $(DOCKER_CONTEXT) -t ${APP_IMG} -f $(DOCKER_FILE)

.PHONY: docker-push
docker-push:
ifneq (${DOCKER_PASSWORD},)
	@docker login \
		--username ${DOCKER_USERNAME} \
		--password ${DOCKER_PASSWORD} ${DOCKER_HOSTNAME}
endif
	docker push ${APP_IMG}

.PHONY: docker-rmi
docker-rmi:
	docker rmi ${APP_IMG} || true

HELM_VALUES ?= \
	--set hello=world1

CHART := ${DOCKER_IMG_NAME}
HELM_RELEASE ?= rel1-${DOCKER_IMG_NAME}
TEMP := /tmp

export HELM_EXPERIMENTAL_OCI=1
export GODEBUG=x509ignoreCN=0

.PHONY: helm-login
helm-login: 
ifneq (${DOCKER_PASSWORD},)
	helm registry login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}" ${DOCKER_HOSTNAME}
endif

.PHONY: helm-verify
helm-verify: 
	helm lint ${CHART}
	helm install --dry-run ${HELM_RELEASE} ${CHART} ${HELM_VALUES}

.PHONY: helm-uninstall
helm-uninstall: 
	helm uninstall ${HELM_RELEASE} || true

.PHONY: helm-install
helm-install: 
	helm install ${HELM_RELEASE} ${CHART} ${HELM_VALUES}

.PHONY: helm-chart-push
helm-chart-push: helm-login 
	helm chart save ${CHART} ${CHART_IMG}
	helm chart list ${CHART_IMG}
	helm chart push ${CHART_IMG}
	helm chart remove ${CHART_IMG}

.PHONY: helm-chart-pull
helm-chart-pull: helm-login 
	helm chart pull ${CHART_IMG} 
	helm chart list

.PHONY: helm-chart-list
helm-chart-list: 
	helm chart list

.PHONY: helm-chart-install
helm-chart-install: 
	helm chart export --destination=${TEMP} ${CHART_IMG} 
	helm install ${HELM_RELEASE} ${TEMP}/${CHART} ${HELM_VALUES}
	helm list

.PHONY: helm-template
helm-template: 
	helm template ${HELM_RELEASE} ${CHART} ${HELM_VALUES}

.PHONY: helm-debug
helm-debug: helm
	helm template ${HELM_RELEASE} ${CHART} ${HELM_VALUES} --debug

.PHONY: helm-actions
helm-actions:
	helm show values ${CHART} | yq -y -r .actions

.PHONY: helm-all
helm-all: helm-verify helm-chart-push helm-chart-pull helm-uninstall helm-chart-install