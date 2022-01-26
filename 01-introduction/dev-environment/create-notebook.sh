#!/bin/bash

new-notebook() {
    file_name="$1.ipynb"
    echo "{
    \"cells\": [],
    \"metadata\": {},
    \"nbformat\": 4,
    \"nbformat_minor\": 2
    }" > "$file_name"

    jupyter-notebook "$file_name"
}

new-notebook "$1"