## NEXTIMS
---
This repository will serve as a repo for planning, and as a testing environment for the dockerized frontend and backend

## Requirement
- [Docker](https://docs.docker.com/engine/install/) container engine
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) local Kubernetes cluster
- [Skaffold](https://skaffold.dev/docs/install/) to handle the building of the containerized applications, pushing it to our Minikube cluster, and then deploying them
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) to interact with the cluster via Kubernetes API 

<!-- Adapted from https://skaffold.dev/docs/quickstart/ -->
## To start the Minikube cluster for testing
Add user to docker group
```sh
sudo usermod -aG docker $USER
```

Set Skaffold to use local cluster
```
skaffold config set --global local-cluster true
```

Run `./configure.sh` which does these:

- Start Minikube cluster

```sh
minikube start --profile nextims
```
- Points the shell to minikube's docker-daemon
```sh
minikube -p nextims docker-env
```
- Start Skaffold in continuous development mode
```sh
skaffold dev
```