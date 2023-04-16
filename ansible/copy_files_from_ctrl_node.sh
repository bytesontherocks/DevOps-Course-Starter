#!/bin/bash

scp ex4:/home/ec2-user/guillem/* .
git add .
git commit -m "$1"