# Set the environment name and desired Python version
$envName = "my_env"
$pythonVersion = "3.8"

# Install Anaconda if it is not already installed
if (!(Test-Path "$env:USERPROFILE\anaconda3")) {
    Write-Host "Anaconda not found, installing..."
    # Modify this line to use the appropriate Anaconda installer for your system
    Invoke-WebRequest https://repo.anaconda.com/archive/Anaconda3-2021.05-Windows-x86_64.exe -OutFile "$env:USERPROFILE\Downloads\Anaconda3-2021.05-Windows-x86_64.exe"
    Start-Process -FilePath "$env:USERPROFILE\Downloads\Anaconda3-2021.05-Windows-x86_64.exe" -ArgumentList "/S /D=$env:USERPROFILE\anaconda3" -Wait
    $env:PATH = "$env:USERPROFILE\anaconda3\Scripts;$env:USERPROFILE\anaconda3\Library\bin;$env:PATH"
}

# Create the new environment
conda create --name $envName python=$pythonVersion

# Activate the environment
conda activate $envName

# Install required packages
conda install package1 package2 ...

# Deactivate the environment
conda deactivate

Write-Host "Done!"
