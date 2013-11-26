:1
adb push androidInterface.py /sdcard/sl4a/scripts
adb push Client.py /sdcard/sl4a/scripts
#adb -e shell am start -a com.googlecode.android_scripting.action.LAUNCH_BACKGROUND_SCRIPT -n com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher -e com.googlecode.android_scripting.extra.SCRIPT_PATH /sdcard/sl4a/scripts
@echo off
pause
goto 1