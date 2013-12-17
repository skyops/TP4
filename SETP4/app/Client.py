#!/usr/bin/python   
# -*- coding: iso-8859-1 -*-
 
import socket
import sys
import hashlib
import base64
import os
import time

import xml.dom.minidom

MAX_RECV = 1024 * 1024 *30 
 #test1212123456789
# http://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/dfgfg
def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
  
    #total data partwise in an array
    total_data=[];
    data='';
 
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
 
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
  
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
            #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

  #make socket blocking
  
  the_socket.setblocking(1)
  
  #join all parts to make final string
  return ''.join(total_data)
 
class client:
  """
  Squelette du client
  """
 
 
  # Socket de connexion au serveur.
  connexion = None
  
  # --- CONSTRUCTEUR ---
  def __init__(self, host, port):
    "Connexion du client au serveur"
 
    self.connexion = socket.socket() 
 
    self.connexion.connect((host, port))
 
  def genXML(self, textexml):
    "M�thode pour g�n�rer le texte en format XML correctement"
    try:
      dom = xml.dom.minidom.parseString(textexml)
    except:
      print "XML invalide pour \"" + textexml + "\""
      self.connexion.close()
      sys.exit(1)
 
    return dom.toxml()
 
  def envoyer_recevoir(self, requeteXML, timeout=1):
    "M�thode pour recevoir la r�ponse du serveur."
 
    self.connexion.send(self.genXML(requeteXML))
 
    if timeout == 0:
      reponseXML = self.connexion.recv(MAX_RECV)
    else:
      reponseXML = recv_timeout(self.connexion, timeout)
 
    return reponseXML

  def transf�rerDonn�esMaps(self, longitude, latitude):
      #Transmet notre position � google maps et affiche le r�seau le plus pr�s de l'utilisateur sur la carte
      
  def afficherWifiPlusProche(self, longitude, latitude):
      #On compare la longitude et latitude de l'utilisateur avec ceux dans le fichier contenant 
      #les coordon�es des r�seaux et on affiche celui dont les coordon�es sont les plus semblables � 
      #ceux de lutilisateur
 
  def listeReseaux(self, fichier):
      #permet de dresser la liste des diff�rents reseaux disponibles dans la ville de Qu�bec avec leur adresses
      #en lisant le fichier texte contenant les donn�es de la ville
      
      
      
  def Localiser(self):
      #R�cupp�re la longitude et la latitude de l'utilisateur avec le gps du t�l�phone
      longitude= ""
      latitude = ""
      
      return longitude, latitude
 
  
 
  
 
  def telechargerFichier(self,):
    "Requ�te de t�l�chargement d'un fichier."
 
    requeteXML = "<telechargerFichier>" + \
                 "</telechargerFichier>"
 
    # R�ponse par d�faut.
    reponseClient = False
 
    # Envoyer la requ�te et Attendre la r�ponse.
    reponseXML = self.envoyer_recevoir(requeteXML)
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    signature= ""
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
 

  def miseAjour(self, dossier):
    "Mise � jour de l'arborescence"
 
    # Parcours de l'arborescence sur le client...
    for racine, reps, noms in os.walk(dossier):
 
      # Corriger la syntaxe de la racine si n�cessaire.
      if racine[-1] == '/':
        racine_corrigee = racine
      else:
        racine_corrigee = racine + '/'
 
      # Parcours des r�pertoires...
      for nom_rep in reps:
 
        # On cr�e le dossier si n�cessaire.
 
        if not self.existeDossier(racine_corrigee + nom_rep):
          self.creerDossier(racine_corrigee + nom_rep)
 
      # Parcours des r�pertoires...
      for nom_fichier in noms:
 
        # Si le fichier n'existe pas sur le serveur...
        if not self.existeFichier(nom_fichier, racine_corrigee):
 
          self.televerserFichier(nom_fichier, racine_corrigee)
 
        else:
 
          # Si le fichier existe sur le serveur...
          if self.fichierRecent(nom_fichier, racine_corrigee):
 
            os.remove(racine_corrigee + nom_fichier)
            self.telechargerFichier(nom_fichier, racine_corrigee)
 
          else:
 
            self.supprimerFichier(nom_fichier, racine_corrigee)
            self.televerserFichier(nom_fichier, racine_corrigee)
 
    # Parcours de l'arborescence sur le serveur...
    for nom_dossier in self.listeDossier(dossier) + ['./']:
 
      # Corriger la syntaxe de la racine si n�cessaire.
      if nom_dossier[-1] == '/':
        nom_dossier_corrigee = nom_dossier
      else:
        nom_dossier_corrigee = nom_dossier + '/'
 
      # Si c'est un dossier...
      if not os.path.exists(nom_dossier_corrigee):
        # On cr�e le dossier localement.
        os.mkdir(nom_dossier_corrigee)
 
      for nom_fichier in self.listeFichiers(nom_dossier_corrigee):
 
          if not os.path.exists(nom_dossier_corrigee + nom_fichier):
 
            self.telechargerFichier(nom_fichier, nom_dossier_corrigee)
     
##########################################
### Main ###
if __name__ == '__main__':
 
  if len(sys.argv) != 2:
    print("Ce client prend le num�ro du port en param�tre.")
    sys.exit(1)

  # R�cur�rer le num�ro du port en param�tre du serveur.  
  port = int(sys.argv[1])
  
  racine = "."
  
  conn_client = client("162.209.100.18", port)
  #conn_client = client("localhost", port)
  
  conn_client.miseAjour(racine)
