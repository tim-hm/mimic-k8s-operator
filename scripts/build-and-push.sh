#! /bin/bash

set -euxo pipefail

image_name="$(yq '.name' rockcraft.yaml)"
version="$(yq '.version' rockcraft.yaml)"
username=tim-hm

rockcraft pack

rock_file=$(ls *.rock | tail -n 1)

sudo /snap/rockcraft/current/bin/skopeo \
    --insecure-policy \
    copy \
    oci-archive:"${rock_file}" \
    docker-daemon:"ghcr.io/$username/$image_name:$version"

docker push "ghcr.io/$username/$image_name:$version"
