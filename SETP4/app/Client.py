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
    "Méthode pour générer le texte en format XML correctement"
    try:
      dom = xml.dom.minidom.parseString(textexml)
    except:
      print "XML invalide pour \"" + textexml + "\""
      self.connexion.close()
      sys.exit(1)
 
    return dom.toxml()
 
  def envoyer_recevoir(self, requeteXML, timeout=1):
    "Méthode pour recevoir la réponse du serveur."
 
    self.connexion.send(self.genXML(requeteXML))
 
    if timeout == 0:
      reponseXML = self.connexion.recv(MAX_RECV)
    else:
      reponseXML = recv_timeout(self.connexion, timeout)
 
    return reponseXML
 
  def existeDossier(self, dossier):
    "Requête au serveur de l'existence d'un dossier"
 
    requeteXML= "<questionListeDossiers>" + dossier + "</questionListeDossiers>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = False
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <listeDossiers>
    for node in dom.getElementsByTagName('listeDossiers'): 
      reponseClient = True
 
    return reponseClient
 
  def listeDossier(self, dossier):
    "Requête au serveur pour obtenir la liste des sous-dossiers d'un dossier"
 
    requeteXML= "<questionListeDossiers>" + dossier + "</questionListeDossiers>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = []
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    liste_dossiers = []
    # Traitement de <listeDossiers>
    for node in dom.getElementsByTagName('listeDossiers'): 
      for node2 in node.getElementsByTagName('dossier'):
        dossier = node2.firstChild.data
        liste_dossiers += [dossier]
 
      reponseClient = liste_dossiers
 
    return reponseClient
 
  def existeFichier(self, fichier, dossier):
    "Requête au serveur de l'existence d'un fichier"
 
    requeteXML= "<questionListeFichiers>" + dossier + "</questionListeFichiers>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = False
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <listeFichiers>
    for node in dom.getElementsByTagName('listeFichiers'):
      for node2 in node.getElementsByTagName('fichier'):
        fichier_trouve = node2.firstChild.data
        if fichier_trouve.find(fichier) != -1:
          reponseClient = True
 
    return reponseClient
 
  def listeFichiers(self, dossier):
    "Requête au serveur pour obtenir la liste des fichiers d'un dossier"
 
    requeteXML= "<questionListeFichiers>" + dossier + "</questionListeFichiers>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = []
 
    liste_fichiers = []
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <listeFichiers>
    for node in dom.getElementsByTagName('listeFichiers'):
      for node2 in node.getElementsByTagName('fichier'):
        fichier = node2.firstChild.data
        liste_fichiers += [ fichier ]
 
      reponseClient = liste_fichiers
 
    return reponseClient
 
  def creerDossier(self, dossier):
    "Requête de création d'un fichier sur le serveur"
 
    requeteXML= "<creerDossier>" + dossier + "</creerDossier>"
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = False
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <listeDossiers>
    for node in dom.getElementsByTagName('ok'): 
      reponseClient = True
 
    return reponseClient
 
  def televerserFichier(self, nom, dossier):
    "Requête de téléversement d'un fichier."
 
    contenu = ""
 
    # Réponse par défaut.
    reponseClient = False
 
    fichier = dossier + nom
    contenu = open(fichier).read()
    m = hashlib.md5()
    m.update(contenu)
    sign_serveur = m.hexdigest()
 
    contenu_encode = base64.b32encode(contenu)
 
    fichier_stat = os.stat(fichier)
    date_modif = fichier_stat.st_mtime 
 
 
    requeteXML = "<televerserFichier>" + \
                 "<nom>" + nom + "</nom>" + \
                 "<dossier>" + dossier + "</dossier>" + \
                 "<signature>" + sign_serveur + "</signature>" + \
                 "<contenu>" + contenu_encode + "</contenu>" + \
                 "<date>" + str(date_modif) + "</date>" + \
                 "</televerserFichier>"
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML)
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <listeDossiers>
    for node in dom.getElementsByTagName('ok'): 
      reponseClient = True
 
    return reponseClient
 
  def telechargerFichier(self, nom, dossier):
    "Requête de téléchargement d'un fichier."
 
    requeteXML = "<telechargerFichier>" + \
                 "<nom>" + nom + "</nom>" + \
                 "<dossier>" + dossier + "</dossier>" + \
                 "</telechargerFichier>"
 
    # Réponse par défaut.
    reponseClient = False
 
    # Envoyer la requête et Attendre la réponse.
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
 
  def supprimerFichier(self, nom, dossier):
    "Requête au serveur pour obtenir la liste des sous-dossiers d'un dossier"
 
    requeteXML= "<supprimerFichier>" + \
                "<nom>" + nom + "</nom>" + \
                "<dossier>" + dossier + "</dossier>" + \
                "</supprimerFichier>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = False
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <ok>
    for node in dom.getElementsByTagName('ok'): 
      reponseClient = True
 
    return reponseClient
 
  def supprimerDossier(self, dossier):
    "Requête au serveur pour obtenir la liste des sous-dossiers d'un dossier"
 
    requeteXML= "<supprimerDossier>" + dossier + "</supprimerDossier>"
 
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    # Réponse par défaut.
    reponseClient = False
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement de <ok>
    for node in dom.getElementsByTagName('ok'): 
      reponseClient = True
 
    return reponseClient
 
  def fichierRecent(self, nom, dossier):
    "Requête de comparaison des fichiers client et serveur."
 
    fichier = dossier + nom
    fichier_stat = os.stat(fichier)
    date_modif = fichier_stat.st_mtime
 
    requeteXML = "<questionFichierRecent>" + \
                 "<nom>" + nom + "</nom>" + \
                 "<dossier>" + dossier + "</dossier>" + \
                 "<date>" + str(date_modif) + "</date>" + \
                 "</questionFichierRecent>"
 
    # Réponse par défaut.
    reponseClient = False
 
    # Envoyer la requête et Attendre la réponse.
    reponseXML = self.envoyer_recevoir(requeteXML, 0)
 
    dom = xml.dom.minidom.parseString(reponseXML)
 
    # Traitement
    for node in dom.getElementsByTagName('oui'): 
      reponseClient = True
 
    return reponseClient
 
  def miseAjour(self, dossier):
    "Mise à jour de l'arborescence"
 
    # Parcours de l'arborescence sur le client...
    for racine, reps, noms in os.walk(dossier):
 
      # Corriger la syntaxe de la racine si nécessaire.
      if racine[-1] == '/':
        racine_corrigee = racine
      else:
        racine_corrigee = racine + '/'
 
      # Parcours des répertoires...
      for nom_rep in reps:
 
        # On crée le dossier si nécessaire.
 
        if not self.existeDossier(racine_corrigee + nom_rep):
          self.creerDossier(racine_corrigee + nom_rep)
 
      # Parcours des répertoires...
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
 
      # Corriger la syntaxe de la racine si nécessaire.
      if nom_dossier[-1] == '/':
        nom_dossier_corrigee = nom_dossier
      else:
        nom_dossier_corrigee = nom_dossier + '/'
 
      # Si c'est un dossier...
      if not os.path.exists(nom_dossier_corrigee):
        # On crée le dossier localement.
        os.mkdir(nom_dossier_corrigee)
 
      for nom_fichier in self.listeFichiers(nom_dossier_corrigee):
 
          if not os.path.exists(nom_dossier_corrigee + nom_fichier):
 
            self.telechargerFichier(nom_fichier, nom_dossier_corrigee)
     
##########################################
### Main ###
if __name__ == '__main__':
 
  if len(sys.argv) != 2:
    print("Ce client prend le numéro du port en paramètre.")
    sys.exit(1)

  # Récurérer le numéro du port en paramètre du serveur.  
  port = int(sys.argv[1])
  
  racine = "."
  
  conn_client = client("162.209.100.18", port)
  #conn_client = client("localhost", port)
  
  conn_client.miseAjour(racine)
