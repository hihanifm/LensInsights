"""Android Crash Detector - Detects FATAL_EXCEPTION in Android logs with AI analysis."""

INSIGHT_CONFIG = {
    "metadata": {
        "id": "android_crash",
        "name": "Android Crash Detector",
        "description": "Detects FATAL_EXCEPTION in Android logs with AI analysis",
        "folder": "android"
    },
    "filters": {
        "line_pattern": r"FATAL\s+EXCEPTION",
        "reading_mode": "ripgrep"
    },
    "ai": {
        "enabled": True,
        "auto": True,
        "prompt_type": "custom",
        "prompt": """You are an expert Android developer analyzing crash logs.

Analyze the following FATAL EXCEPTION errors and provide:

1. **Summary**: Brief overview of the crashes found
2. **Common Patterns**: Are there recurring issues?
3. **Top Causes**: What are the main causes of these crashes?
4. **Recommended Fixes**: Actionable steps to fix the most critical issues
5. **Priority**: Which crashes should be fixed first?

Be concise and focus on actionable insights.

{result_content}"""
    }
}

# Standalone execution support
if __name__ == "__main__":
    from app.utils.config_insight_runner import main_config_standalone
    main_config_standalone(__file__)


