# Sample Files

This directory contains sample log files that can be used with Lens insights for testing and demonstration purposes.

## Adding Sample Files

Place your sample files in this directory. Supported formats:

- **Plain text files**: `.txt`, `.log` - Used directly
- **Compressed files**: `.zip`, `.gz` - Automatically extracted on first use

## Sample Metadata (Optional)

You can provide metadata for your samples by creating a JSON file with the same name as your sample file (without extension).

Example: For `my-sample.txt`, create `my-sample.json`:

```json
{
  "name": "My Sample Log",
  "description": "A sample log file for testing error detection",
  "size_mb": 5.2,
  "recommended_insights": ["error_detector", "line_count"]
}
```

If no metadata file is provided, Lens will infer the name and description from the filename.

## Auto-Extraction

Compressed files (`.zip` and `.gz`) are automatically extracted when Lens discovers them. The extracted files are created in the same directory and can be safely ignored in version control (add to `.gitignore` if needed).

## Example Structure

```
samples/
├── android-bugreport.zip      # Compressed sample (auto-extracted)
├── android-bugreport.txt       # Extracted file (gitignored)
├── android-bugreport.json      # Optional metadata
├── web-server-logs.log         # Plain text sample
└── ios-crash-reports.zip       # Another compressed sample
```

## Notes

- Large files (>50MB uncompressed) should be stored compressed to save repository space
- Extracted files are automatically created and can be gitignored
- Sample files are discovered automatically when Lens starts up
- Samples from all configured insight paths are available in the Lens UI
