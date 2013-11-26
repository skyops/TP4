#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
Created on 2013-10-28

@author: Bob
'''

import subprocess

ADB = r'C:\Android\adt-bundle-windows-x86_64-20130917\sdk\platform-tools\adb.exe'
APPLICATION = 'androidInterface.py'
TARGET = '/sdcard/sl4a/scripts/'

def main():
    # Upload the application.   
    subprocess.call([ADB, '-e', 'push', APPLICATION, TARGET + APPLICATION])
    
    # Launch the application.
    
    subprocess.call([ADB, '-e', 'shell', 'am', 'start',
          '-a', 'com.googlecode.android_scripting.action.LAUNCH_BACKGROUND_SCRIPT',
          '-n',
           'com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher',
          '-e', 'com.googlecode.android_scripting.extra.SCRIPT_PATH',
          TARGET + APPLICATION])
    
if __name__ == '__main__':
    main()