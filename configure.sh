#!/bin/bash

minikube start --profile nextims
minikube -p nextims docker-env
skaffold dev