#! /usr/bin/env bash

sudo docker compose up -d

wait

ansible-playbook site.yml -i inventory/prod.yml --ask-vault-password

sudo docker compose down
