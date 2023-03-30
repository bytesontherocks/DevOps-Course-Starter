#!/bin/bash

curl -sSL https://install.python-poetry.org | python3 -

cd /opt/todoapp

/home/ec2-user/.local/bin/poetry install
