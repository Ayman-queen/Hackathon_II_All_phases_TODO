# Tasks: Cloud-Native Migration

**Input**: Design documents from `specs/001-cloud-native-migration/`
**Prerequisites**: plan.md, spec.md

## User Story 1: Cloud-Native Deployment

**Goal**: Containerize the application, create Kubernetes manifests, and set up a CI/CD pipeline for automated deployment.

**Independent Test**: The entire application can be deployed to a Kubernetes cluster from scratch using the defined pipeline, and the application will be fully functional.

### Implementation Tasks

- [X] **T-401**: Refactor `frontend/Dockerfile` and `backend/Dockerfile` into multi-stage production builds.
- [X] **T-402**: Create Kubernetes manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`) in the `/k8s` directory for both frontend and backend deployments.
- [X] **T-403**: Set up the GitHub Actions workflow in `.github/workflows/deploy.yml` for automated testing, image building, and pushing to a container registry.
- [X] **T-404**: Add Liveness and Readiness probes to the FastAPI `/health` endpoint in the backend Kubernetes deployment manifest.
