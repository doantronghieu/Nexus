#!/bin/bash

# Directories to clean
TARGET_DIRS=(
  "$(pwd)/apps/services/dev/stream/frames"
  "$(pwd)/apps/services/dev/stream/processed_frames"
)

# Function to clean a directory
clean_directory() {
  local dir=$1

  # Check if directory exists
  if [ ! -d "$dir" ]; then
    echo "Error: Directory $dir does not exist"
    return 1
  fi

  # Debug: Show files and folders before deletion
  echo "Files and folders to be deleted in $dir:"
  find "$dir" -mindepth 1 -print
  echo "Total items found: $(find "$dir" -mindepth 1 | wc -l)"

  # Delete all files and folders inside the target directory
  if find "$dir" -mindepth 1 -delete; then
    echo "All files and folders in $dir have been deleted"
    # Verify deletion
    echo "Verifying deletion:"
    find "$dir" -mindepth 1 -print
    echo "Remaining items: $(find "$dir" -mindepth 1 | wc -l)"
  else
    echo "Error: Some items could not be deleted in $dir. Possible reasons:"
    echo "1. Insufficient permissions"
    echo "2. Files are in use"
    echo "3. Files are read-only"

    # Check for problematic files
    echo "Checking for problematic items in $dir:"
    find "$dir" -mindepth 1 ! -writable -print
    return 1
  fi
}

# Clean each directory
for dir in "${TARGET_DIRS[@]}"; do
  clean_directory "$dir"
done