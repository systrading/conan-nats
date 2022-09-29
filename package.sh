#!/bin/bash

conan create . 
conan upload -c "*" --remote staconan --force
