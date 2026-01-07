# Android Insights

Custom insights for analyzing Android logs, crash reports, and bug reports.

## Available Insight

### Android Crash Detector
**File:** `simple_crash_detector.py`

A config-based crash detector that detects `FATAL EXCEPTION` crashes with AI-powered analysis.

**Features:**
- ✅ Config-based (easy to modify)
- ✅ Detects FATAL_EXCEPTION patterns
- ✅ Fast ripgrep-based searching
- ✅ AI-powered analysis with custom prompt
- ✅ Auto-triggers AI after detection
- ✅ Simple and easy to customize

**Best for:**
- Quick crash detection and analysis
- Learning how config-based insights work
- Easy customization for specific needs

**Usage:**
```bash
# Test standalone
cd /path/to/awebees/backend
source venv/bin/activate
python -m app.utils.config_insight_runner /path/to/LensInsights/android/simple_crash_detector.py /path/to/android.log
```

---

## Adding to Lens

1. Open Lens application
2. Click Settings (⚙️) in the bottom-left
3. Go to "External Insights" tab
4. Click "Add Directory"
5. Enter: `/Users/yourname/LensInsights`
6. The insight will appear under "Android" folder

---

## Customizing the AI Prompt

The insight uses a custom AI prompt. You can modify it in `simple_crash_detector.py` to focus on specific aspects:

### For More Technical Analysis
```python
"prompt": """Analyze these Android crashes focusing on:
1. Exception types and their technical causes
2. Threading issues (main thread vs background)
3. Memory-related crashes
4. Null pointer exceptions and their origins

{result_content}"""
```

### For Product/Business Focus
```python
"prompt": """Analyze these crashes from a product perspective:
1. User impact - which features are affected?
2. Frequency - which crashes happen most often?
3. Business priority - which should be fixed first?
4. Customer-facing messaging recommendations

{result_content}"""
```

### For Security Analysis
```python
"prompt": """Analyze these crashes for security implications:
1. Are there any crashes exposing sensitive data?
2. Could any crash be exploited?
3. Are there authentication/permission issues?
4. Security-focused fix recommendations

{result_content}"""
```

---

## Pattern Customization

To detect other Android issues, modify the `line_pattern` in `simple_crash_detector.py`:

```python
# ANR (Application Not Responding) detection
"line_pattern": r"ANR\s+in"

# Native crashes
"line_pattern": r"(SIGSEGV|SIGABRT|signal \d+)"

# Out of Memory
"line_pattern": r"OutOfMemoryError"

# Multiple patterns (use OR regex)
"line_pattern": r"(FATAL\s+EXCEPTION|ANR\s+in|OutOfMemoryError)"
```

---

## Creating More Insights

You can easily create more insights by copying and modifying `simple_crash_detector.py`:

### Example: ANR Detector
```python
"""Android ANR (Application Not Responding) Detector."""

INSIGHT_CONFIG = {
    "metadata": {
        "id": "android_anr",
        "name": "ANR Detector",
        "description": "Detects Application Not Responding issues"
    },
    "filters": {
        "line_pattern": r"ANR\s+in"
    },
    "ai": {
        "auto": True,
        "prompt_type": "custom",
        "prompt": """Analyze these ANR (Application Not Responding) issues:
1. Which operations are blocking the main thread?
2. How long are the ANRs lasting?
3. What are the immediate fixes needed?

{result_content}"""
    }
}
```

### Example: Out of Memory Detector
```python
"""Android Out of Memory Detector."""

INSIGHT_CONFIG = {
    "metadata": {
        "id": "android_oom",
        "name": "Out of Memory Detector",
        "description": "Detects OutOfMemoryError issues"
    },
    "filters": {
        "line_pattern": r"OutOfMemoryError"
    },
    "ai": {
        "auto": True,
        "prompt_type": "recommend"
    }
}
```

---

## Testing Tips

1. **Use sample logs**: Test with `backend/samples/android-bugreport.txt` from Lens repo
2. **Check ripgrep**: Verify ripgrep is installed: `which rg`
3. **Enable debug logs**: Check Lens backend logs for detailed output
4. **AI testing**: Make sure AI is configured in Lens Settings > AI Configuration

---

## Troubleshooting

### "Ripgrep not available" warning
Install ripgrep for 10-100x faster performance:
```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows
choco install ripgrep
```

### "No crashes found" but you know there are crashes
- Check the log file encoding (should be UTF-8 or ASCII)
- Try the pattern in a text editor to verify it matches
- Pattern matching is case-insensitive by default

### AI not triggering
- Check Lens Settings > AI Configuration (API key must be set)
- Verify `"auto": True` in the `ai` config
- Check backend logs for AI errors

### Changes not detected
- Lens auto-reloads insights (2-second debounce)
- Save your file and wait a moment
- Check Settings > External Insights to refresh manually

---

## Learn More

- **Main README**: `/path/to/LensInsights/README.md`
- **Insight Development Guide**: `/path/to/awebees/backend/app/insights/README.md`
- **AI Setup Guide**: `/path/to/awebees/docs/AI_SETUP.md`

---

Happy crash hunting! 🐛🔍
