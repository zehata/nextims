#!/bin/bash

# Allocate more memory to minikube if you would like to
# minikube config set memory 4096
minikube start --profile nextims
minikube -p nextims docker-env
minikube addons enable dashboard -p nextims
minikube addons enable storage-provisioner-rancher -p nextims
skaffold dev