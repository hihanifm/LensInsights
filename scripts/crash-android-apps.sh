#!/bin/bash
# crash_android_apps_launch.sh - Launch apps then crash them

echo "======================================"
echo "Android App Crash Generator"
echo "Launch -> Crash"
echo "======================================"
echo ""

# Check if device is connected
device_count=$(adb devices | grep -w "device" | wc -l)
if [ "$device_count" -eq 0 ]; then
    echo "ERROR: No Android device connected via ADB"
    adb devices
    exit 1
fi

echo "Device connected! Starting launch + crash sequence..."
echo ""

# List of common Android apps to crash
apps=(
    "com.android.chrome"
    "com.google.android.gm"
    "com.android.contacts"
    "com.android.calculator2"
    "com.android.calendar"
    "com.android.messaging"
    "com.android.settings"
    "com.google.android.apps.maps"
)

crashed_count=0

for app in "${apps[@]}"; do
    echo "Processing: $app"
    
    # Launch the app first using monkey
    echo "  → Launching app..."
    adb shell monkey -p "$app" -c android.intent.category.LAUNCHER 1 2>/dev/null
    sleep 2
    
    # Now crash it
    echo "  → Crashing app..."
    if adb shell am crash "$app" 2>/dev/null; then
        echo "  ✓ Crashed successfully"
        ((crashed_count++))
    else
        echo "  ✗ Crash command failed (may not be supported on this device)"
    fi
    
    sleep 1
    echo ""
done

echo "======================================"
echo "Launch + Crash sequence complete!"
echo "Successfully crashed: $crashed_count apps"
echo "======================================"
echo ""
echo "Checking for FATAL logs in logcat..."
adb logcat -d | grep -i "FATAL" | tail -20

echo ""
echo "Now capturing bug report..."
echo "(This may take 30-60 seconds...)"
echo ""

timestamp=$(date +%Y%m%d-%H%M%S)
bugreport_file="bugreport-crashes-${timestamp}.zip"

adb bugreport "$bugreport_file"

if [ -f "$bugreport_file" ]; then
    echo ""
    echo "======================================"
    echo "✓ Bug report saved: $bugreport_file"
    echo "======================================"
else
    echo ""
    echo "ERROR: Bug report generation failed"
    exit 1
fi

