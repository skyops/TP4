#!/usr/bin/python   
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

from xml.dom.minidom import parse, parseString
from os import listdir
from os.path import isdir

#---------------------#
#-----#|Server|#-----#
#---------------------#
class server:
    """
        Classe représentant le serveur
    """
    #Réponse possible du serveur
    greetingTag = '<bonjourClient />'
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
        
    def bonjour(self):
        "Traitement de <bonjourServeur/>"
        
        dom = parseString(self.greetingTag)
        return dom.toxml()
    
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
    
    def miseAJour(self):
        "Met à jour les données depuis le site gouvernemental du québec"
        miseAJourValid = False
        return miseAJourValid

    def televerserfichier(self, folder, fileToAdd):
        "Traitement de <televerserfichier>"
        
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                #print os.path.join(dirname, subdirname)
                if (subdirname == folder):
                    pass#Créer un nouveau fichier selon fileToAdd
            
        dom = "<televerserfichier/>"
        return dom.toxml()
    
    def Parse_File(self, File):
		pass
        #Parse le fichier des données ouverte de la ville et en fait un fichier utilisable par l'application
        
    def VerifierDonneesVille(self,date):
        pass
        #Si la date de modification des fichiers est plus grande que la date du dernier  téléchargement, le logiciel
        #télécharge la nouvelle version et récupère cette date
    
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
        msgClient = serv.connexion.recv(serv.MAX_RECV)
        
        try:
            dom = parseString(msgClient)
        except:
            print "XML invalide!"
            serv.connexion.close()
            break
        
        # Traitement de <bonjourServeur />
        for node in dom.getElementsByTagName('bonjourServeur'):
            if node.firstChild == None:
                msgServer = serv.bonjour()
        
        # Traitement de <questionNomServeur/>
        for node in dom.getElementsByTagName('nomServeur'):
            if node.firstChild == None:
                msgServer = serv.nom()

        # Traitement de <televerserFichier/>
        for node in dom.getElementsByTagName('televerserFichier'):
            msgServer = serv.televerserfichier(node.firstChild.data)
        
		# Traitement de <VerifierDonneesVille/>
        for node in dom.getElementsByTagName('VerifierDonneesVille'):
            msgServer = serv.VerifierDonneesVille(node.firstChild.data)
		
        # Traitement de <quitter/>
        for node in dom.getElementsByTagName('quitter'):
            msgServer = serv.quitter()
          
        serv.connexion.send(msgServer)
        print "Envoi au client le xml : " + msgServer