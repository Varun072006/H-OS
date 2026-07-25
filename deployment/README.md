# Deployment

Deployment configurations, tooling, and infrastructure-as-code for HumanOS.

## Modules

### `edge/`
Edge device deployment configurations:
- **`jetson/`** — NVIDIA Jetson (Nano, Orin) with TensorRT optimization
- **`coral/`** — Google Coral with Edge TPU runtime
- **`raspberry_pi/`** — Raspberry Pi with ONNX Runtime

### `cloud/`
Cloud deployment infrastructure:
- **`kubernetes/`** — Kubernetes manifests and configurations
- **`terraform/`** — Infrastructure provisioning (AWS, GCP, Azure)
- **`helm/`** — Helm charts for templated Kubernetes deployments

### `docker/`
Docker configurations:
- Multi-stage Dockerfiles for minimal production images
- Docker Compose for local development
- GPU-enabled containers for inference

### `ci/`
CI/CD pipeline configurations:
- GitHub Actions workflows
- Automated testing, linting, and security scanning
- Container image building and publishing
- Release automation

## Deployment Targets

| Target | Runtime | Use Case |
|--------|---------|----------|
| Local Development | Docker Compose | Developer machines |
| Edge Single Device | Docker / Native | Single camera, on-premise |
| Cloud Single Node | Docker on VM | Small-scale |
| Cloud Cluster | Kubernetes + Helm | Production-scale |
