"""Simple Android Crash Detector - Config-based insight with AI analysis.

This is a simpler, config-based version of the crash detector that demonstrates
how to use INSIGHT_CONFIG with AI integration.
"""

INSIGHT_CONFIG = {
    "metadata": {
        "id": "android_simple_crash",
        "name": "Android Crash Detector (Simple)",
        "description": "Detects FATAL_EXCEPTION in Android logs with AI analysis",
        "folder": "android"
    },
    "filters": {
        "line_pattern": r"FATAL\s+EXCEPTION",
        "reading_mode": "ripgrep"  # Fast pattern matching
    },
    "ai": {
        "enabled": True,
        "auto": True,  # Automatically trigger AI after detection
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


def process_results(filter_result):
    """
    Format the filtered crash lines into a readable report.
    
    Args:
        filter_result: FilterResult with matched lines
        
    Returns:
        dict with 'content' and 'metadata' keys
    """
    lines_by_file = filter_result.get_lines_by_file()
    total_crashes = filter_result.get_total_line_count()
    
    # Format output
    content = "Android Crash Detection (Simple)\n"
    content += "=" * 80 + "\n\n"
    content += f"Total FATAL_EXCEPTION lines found: {total_crashes}\n"
    content += f"Files analyzed: {filter_result.get_file_count()}\n\n"
    
    if total_crashes == 0:
        content += "No crashes found.\n"
        return {
            "content": content,
            "metadata": {"total_crashes": 0}
        }
    
    # Show crashes per file
    for file_path, lines in lines_by_file.items():
        import os
        content += "=" * 80 + "\n"
        content += f"File: {os.path.basename(file_path)}\n"
        content += f"Path: {file_path}\n"
        content += f"Crashes: {len(lines)}\n"
        content += "=" * 80 + "\n\n"
        
        # Show first 50 crash lines to avoid overwhelming the AI
        for i, line in enumerate(lines[:50], 1):
            content += f"{i}. {line.strip()}\n"
        
        if len(lines) > 50:
            content += f"\n... and {len(lines) - 50} more crash lines\n"
        
        content += "\n"
    
    return {
        "content": content,
        "metadata": {
            "total_crashes": total_crashes,
            "files_analyzed": filter_result.get_file_count()
        }
    }


# Standalone execution support
if __name__ == "__main__":
    from app.utils.config_insight_runner import main_config_standalone
    main_config_standalone(__file__)

