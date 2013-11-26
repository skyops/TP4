#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
Created on 2013-10-28

@author: Bob
'''
import android
import Client
import time
import sys

def inputCommand(droid):
    title = 'Alert'
    message = ('Voulez vous mettre a jour laborescence')
    droid.dialogCreateAlert(title, message)
    #droid.dialogCreateAlert(title, message)
    droid.dialogSetPositiveButtonText('Yes')
    droid.dialogSetNegativeButtonText('No')
    #droid.dialogSetNeutralButtonText('Cancel')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    droid.dialogDismiss()
    #return response['which'] in ('positive', 'negative', 'neutral')
    return response

if __name__ == '__main__':
    droid = android.Android()
    #my_client = Client.client("162.209.100.18", 60017)
    my_client = Client(android.Android().dialogGetInput('IP').result,android.Android().dialogGetInput('Port').result)
    response = inputCommand(droid)
    
    if not 'which' in response or response['which'] != 'positive': 
        sys.exit()
    
    while True:
        droid.dialogCreateSpinnerProgress('Mise a jour', 'Veuillez passienter')
        droid.dialogShow()
        my_client.miseAjour(".")
        droid.dialogDismiss()
        time.sleep(300)