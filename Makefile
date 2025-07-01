# Makefile
# Variables
DOCKER_CONFIG ?= /tmp/docker-config-noauth
IMAGE ?= sicar
DOCKERFILE ?= Dockerfile

# Build Docker image
build:
	@echo "🛠️  Buildando imagem $(IMAGE):latest via $(DOCKERFILE)..."
	docker build -t $(IMAGE):latest -f $(DOCKERFILE) .

# Run container with optional command
run:
	@echo "🚀 Executando container $(IMAGE):latest..."
	DOCKER_CONFIG=$(DOCKER_CONFIG) docker run -it --rm -v $(PWD):/sicar $(IMAGE):latest $(CMD)

# Open shell inside container
shell:
	@echo "🔗 Entrando no container $(IMAGE)..."
	DOCKER_CONFIG=$(DOCKER_CONFIG) docker run -it --rm -v $(PWD):/sicar $(IMAGE):latest bash

# Remove local image
clean:
	@echo "🗑️  Removendo imagem $(IMAGE):latest..."
	docker rmi $(IMAGE):latest

# Execute Python unit tests
unit-test:
	@echo "🧪 Executando testes unitários..."
	python -m unittest SICAR/tests/unit/*.py SICAR/tests/unit/drivers/*.py

# Execute Python integration tests
integration-test:
	@echo "🧪 Executando testes de integração..."
	python -m unittest SICAR/tests/integration/*.py

test: unit-test integration-test

