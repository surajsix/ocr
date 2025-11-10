# Create necessary directories
$directories = @(
    "src",
    "src/static",
    "src/templates",
    "src/services",
    "src/utils",
    "src/translations",
    "src/uploads",
    "tests"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "Created directory: $dir"
    }
}

# Move Python files to appropriate locations
$fileMappings = @{
    "backend/app.py" = "src/app.py"
    "backend/config.py" = "src/config.py"
    "backend/services/" = "src/services/"
    "backend/utils/" = "src/utils/"
    "backend/requirements.txt" = "requirements.txt"
    "backend/NotoSans-Regular.ttf" = "src/static/NotoSans-Regular.ttf"
    "backend/test_ocr.py" = "tests/test_ocr.py"
    "backend/test_ocr_direct.py" = "tests/test_ocr_direct.py"
    "backend/test_ocr_improved.py" = "tests/test_ocr_improved.py"
    "backend/test_translation.py" = "tests/test_translation.py"
}

foreach ($src in $fileMappings.Keys) {
    $dest = $fileMappings[$src]
    if (Test-Path $src) {
        if ($src.EndsWith("/")) {
            # Copy directory
            Copy-Item -Path "$src*" -Destination $dest -Recurse -Force
        } else {
            # Copy file
            Copy-Item -Path $src -Destination $dest -Force
        }
        Write-Host "Moved $src to $dest"
    }
}

# Move test files to tests directory
$testFiles = @(
    "backend/test_flask.py",
    "backend/minimal_test.py",
    "backend/create_test_image.py"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        $dest = Join-Path "tests" (Split-Path $file -Leaf)
        Move-Item -Path $file -Destination $dest -Force
        Write-Host "Moved test file: $file to $dest"
    }
}

# Move test data
if (Test-Path "backend/test.txt") {
    Move-Item -Path "backend/test.txt" -Destination "tests/test_data/test.txt" -Force
    New-Item -ItemType Directory -Path "tests/test_data" -Force | Out-Null
    Write-Host "Moved test data to tests/test_data/"
}

# Clean up old directories
$directoriesToRemove = @(
    "backend/__pycache__",
    "backend/translations",
    "backend/uploads"
)

foreach ($dir in $directoriesToRemove) {
    if (Test-Path $dir) {
        Remove-Item -Path $dir -Recurse -Force
        Write-Host "Removed directory: $dir"
    }
}

# Create a new README.md if it doesn't exist
if (-not (Test-Path "README.md")) {
    @"
# OCR Translator

A web application for OCR and translation of documents.

## Project Structure

- `src/` - Main application source code
  - `static/` - Static files (CSS, JS, fonts)
  - `templates/` - HTML templates
  - `uploads/` - Temporary file uploads
  - `translations/` - Translated output files
  - `services/` - Service modules
  - `utils/` - Utility functions
- `tests/` - Test files
  - `test_data/` - Test data files
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/app.py
   ```

4. Open http://localhost:5000 in your browser.
"@ | Out-File -FilePath "README.md" -Encoding utf8
    Write-Host "Created README.md"
}

Write-Host ""
Write-Host "Reorganization complete!" -ForegroundColor Green
Write-Host "New project structure:"
Get-ChildItem -Path . -Recurse | Where-Object { $_.PSIsContainer } | Select-Object FullName | Format-Table -HideTableHeaders

# Instructions for the user
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the new project structure"
Write-Host "2. Update any file paths in your code if needed"
Write-Host "3. Test the application with: python src/app.py"
Write-Host "4. Check the README.md for setup instructions"
