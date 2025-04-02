#!/bin/bash

# Usage: ./add-devcontainer.sh --type python|node|docker|bash|terraform|docs|azure|kubernetes

set -e

REPO_NAME=$(basename "$PWD")
PROJECT_TYPE=${1#--type=}
DEV_FOLDER=".devcontainer"

if [ -z "$PROJECT_TYPE" ]; then
  PROJECT_TYPE="python"
fi

echo "Setting up dev container for project: $REPO_NAME (type: $PROJECT_TYPE)"
mkdir -p "$DEV_FOLDER"

cat > "$DEV_FOLDER/devcontainer.json" <<EOF
{
  "name": "$REPO_NAME",
EOF

case "$PROJECT_TYPE" in
  python)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "apt update && apt install -y neovim && pip install -r requirements.txt || true",
EOF
    [ ! -f requirements.txt ] && echo "Pillow" > requirements.txt
    ;;
  node)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "postCreateCommand": "apt update && apt install -y neovim && npm install || true",
EOF
    ;;
  docker)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:1": {}
  },
EOF
    ;;
  bash)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y neovim",
EOF
    ;;
  terraform)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "hashicorp/terraform:latest",
  "postCreateCommand": "apt update && apt install -y vim curl git",
EOF
    ;;
  docs)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y neovim markdownlint",
EOF
    ;;
  azure)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y curl gnupg powershell neovim && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    pwsh -Command 'Install-Module -Name Az -Force -AllowClobber' && \
    az bicep install || true",
EOF
    ;;
  kubernetes)
    cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y curl neovim apt-transport-https gnupg && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo 'deb https://apt.kubernetes.io/ kubernetes-xenial main' > /etc/apt/sources.list.d/kubernetes.list && \
    apt update && apt install -y kubectl helm || true",
EOF
    ;;
  *)
    echo "Unknown project type: $PROJECT_TYPE"
    exit 1
    ;;
esac

cat >> "$DEV_FOLDER/devcontainer.json" <<EOF
  "customizations": {
    "vscode": {
      "extensions": [
        "asvetliakov.vscode-neovim",
        "esbenp.prettier-vscode",
        "streetsidesoftware.code-spell-checker",
        "redhat.vscode-yaml",
        "ms-kubernetes-tools.vscode-kubernetes-tools"
      ]
    }
  },
  "mounts": [
    "source=\${localWorkspaceFolder}/fonts,target=/workspace/fonts,type=bind"
  ]
}
EOF

echo "Dev container setup completed in $PWD/$DEV_FOLDER"
