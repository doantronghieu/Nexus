#!/bin/bash

# Get the root directory
ROOT_DIR=$(pwd)

# Function to rename a file and log the operation
rename_imports_file() {
    local source_file="$1"
    local target_file="${source_file/imports.py/packages.py}"
    
    echo "Processing:"
    echo "  From: $source_file"
    echo "  To:   $target_file"
    
    if [ -f "$target_file" ]; then
        echo "  Warning: Target file already exists, skipping: $target_file"
        return 1
    fi
    
    if mv "$source_file" "$target_file"; then
        echo "  Success: File renamed"
        return 0
    else
        echo "  Error: Failed to rename file"
        return 1
    fi
}

# Counter for statistics
total_files=0
successful_renames=0
failed_renames=0

echo "Starting rename operation..."

# Find and process all imports.py files
while IFS= read -r file; do
    ((total_files++))
    if rename_imports_file "$file"; then
        ((successful_renames++))
    else
        ((failed_renames++))
    fi
    echo "----------------------------------------"
done < <(find "$ROOT_DIR/apps" -name "imports.py" -type f)

# Print summary
echo "Rename operation completed:"
echo "  Total files found: $total_files"
echo "  Successfully renamed: $successful_renames"
echo "  Failed to rename: $failed_renames"

# Exit with error if any renames failed
[ "$failed_renames" -eq 0 ] || exit 1