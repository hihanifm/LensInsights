# LensInsights - External Insights Repository

This repository contains custom insights for the Lens analysis engine.

## Purpose

LensInsights is a separate repository for custom insights that can be used with the Lens engine. This separation allows:

- **Easy sharing** of insights across different projects
- **Independent version control** for insights vs. engine
- **Developer access control** - contribute insights without engine access
- **Modular deployment** - add/remove insight collections as needed

## Structure

You can organize insights in two ways:

### 1. Flat Structure (All insights in root)

```
LensInsights/
├── my_insight.py
├── another_insight.py
├── custom_analyzer.py
└── README.md
```

### 2. Nested Structure (Organized by category)

```
LensInsights/
├── android/
│   ├── crash_analyzer.py
│   ├── anr_detector.py
│   └── logcat_parser.py
├── web/
│   ├── error_tracker.py
│   └── performance_monitor.py
├── ios/
│   └── crash_reporter.py
└── README.md
```

Both structures are supported, and you can mix them based on your needs.

## Creating an Insight

Lens supports two types of insights:

### 1. Config-Based Insights (Recommended - Simpler)

Create a Python file with an `INSIGHT_CONFIG` dictionary:

```python
"""My Custom Insight - detects specific patterns in logs."""

INSIGHT_CONFIG = {
    "metadata": {
        "id": "my_custom_insight",
        "name": "My Custom Insight",
        "description": "Detects custom patterns in log files"
    },
    "filters": {
        "line_pattern": r"CUSTOM_PATTERN",
        # Optional: reading_mode defaults to "ripgrep" (fastest)
        # Optional: regex_flags defaults to case-insensitive
    }
}

def process_results(filter_result):
    """
    Process filtered lines and format output.
    
    Args:
        filter_result: FilterResult containing filtered lines
        
    Returns:
        dict with 'content' (formatted text) and optional 'metadata'
    """
    lines_by_file = filter_result.get_lines_by_file()
    total_matches = sum(len(lines) for lines in lines_by_file.values())
    
    result_text = f"Found {total_matches} matches\n"
    for file_path, lines in lines_by_file.items():
        result_text += f"\nFile: {file_path}\n"
        for line in lines[:10]:  # Show first 10
            result_text += f"  {line}\n"
    
    return {
        "content": result_text,
        "metadata": {"total_matches": total_matches}
    }

# Standalone execution support (optional but recommended)
if __name__ == "__main__":
    from app.utils.config_insight_runner import main_config_standalone
    main_config_standalone(__file__)
```

### 2. Class-Based Insights (Advanced - More Control)

Create a class that inherits from `Insight`:

```python
"""My Custom Insight - advanced implementation."""

from app.core.insight_base import Insight
from app.core.models import InsightResult

class MyCustomInsight(Insight):
    @property
    def id(self) -> str:
        return "my_custom_insight"
    
    @property
    def name(self) -> str:
        return "My Custom Insight"
    
    @property
    def description(self) -> str:
        return "Advanced custom analysis"
    
    async def analyze(self, file_paths, cancellation_event=None, progress_callback=None):
        # Your custom analysis logic here
        result_text = "Analysis results..."
        
        return InsightResult(
            result_type="text",
            content=result_text
        )
```

For detailed documentation, see: `backend/app/insights/README.md` in the Lens repository

## Adding to Lens

1. Open Lens application
2. Click the Settings icon (bottom-left corner)
3. Go to the "External Insights" tab
4. Click "Add" and enter the path to this directory (e.g., `/Users/yourname/LensInsights`)
5. Your insights will be loaded immediately

## Hot Reload

Lens automatically watches external insight directories for changes. When you:

- Add a new insight file
- Modify an existing insight
- Delete an insight

...the changes are detected and insights are reloaded automatically (within 2 seconds).

## Testing Your Insights

### Quick Test in Lens UI

1. Add this directory to Lens via Settings
2. Select your insight from the list
3. Enter a test file path
4. Click "Analyze Files"

### Standalone Testing (Recommended for Development)

Run your insight directly from the command line:

```bash
# From the Lens backend directory
cd /path/to/awebees/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run your insight
python -m app.insights.your_insight_name /path/to/test/file.log
```

Or use the test runner script:

```bash
# From the Lens root directory
./scripts/run_insight.py /path/to/LensInsights/your_insight.py /path/to/test/file.log
```

## Best Practices

1. **Use Config-Based Insights** for simple filtering tasks - they're faster to write and maintain
2. **Test Standalone** before adding to Lens - catch errors early
3. **Use Descriptive IDs** - make them unique and descriptive (e.g., `android_crash_detector` not `insight1`)
4. **Add Folders for Organization** - group related insights (e.g., `android/`, `web/`, `ios/`)
5. **Document Your Insights** - add docstrings explaining what they do and what they look for
6. **Handle Edge Cases** - test with empty files, binary files, and large files
7. **Use Ripgrep Mode** - it's 10-100x faster than Python regex for simple pattern matching

## Troubleshooting

### Insight Not Appearing in Lens

- Check that the path is correctly added in Settings > External Insights
- Ensure the Python file has either `INSIGHT_CONFIG` or an `Insight` subclass
- Look for errors in the backend logs (they're shown in the Lens UI error banner)

### Insight Throws Errors

- Test standalone first: `python your_insight.py /test/file.log`
- Check backend logs for detailed error messages
- Ensure all imports are correct (external insights need to import from `app.core.*`)

### Changes Not Detected

- The file watcher has a 2-second debounce - wait a moment
- Try using the "Refresh Insights" button in Settings > External Insights
- Restart the Lens backend if hot reload isn't working

## Contributing

Feel free to share your insights with others! Create a GitHub repository with your LensInsights collection and share the link.

## Learn More

- **Main Lens Repository**: [Link to Lens repo]
- **Insight Development Guide**: `backend/app/insights/README.md`
- **Example Insights**: `backend/app/insights/` in the Lens repository

---

Happy insight crafting! 🔍✨
