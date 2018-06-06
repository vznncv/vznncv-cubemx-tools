#!/usr/bin/env bash
# Helper script to build project from cmake file
set -e

build_dir="{{ build_dir }}"
if [ ! -d "$build_dir" ]; then
    mkdir "$build_dir"
fi

cd "$build_dir"
cmake ..
cmake --build .
