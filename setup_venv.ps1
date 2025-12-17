$ErrorActionPreference = "Stop"

$PythonPath =  "python"
$VenvDir = ".venv"

Write-Host "Creating virtual environment in '$VenvDir'..."

# Create venv
& $PythonPath -m venv $VenvDir

# Determine activation script
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    throw "Activation script not found: $activateScript"
}

# Use venv's Python directly (no activation needed for installs)
$venvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Venv python not found: $venvPython"
}

Write-Host "Upgrading pip in venv..."
& $venvPython -m pip install --upgrade pip

# Install requirements if present
$req = Join-Path $PWD "requirements.txt"
if (Test-Path $req) {
    Write-Host "Installing requirements from $req..."
    & $venvPython -m pip install -r $req
} else {
    Write-Host "No requirements.txt found. Skipping package install."
}

Write-Host "Venv ready. To activate later:"
Write-Host ". .\\.venv\\Scripts\\Activate.ps1"