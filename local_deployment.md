# Local Deployment Instructions

This guide provides instructions for deploying the application locally using Docker and Kubernetes.

## Prerequisites

- Docker installed and running.
- A local Kubernetes cluster (e.g., Minikube, Docker Desktop Kubernetes).
- `kubectl` installed and configured to connect to your local cluster.

## 1. Build Docker Images

First, you need to build the Docker images for the frontend, backend, and MCP server.

### Backend Image

```bash
docker build -t evo-todo-backend:latest -f backend/Dockerfile .
```

### Frontend Image

```bash
docker build -t evo-todo-frontend:latest -f frontend/Dockerfile .
```

### MCP Server Image

```bash
docker build -t evo-todo-mcp-server:latest -f backend/mcp_server.Dockerfile .
```

**Note for Minikube users:** If you are using Minikube, you can build the images directly into Minikube's Docker daemon by running the following command first:

```bash
eval $(minikube -p minikube docker-env)
```

## 2. (Optional) Push Docker Images to a Registry

If your Kubernetes cluster does not have access to your local Docker images, you will need to push them to a container registry.

First, tag the images with your registry's URL:

```bash
docker tag evo-todo-backend:latest your-registry-url/evo-todo-backend:latest
docker tag evo-todo-frontend:latest your-registry-url/evo-todo-frontend:latest
docker tag evo-todo-mcp-server:latest your-registry-url/evo-todo-mcp-server:latest
```

Then, push them:

```bash
docker push your-registry-url/evo-todo-backend:latest
docker push your-registry-url/evo-todo-frontend:latest
docker push your-registry-url/evo-todo-mcp-server:latest
```

## 3. Update Kubernetes Manifests

If you pushed your images to a registry, you need to update the `image` field in `k8s/deployment.yaml` to point to your images.

For example, change:
`image: evo-todo-backend:latest`
to:
`image: your-registry-url/evo-todo-backend:latest`

## 4. Deploy to Kubernetes

Now you can deploy the application to your Kubernetes cluster using the manifests in the `k8s` directory.

```bash
kubectl apply -f k8s/
```

This will create the deployments, services, and horizontal pod autoscalers for the frontend, backend, and MCP server.

## 5. Access the Application

To access the application, you need to find the external IP address of the frontend service.

```bash
kubectl get services frontend-service
```

Look for the `EXTERNAL-IP` address in the output. It might take a few minutes for the external IP to be available.

Once you have the external IP, you can access the application in your browser at `http://<EXTERNAL-IP>`.

If you are using Minikube, you can get the URL by running:

```bash
minikube service frontend-service
```

The `mcp-server` is exposed as a `ClusterIP` service, so it is only accessible from within the Kubernetes cluster.

## 6. Cleanup

To remove the deployment from your cluster, run the following command:

```bash
kubectl delete -f k8s/
```
