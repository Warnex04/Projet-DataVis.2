#!/bin/bash

# Set the environment name and desired Python version
ENV_NAME="my_env"
PYTHON_VERSION="3.8"

# Check if Anaconda is already installed
if ! command -v conda > /dev/null; then
    echo "Anaconda not found, installing..."
    # Modify this line to use the appropriate Anaconda installer for your system
    wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
    bash /tmp/Anaconda3-2021.05-Linux-x86_64.sh -b -p $HOME/anaconda3
    echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> $HOME/.bashrc
    source $HOME/.bashrc
else
    echo "Anaconda is already installed"
fi

export PATH="$HOME/anaconda3/bin:$PATH"


# Create the new environment
conda create --name $ENV_NAME python=$PYTHON_VERSION

# Activate the environment
conda activate $ENV_NAME

# Install required packages
conda install -y pandas

# Deactivate the environment
conda deactivate

echo "Done!"
