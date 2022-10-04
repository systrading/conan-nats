#!/bin/bash

conan create . --build=missing && \
  conan upload -c "*" --check --all --remote staconan
