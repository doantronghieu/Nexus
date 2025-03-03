#!/bin/bash

# Script to clean Final Cut Pro backups
# WARNING: This will delete files! Use with caution.

# Define the path to Final Cut Backups folder
BACKUPS_DIR="/Users/thung/Movies/Final Cut Backups.localized"

# Check if the directory exists
if [ ! -d "$BACKUPS_DIR" ]; then
    echo "Error: Final Cut Backups folder not found at $BACKUPS_DIR"
    echo "Please update the BACKUPS_DIR variable in the script."
    exit 1
fi

# Print current disk usage
echo "Current disk usage of Final Cut Backups folder:"
du -sh "$BACKUPS_DIR"

# Ask for confirmation
echo ""
echo "This script will delete backup files in: $BACKUPS_DIR"
echo "Are you sure you want to continue? (y/n)"
read -r confirmation

if [ "$confirmation" != "y" ] && [ "$confirmation" != "Y" ]; then
    echo "Operation cancelled."
    exit 0
fi

# Option to keep recent backups
echo ""
echo "Do you want to keep the most recent backups? (y/n)"
read -r keep_recent

if [ "$keep_recent" = "y" ] || [ "$keep_recent" = "Y" ]; then
    echo "How many days of recent backups do you want to keep? (e.g., 7)"
    read -r days_to_keep
    
    if [[ ! "$days_to_keep" =~ ^[0-9]+$ ]]; then
        echo "Invalid input. Please enter a number."
        exit 1
    fi
    
    echo "Removing backup files older than $days_to_keep days..."
    find "$BACKUPS_DIR" -type f -mtime +$days_to_keep -delete
    find "$BACKUPS_DIR" -type d -empty -delete
else
    echo "Removing all backup files..."
    rm -rf "$BACKUPS_DIR"/*
fi

# Print new disk usage
echo ""
echo "Cleanup completed!"
echo "New disk usage of Final Cut Backups folder:"
du -sh "$BACKUPS_DIR"