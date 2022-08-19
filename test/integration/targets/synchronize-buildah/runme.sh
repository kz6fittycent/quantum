#!/usr/bin/env bash

set -ux

CONTAINER_NAME=buildah-container

buildah rm $CONTAINER_NAME >/dev/null 2>/dev/null

set -e

buildah from --name $CONTAINER_NAME docker.io/library/centos:7
trap '{ buildah rm $CONTAINER_NAME; }' EXIT
buildah run $CONTAINER_NAME -- yum install -y rsync

quantum-coupling test_synchronize_buildah.yml -c buildah -i inventory -vv
