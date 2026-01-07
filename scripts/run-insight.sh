#!/bin/bash

# Convenience script to run LensInsights using the Lens (awebees) backend
# Usage: ./run-insight.sh <insight_py_file> <log_file> [log_file2 ...]
#
# Examples:
#   ./run-insight.sh android/simple_crash_detector.py /path/to/crash.log
#   ./run-insight.sh android/simple_crash_detector.py ~/logs/*.log

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find the Lens (awebees) project - assume it's in a sibling directory to LensInsights
LENS_DIR=""
if [ -d "$SCRIPT_DIR/../../awebees/backend" ]; then
  LENS_DIR="$(cd "$SCRIPT_DIR/../../awebees" && pwd)"
elif [ -d "$SCRIPT_DIR/../../Lens/backend" ]; then
  LENS_DIR="$(cd "$SCRIPT_DIR/../../Lens" && pwd)"
else
  echo "Error: Could not find Lens (awebees) project"
  echo "Expected to find it at: $SCRIPT_DIR/../../awebees or $SCRIPT_DIR/../../Lens"
  exit 1
fi

echo "✓ Found Lens project at: $LENS_DIR"

# Check if venv exists
if [ ! -d "$LENS_DIR/backend/venv" ]; then
  echo "Error: Virtual environment not found at $LENS_DIR/backend/venv"
  echo "Please run setup.sh in the Lens project first"
  exit 1
fi

# Check arguments
if [ $# -lt 2 ]; then
  echo "Usage: $0 <insight_py_file> <log_file> [log_file2 ...]"
  echo ""
  echo "Available insights:"
  echo "  - android/simple_crash_detector.py  - Detects Android FATAL_EXCEPTION crashes"
  echo ""
  echo "Examples:"
  echo "  $0 android/simple_crash_detector.py /path/to/crash.log"
  echo "  $0 android/simple_crash_detector.py ~/logs/*.log"
  exit 1
fi

INSIGHT_FILE="$1"
shift

# Convert relative path to absolute if needed (relative to LensInsights root, not scripts folder)
if [[ "$INSIGHT_FILE" != /* ]]; then
  INSIGHT_FILE="$SCRIPT_DIR/../$INSIGHT_FILE"
fi

# Check if insight file exists
if [ ! -f "$INSIGHT_FILE" ]; then
  echo "Error: Insight file not found: $INSIGHT_FILE"
  exit 1
fi

echo "✓ Using insight: $(basename "$INSIGHT_FILE")"
echo "✓ Analyzing $# file(s)"
echo ""

# Activate venv and run the insight
cd "$LENS_DIR/backend"
source venv/bin/activate

python -m app.utils.config_insight_runner "$INSIGHT_FILE" "$@"

