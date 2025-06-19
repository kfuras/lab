param(
    [Parameter(Mandatory)]
    [string]$Name
)

$vaultName = "bpsharedkv"

try {
    $username = az keyvault secret show --vault-name $vaultName --name "$Name-Username" --query value -o tsv
    $password = az keyvault secret show --vault-name $vaultName --name "$Name-Password" --query value -o tsv
} catch {
    Write-Error "❌ Failed to retrieve secrets using Azure CLI"
    exit 1
}

Write-Host "🔐 Username: $username"
Write-Host "🔐 Password: ********"

# Copy password to clipboard
if ($IsMacOS) {
    $password | pbcopy
    Write-Host "📋 Password copied to clipboard (macOS)"
}
elseif ($IsWindows) {
    Set-Clipboard -Value $password
    Write-Host "📋 Password copied to clipboard (Windows)"
}
else {
    Write-Host "⚠️ Clipboard copy not supported on this OS."
}