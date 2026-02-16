@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo       Voris ADB Connection Setup
echo ==========================================

echo [1/5] Disconnecting old connections...
adb disconnect > nul 2>&1

echo [2/5] Restarting ADB server...
adb kill-server
adb start-server

echo [3/5] Checking for connected devices...
adb devices
echo.

echo [4/5] Enabling TCP/IP mode on port 5555...
adb tcpip 5555
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] ERROR: Device not found or unauthorized.
    echo.
    echo Troubleshooting:
    echo 1. Connect your phone via USB.
    echo 2. Check your phone screen for "Allow USB debugging?".
    echo 3. Select "Always allow from this computer" and tap OK.
    echo.
    rem pause removed to allow automatic startup
    exit /b 1
)

echo [5/5] Connecting over Wi-Fi...
echo Waiting for device to initialize (3s)...
timeout /t 3 /nobreak > nul

echo Discovering device IP address...
set ipfull=

rem Try to find the first non-local IPv4 address
for /f "tokens=2" %%a in ('adb shell "ip -4 addr show | grep inet | grep -v 127.0.0.1"') do (
    if "!ipfull!"=="" (
        set ipfull=%%a
    )
)

if "%ipfull%"=="" (
    echo [!] WARNING: Could not discover IP automatically.
    echo Fallback to 192.0.0.4. If this is wrong, specify IP manually in device.bat.
    set ip=192.0.0.4
) else (
    for /f "delims=/" %%a in ("%ipfull%") do set ip=%%a
)

echo Connecting to %ip%:5555...
adb connect %ip%:5555

echo.
echo Setup finished. Final status:
adb devices
echo.
echo ==========================================
echo [PRO TIP] You can now unplug the USB cable.
echo Everything is set for the next step!
echo ==========================================
rem pause removed to allow automatic startup
