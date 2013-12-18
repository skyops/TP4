[21:14:42] roberge-champagne philippe: #!/usr/bin/python   
# -*- coding: iso-8859-1 -*-

'''
Created on 2013-10-06

@author: Bob
'''

import socket
import os
import hashlib
import shutil
import base64
import urllib2
import xlrd
from xml.dom.minidom import parse, parseString
from os import listdir
from os.path import isdir

#---------------------#
#-----#|Server|#-----#
#---------------------#
class server:
    """
        Classe représentant le serveur test
    """
    #Réponse possible du serveur
    nameOfServer = '<nomServeur>Ubuntu Dropbox 1.0</nomServeur>'
    
    # Se donner un objet de la classe socket.
    my_socket = socket.socket()
    
    # Socket connexion au client.
    connexion = None
    
    MAX_RECV = 1024
    
    
    # Constructeur
    def __init__(self, host, port):
        "Constructeur du serveur et attendre une connection"
                self.miseAJour();
        self.my_socket.bind((host, port))    
        
        # Passer en mode écoute.
        self.my_socket.listen(5)  
        
        c, addr = self.my_socket.accept()
        self.connexion = c
        date_ville= ""
  
 #Si la date de modification des fichiers est plus grande que la date du dernier  téléchargement, le logiciel
    #télécharge la nouvelle version et récupère cette date
     def updateFile(self):
  "Met à jour les données depuis le site gouvernemental du québec"
        dataXLS = urllib2.urlopen("http://donnees.ville.quebec.qc.ca/Handler.ashx?id=29&f=XLS")
        
        fData = open('wifiData.xls','w')
        fData.write(dataXLS.read())
        fData.close()
        self.parseWifiData('wifiData')
        '''
        Le lien pour ce fichier source n'est pas encore déterminé
        updateFile = urllib2.urlopen("http://donnees.ville.quebec.qc.ca/donne_details.aspx?jdid=63")
        '''
        
        '''
        fUpdate = open('update.xml','w')
        fUpdate.write(dataFile.read())
        fUpdate.close()
        '''  
    
 #Parse le fichier des données ouverte de la ville et en fait un fichier utilisable par l'application
    def parseWifiData(file):  
        ftxt = open(file + '.txt', 'w')
        workbook = xlrd.open_workbook(file + '.xls')
        wifiSheet = workbook.sheet_by_name('WIFI')
        num_rows = wifiSheet.nrows - 1
        num_cells = wifiSheet.ncols - 1
        curr_row = -1
        
        while curr_row < num_rows:
         curr_row += 1
         row = wifiSheet.row(curr_row)
         curr_cell = -1
         cell_type = wifiSheet.cell_type(curr_row, curr_cell)
         cell_value = wifiSheet.cell_value(curr_row, curr_cell)
         ftxt.write(
          wifiSheet.cell(curr_row, 1) + ',' +
          wifiSheet.cell_value(curr_row, 2)+',' +
          wifiSheet.cell_value(curr_row, 3)+',' +
          wifiSheet.cell_value(curr_row, 4)+':')
        
        ftxt.close()
    
    def nom(self):
        "Traitement de <questionNomServeur>"
     
        dom = parseString(self.nameOfServer)
        return dom.toxml()
    
    def telechargerFichier(self):
        "Requête de téléchargement d'un fichier."
     
        requeteXML = "<telechargerFichier>" + \
                     "</telechargerFichier>"
                
                # Si le transfert c'est bien éffectué
        validTransfert = False
        
        # Envoyer la requête et Attendre la réponse.
        reponseXML = self.envoyer_recevoir(requeteXML)
        
        dom = parseString(reponseXML)
        
        signature = ""
        contenu = ""
        date = ""
        for node in dom.getElementsByTagName('fichier'): 
          reponseClient = True
     
          if node.firstChild != None:
            for node2 in node.getElementsByTagName('signature'):
              signature = node2.firstChild.data
     
            for node2 in node.getElementsByTagName('contenu'):
              if node2.firstChild == None:
                contenu = ""
              else:
                contenu = node2.firstChild.data
     
            for node2 in node.getElementsByTagName('date'):
                date_modif = node2.firstChild.data
     
        
        contenu_decode = base64.b32decode(contenu)
        fichier = dossier + nom
        
        if signature != "":
          m = hashlib.md5()
          m.update(contenu_decode)
          sign_serveur = m.hexdigest()
     
          if signature != sign_serveur:
            print("Erreur: Erreur de transfert du fichier " + fichier)
     
          obj_fichier = open(fichier, "wb")
          obj_fichier.write(contenu_decode)
          obj_fichier.close()
     
          fichier_stat = os.stat(fichier)
          date_acces = fichier_stat.st_atime
     
          os.utime(fichier,(date_acces,float(date_modif)))
     
        return reponseClient
 
 #Génére le xml pour l'envoi d'un fichier texte TODO: retourner xml avec le fichier wifiData.txt
    def televerserfichier(self, fileName):
 
        "Traitement de <televerserfichier>"
        dom = '<televerserfichier>'
  '''
        for dirname, dirnames, fileName in os.walk('.'):
            for subdirname in dirnames:
                #print os.path.join(dirname, subdirname)
                if (subdirname == folder):
                    pass#Créer un nouveau fichier selon fileToAdd
  '''
        dom += "<televerserfichier/>"
  with open('wifiData.txt', mode='rb') as file: 
   dom = file.read()
   file.closed
        return dom
        
    
 #Termine la connection
    def quitter(self):
        msg = "<ok/>"
        return msg.toxml()
  
#--------------------#
#------#|Main|#------#
#--------------------#
if __name__ == '__main__':
    serv = server('', 50017)
        
    msgServer = ""
    while True:
        
        # On attend un message du client.
        msgClient = my_server.connexion.recv(my_server.MAX_RECV)
        
        try:
            dom = parseString(msgClient)
        except:
            print "XML invalide!"
            my_server.connexion.close()
            break
   
        # Traitement de <update/>
        for node in dom.getElementsByTagName('update'):
   if node.firstChild == None:
    my_server.updateFile()
    msgServer = my_server.televerserfichier()
        
        # Traitement de <questionNomServeur/>
        for node in dom.getElementsByTagName('nomServeur'):
            if node.firstChild == None:
                msgServer = my_server.nom()
        
                
        # Traitement de <quitter/>
        for node in dom.getElementsByTagName('quitter'):
            msgServer = my_server.quitter()
          
        my_server.connexion.send(msgServer)
        print "Envoi au client le xml : " + msgServer