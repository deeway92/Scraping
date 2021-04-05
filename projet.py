#Importation des modules python besoin

import requests #Utilisé pour faire une requests
from bs4 import BeautifulSoup #Utilisé pour le scraping
import mysql.connector #Utilisé pour se connecter à la base de données
import re #Utilisé pour faire des opérations à base d'expressions rationnelles
import string #Utilisé pour faire des opérations usuelles sur des chaînes de caractères

#__________________________________Partie Scraping_______________________________________________
#Code permettant de récupérer des valeurs sur une page HTML

Liste  = [] #On cré une liste de vide "Liste"


try:
    for i in range(73): 
        url = 'https://www.cinenews.be/fr/cinema/programme/prochainement/?startrow=' + str(i+1) #Boucle qui change la dernière valeurs de l'URL pour parcourir toutes les pages du sites 
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text)

        for links in soup.findAll("h3", class_="stk-title visible-lg visible-md visible-sm visible-xs"): #On récupère les valeurs dans le code HTLM
            a = links.text
            Liste.append(a) #On ajoute les valeurs "a" dans la liste de vide "Liste"
    print(Liste)
except Exception as e:
    print("[IL Y A UNE ERREUR !]", e)




def remove_duplicate(duplist): #Fonction pour pouvoir supprimer les élements dupliquer dans notre liste
    noduplist = []
    for element in duplist:
        if element not in noduplist:
            noduplist.append(element)
    return noduplist

fin = remove_duplicate(Liste)

fin.remove ("The Conjuring 3 : Sous l'Emprise du Diable") #On enlève toutes les valeurs qui font bug le code (pour l'instant)
fin.remove ("Spirit: L'Indomptable")
fin.remove ("Don't Breathe 2")
fin.remove ("D'où l'on vient")
fin.remove("SOS Fantômes: L'Héritage")
fin.remove("Jurassic World: Le Monde d'Après")
print(fin)

#____________________________________Partie base de données_________________________________________

try:
    con= mysql.connector.connect(host='127.0.0.1 ',database='discord',user='root',password='') #On se connecte à la base de données
    print(con)
    cursor=con.cursor()
    print(cursor)
    req = "SELECT * FROM film " #Met dans une variable la requete demandé
    cursor.execute(req) #On exécute la requete
    cursor.fetchall() # Retourne un tableau contenant toutes les lignes du jeu d'enregistrements
    print(cursor.fetchall)

    for i in range(len(fin)-2): #Création d'une boucle pour pouvoir insérer toutes les valeurs dans la liste une par une sans le faire à la main
        print(fin[i])
        sql = f"INSERT INTO film (id_film, films_nom) VALUES (NULL, '{fin[i]}');" #requête SQL pour mettre les valeurs dans la BDD
        cursor.execute(sql) #On exécute la requête
    b = cursor.execute(sql)
    if b == b:
        print("Toutes les valeurs on bien été mise dans la base de données !")


except Exception as e:
    print("[IL Y A UNE ERREUR !]", e)
    con.rollback()

finally:
    con.commit()


#_______________________________Affichage de la base de données____________________________________

#Code permettant à afficher les valeurs dans notre base de données

con= mysql.connector.connect(host='127.0.0.1 ',database='discord',user='root',password='') #On connecte à notre base de données


sql = "SELECT * FROM `film` ORDER BY `id_film` ASC"  #on sélectionne toute les valeurs entrées

cursor = con.cursor()

cursor.execute(sql)

records = cursor.fetchall()

print("\nNombre total de ligne dans la table: ", cursor.rowcount)

print("\nVoici les prochaines sorties de films en 2021 !")
for row in records:
    print("Nom des films | ", row[1], )
    print("----------------------------------------------------------")














