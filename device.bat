@echo off
echo.
echo ========================================
echo   SETTING UP ADB CONNECTION
echo ========================================
echo.

echo Disconnecting old connections...
adb disconnect >nul 2>&1

echo Checking for USB devices...
adb devices | find "device" | find /v "List" >nul
if errorlevel 1 (
    echo [!] No USB device detected or unauthorized.
    echo [TIP] Try "Wireless Debugging" on your OnePlus.
) else (
    echo [+] USB device found. Switching to TCPIP...
    adb tcpip 5555
    timeout /t 3 /nobreak >nul
)

:: Try to connect
echo.
set /p DEVICE_IP="Enter Phone IP (from Wireless Debugging Settings): "
if "%DEVICE_IP%"=="" set DEVICE_IP=192.168.0.4

echo Connecting to %DEVICE_IP%:5555...
adb connect %DEVICE_IP%:5555
echo.
adb devices
echo ========================================
echo.
