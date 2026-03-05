#!/bin/bash

minikube start --profile nextims
minikube -p nextims docker-env
minikube addons enable dashboard -p nextims
minikube addons enable storage-provisioner -p nextims
minikube addons enable storage-provisioner-rancher -p nextims
skaffold dev