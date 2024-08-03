#!/bin/sh
sed "s/tagVersion/$1/g" kubernetes-manifest/deployment.yaml > kubernetes-manifest/deployment.yaml.tmp && mv kubernetes-manifest/deployment.yaml.tmp kubernetes-manifest/deployment.yaml
