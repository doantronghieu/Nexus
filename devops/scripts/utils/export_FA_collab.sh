#!/bin/bash

# Configuration
GIT_USERNAME="hieudt71"
GIT_PASSWORD="BDOlSEX539rGYaynav4fDwxnSofXOtqZlauK74dH52IiIGIkxVf3JQQJ99BAACAAAAAubb37AAASAZDOrVlW"
AZURE_ORG="azurefsoft062"
PROJECT_NAME="Embedded%20AI"
REPO_NAME="IvyEdge"
BRANCH_NAME="CDCxAIC"

# Construct URLs
BASE_URL="dev.azure.com/${AZURE_ORG}/${PROJECT_NAME}/_git/${REPO_NAME}"
SIMPLE_URL="https://${AZURE_ORG}@${BASE_URL}"
AUTH_URL="https://${GIT_USERNAME}:${GIT_PASSWORD}@${BASE_URL}"

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="${SCRIPT_DIR%/devops/scripts/utils}"

# Create and navigate to clone directory
CLONE_DIR="${ROOT_DIR}/clone"
mkdir -p "$CLONE_DIR"
cd "$CLONE_DIR" || exit 1

# Initialize git repository if it doesn't exist
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized in ${CLONE_DIR}"
    
    # Add remote origin
    git remote add origin "${SIMPLE_URL}"
    
    # Set URL with credentials
    git remote set-url origin "${AUTH_URL}"
    
    echo "Remote repository configured"
else
    echo "Git repository already exists in ${CLONE_DIR}"
    
    # Update remote URL
    git remote set-url origin "${AUTH_URL}"
    echo "Remote URL updated"
fi

# Create and switch to branch
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
    # Branch exists, just switch to it
    git checkout "${BRANCH_NAME}"
    echo "Switched to existing branch ${BRANCH_NAME}"
else
    # Create and switch to new branch
    git checkout -b "${BRANCH_NAME}"
    echo "Created and switched to new branch ${BRANCH_NAME}"
fi

# Verify current branch
git branch --show-current