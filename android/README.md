# Android Insights

Custom insights for analyzing Android logs, crash reports, and bug reports.

## Available Insights

### 1. Android Crash Analyzer (Advanced)
**File:** `android_crash_analyzer.py`

A comprehensive crash analyzer that detects `FATAL EXCEPTION` crashes and captures 10 lines of context after each crash for detailed analysis.

**Features:**
- ✅ Detects FATAL_EXCEPTION patterns
- ✅ Captures 10 lines of stack trace context
- ✅ Uses ripgrep for fast searching (with fallback)
- ✅ AI-powered crash analysis with custom prompts
- ✅ Auto-triggers AI after detection
- ✅ Provides root cause, severity, and fix recommendations

**Best for:** 
- Production crash investigations
- Detailed stack trace analysis
- When you need context around crashes

**Usage:**
```bash
# Test standalone
cd /path/to/awebees/backend
source venv/bin/activate
python /path/to/LensInsights/android/android_crash_analyzer.py /path/to/android.log
```

---

### 2. Android Crash Detector (Simple)
**File:** `simple_crash_detector.py`

A simpler, config-based crash detector that's easier to customize and understand.

**Features:**
- ✅ Config-based (easy to modify)
- ✅ Detects FATAL_EXCEPTION patterns
- ✅ Fast ripgrep-based searching
- ✅ AI-powered analysis with custom prompt
- ✅ Auto-triggers AI after detection

**Best for:**
- Quick crash detection
- Learning how config-based insights work
- Simple crash counts and summaries

**Usage:**
```bash
# Test standalone
cd /path/to/awebees/backend
source venv/bin/activate
python -m app.utils.config_insight_runner /path/to/LensInsights/android/simple_crash_detector.py /path/to/android.log
```

---

## Comparison

| Feature | Advanced | Simple |
|---------|----------|--------|
| Implementation | Class-based | Config-based |
| Context Lines | ✅ 10 lines after | ❌ Match line only |
| Stack Traces | ✅ Full | ❌ Partial |
| AI Analysis | ✅ Yes | ✅ Yes |
| Auto AI | ✅ Yes | ✅ Yes |
| Customization | Moderate | Easy |
| Performance | Fast | Fast |
| Code Complexity | Higher | Lower |

---

## Adding to Lens

1. Open Lens application
2. Click Settings (⚙️) in the bottom-left
3. Go to "External Insights" tab
4. Click "Add Directory"
5. Enter: `/Users/yourname/LensInsights`
6. Both insights will appear under "Android" folder

---

## Customizing the AI Prompts

Both insights use custom AI prompts. You can modify them to focus on specific aspects:

### For More Technical Analysis
```python
"prompt": """Analyze these Android crashes focusing on:
1. Exception types and their technical causes
2. Threading issues (main thread vs background)
3. Memory-related crashes
4. Null pointer exceptions and their origins
"""
```

### For Product/Business Focus
```python
"prompt": """Analyze these crashes from a product perspective:
1. User impact - which features are affected?
2. Frequency - which crashes happen most often?
3. Business priority - which should be fixed first?
4. Customer-facing messaging recommendations
"""
```

### For Security Analysis
```python
"prompt": """Analyze these crashes for security implications:
1. Are there any crashes exposing sensitive data?
2. Could any crash be exploited?
3. Are there authentication/permission issues?
4. Security-focused fix recommendations
"""
```

---

## Pattern Customization

To detect other Android issues, modify the `line_pattern`:

```python
# ANR (Application Not Responding) detection
"line_pattern": r"ANR\s+in"

# Native crashes
"line_pattern": r"(SIGSEGV|SIGABRT|signal \d+)"

# Out of Memory
"line_pattern": r"OutOfMemoryError"

# Multiple patterns (combine insights or use OR regex)
"line_pattern": r"(FATAL\s+EXCEPTION|ANR\s+in|OutOfMemoryError)"
```

---

## Testing Tips

1. **Use sample logs**: Test with `backend/samples/android-bugreport.txt` from Lens repo
2. **Check ripgrep**: Verify ripgrep is installed: `which rg`
3. **Enable debug logs**: Set `logging.basicConfig(level=logging.DEBUG)` in standalone mode
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
- Use case-insensitive search (enabled by default)

### AI not triggering
- Check Lens Settings > AI Configuration (API key must be set)
- Verify `"auto": True` in the `ai` config
- Check backend logs for AI errors

---

## Learn More

- **Main README**: `/path/to/LensInsights/README.md`
- **Insight Development Guide**: `/path/to/awebees/backend/app/insights/README.md`
- **AI Setup Guide**: `/path/to/awebees/docs/AI_SETUP.md`

---

Happy crash hunting! 🐛🔍

