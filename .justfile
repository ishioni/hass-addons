#!/usr/bin/env -S just --justfile


set lazy
set quiet
set script-interpreter := ['bash', '-euo', 'pipefail']
set shell := ['bash', '-euo', 'pipefail', '-c']

root_dir := justfile_directory()

[private]
[script]
default:
    just -l

[private]
[script]
log lvl msg *args:
    gum log -t rfc3339 -s -l "{{ lvl }}" "{{ msg }}" {{ args }}

# Format all files
format-all: format-markdown format-yaml

# Format Markdown files
format-markdown:
    -prettier \
        --config '{{ root_dir }}/.ci/prettier/.prettierrc.yaml' \
        --list-different \
        --ignore-unknown \
        --parser=markdown \
        --write '*.md' \
        '{{ root_dir }}/**/*.md'

# Format YAML files
format-yaml:
    -prettier \
        --config '{{ root_dir }}/.ci/prettier/.prettierrc.yaml' \
        --list-different \
        --ignore-unknown \
        --parser=yaml \
        --write '*.y*ml' \
        '{{ root_dir }}/**/*.y*ml'

# Initialize pre-commit hooks
precommit-init:
    pre-commit install --install-hooks

# Run pre-commit on all files
precommit-run:
    pre-commit run --all-files

# Lint code by running pre-commit on all files
check-lint:
    just precommit-run

# Run all checks
check: check-lint

# Build docker image for linux/arm64 in the current working directory
build-docker-arm64:
    pwd && docker buildx build --platform 'linux/arm64' -t test:localdev-arm64 .

# Build docker image for linux/amd64 in the current working directory
build-docker-amd64:
    docker buildx build --platform 'linux/amd64' -t test:localdev-amd64 .

# Build docker images for all supported architectures
build: build-docker-arm64 build-docker-amd64
    pwd

# Validate Renovate config locally
validate-renovate:
    npx --yes --package renovate -- renovate-config-validator .renovaterc.json5

# Update pre-commit hooks
precommit-update:
    pre-commit autoupdate
