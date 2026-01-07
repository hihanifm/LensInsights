# Quick Start Guide

Welcome to LensInsights! This repository contains custom insights for the Lens analysis engine.

## 🚀 Getting Started (2 minutes)

### 1. Add to Lens

1. Open your Lens application
2. Click the **Settings** icon (⚙️) in the bottom-left corner
3. Go to the **"External Insights"** tab
4. Click **"Add Directory"**
5. Enter the path to this directory: `/Users/yourname/LensInsights`
6. Click **"Save"**

Your insights will be loaded immediately! 🎉

### 2. Use the Insights

After adding the directory:

1. Select an insight from the list (e.g., "Android Crash Analyzer")
2. Click **"Browse"** to select a log file
3. Click **"Analyze Files"**
4. Wait for results
5. Click **"Analyze with AI"** for AI-powered insights (or it will auto-trigger)

## 📱 Android Crash Analysis

A simple, config-based insight for Android crash detection:

### Android Crash Detector
**Best for:** Easy crash detection with AI-powered analysis

```
✅ Config-based (easy to customize)
✅ Fast ripgrep pattern matching
✅ AI auto-triggers with detailed analysis
✅ Provides root cause and fix recommendations
✅ Simple to modify for your needs
```

## 🧪 Test It Out

### Option 1: Using Lens UI (Recommended)
1. Add this directory to Lens (see above)
2. Select "Android Crash Detector" from the insight list
3. Browse to a log file (e.g., `backend/samples/android-bugreport.txt` in Lens repo)
4. Click "Analyze Files"
5. View results and AI analysis

### Option 2: Standalone Testing
```bash
# Navigate to Lens backend
cd /path/to/awebees/backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the crash detector
python -m app.utils.config_insight_runner /path/to/LensInsights/android/simple_crash_detector.py /path/to/android.log
```

## 🤖 AI Configuration

To use AI features, configure your AI settings in Lens:

1. Click **Settings** (⚙️)
2. Go to **"AI Configuration"** tab
3. Enter your OpenAI API key (or configure local LLM)
4. Save settings

See the [AI Setup Guide](../awebees/docs/AI_SETUP.md) in the Lens repo for detailed instructions.

## 📂 Directory Structure

```
LensInsights/
├── README.md                      # Full documentation
├── QUICK_START.md                # This file
├── .gitignore                    # Git ignore rules
└── android/                      # Android-specific insights
    ├── README.md                 # Android insights documentation
    └── simple_crash_detector.py  # Crash detector (config-based)
```

## 🎯 What's Next?

1. **Try the crash detector** on your Android logs
2. **Customize the AI prompts** to focus on what matters to you
3. **Create more insights** - see [README.md](README.md) for guide
4. **Add more folders** - organize insights by category (ios/, web/, etc.)

## 📚 Documentation

- **Main Documentation**: [README.md](README.md)
- **Android Insights**: [android/README.md](android/README.md)
- **Lens Insight Development**: `/path/to/awebees/backend/app/insights/README.md`
- **AI Setup**: `/path/to/awebees/docs/AI_SETUP.md`

## 🛠️ Customization Examples

### Detect ANR (Application Not Responding)
Create a new file `android/anr_detector.py`:
```python
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
        "enabled": True,
        "auto": True,
        "prompt_type": "explain"
    }
}

if __name__ == "__main__":
    from app.utils.config_insight_runner import main_config_standalone
    main_config_standalone(__file__)
```

### Detect Out of Memory Errors
```python
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
        "enabled": True,
        "prompt_type": "recommend"
    }
}
```

## 💡 Tips

1. **Use ripgrep** for 10-100x faster analysis: `brew install ripgrep` (macOS)
2. **Hot reload**: Changes to insights are detected automatically (2-second delay)
3. **Test standalone first**: Catch errors before loading into Lens UI
4. **Start with config-based**: Easier to learn and customize
5. **Use folders**: Organize insights by platform (android/, ios/, web/)

## ❓ Troubleshooting

### Insights not showing up
- Verify the path in Settings > External Insights
- Check backend logs for errors
- Ensure Python files have `INSIGHT_CONFIG` or inherit from `Insight`

### AI not working
- Check Settings > AI Configuration (API key must be set)
- Verify `"enabled": True` in the insight's AI config
- Check backend logs for API errors

### Ripgrep warnings
- Install ripgrep for best performance: `brew install ripgrep`
- Insights will fall back to slower methods automatically

---

**Need help?** Check the main [README.md](README.md) or the [Android README](android/README.md) for more details.

Happy analyzing! 🔍✨


