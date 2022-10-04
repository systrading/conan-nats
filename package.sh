#!/bin/bash

conan create . && \
  conan upload -c "*" --all --remote staconan --force
