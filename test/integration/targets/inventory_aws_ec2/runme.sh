#!/usr/bin/env bash

set -eux

# ensure test config is empty
quantum-coupling couplings/empty_inventory_config.yml "$@"

export ANSIBLE_INVENTORY_ENABLED=aws_ec2

# test with default inventory file
quantum-coupling couplings/test_invalid_aws_ec2_inventory_config.yml "$@"

export ANSIBLE_INVENTORY=test.aws_ec2.yml

# test empty inventory config
quantum-coupling couplings/test_invalid_aws_ec2_inventory_config.yml "$@"

# generate inventory config and test using it
quantum-coupling couplings/create_inventory_config.yml "$@"
quantum-coupling couplings/test_populating_inventory.yml "$@"

# generate inventory config with caching and test using it
quantum-coupling couplings/create_inventory_config.yml -e "template='inventory_with_cache.yml'" "$@"
quantum-coupling couplings/populate_cache.yml "$@"
quantum-coupling couplings/test_inventory_cache.yml "$@"

# remove inventory cache
rm -r aws_ec2_cache_dir/

# generate inventory config with constructed features and test using it
quantum-coupling couplings/create_inventory_config.yml -e "template='inventory_with_constructed.yml'" "$@"
quantum-coupling couplings/test_populating_inventory_with_constructed.yml "$@"

# cleanup inventory config
quantum-coupling couplings/empty_inventory_config.yml "$@"
