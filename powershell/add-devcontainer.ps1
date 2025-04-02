param (
    [string]$Type = "python"
)

$projectName = Split-Path -Leaf (Get-Location)
$devFolder = ".devcontainer"
$devFile = "$devFolder\devcontainer.json"

Write-Host "📦 Setting up dev container for project: $projectName (type: $Type)"
New-Item -ItemType Directory -Force -Path $devFolder | Out-Null

$content = @"
{
  "name": "$projectName",
"@

switch ($Type) {
  "python" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "apt update && apt install -y neovim && pip install -r requirements.txt || true",
"@
    if (-not (Test-Path "requirements.txt")) {
      "Pillow" | Out-File -Encoding utf8 -FilePath "requirements.txt"
    }
  }
  "node" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "postCreateCommand": "apt update && apt install -y neovim && npm install || true",
"@
  }
  "docker" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:1": {}
  },
"@
  }
  "bash" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y neovim",
"@
  }
  "terraform" {
    $content += @"
  "image": "hashicorp/terraform:latest",
  "postCreateCommand": "apt update && apt install -y vim curl git",
"@
  }
  "docs" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y neovim markdownlint",
"@
  }
  "azure" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y curl gnupg powershell neovim && curl -sL https://aka.ms/InstallAzureCLIDeb | bash && pwsh -Command 'Install-Module -Name Az -Force -AllowClobber' && az bicep install || true",
"@
  }
  "kubernetes" {
    $content += @"
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "postCreateCommand": "apt update && apt install -y curl neovim apt-transport-https gnupg && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && echo 'deb https://apt.kubernetes.io/ kubernetes-xenial main' > /etc/apt/sources.list.d/kubernetes.list && apt update && apt install -y kubectl helm || true",
"@
  }
  default {
    Write-Host "❌ Unknown project type: $Type"
    exit 1
  }
}

$content += @"
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
"@

Set-Content -Path $devFile -Value $content -Encoding UTF8
Write-Host "✅ Dev container setup completed in $PWD\$devFolder"

