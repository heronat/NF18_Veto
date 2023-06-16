from tkinter import *
import psycopg2 as ps


# fonction de connexion à la base de donnée, des valeurs sont entrées par défaut mais on peut entrer des valeurs si on veut utiliser une autre base de donnée
def connexion(dbname="dbnf18a029", user="nf18a029", password="Y1odKfZJ", host="tuxa.sme.utc", port="5432"):
    conn = ps.connect(host=host, database=dbname, user=user, password=password, port=port)
    return conn


# insère un client d'abord dans la table personne pouis dans la Table Client
# ne gère ni ne vérifies les numéros bis/ter pour le moment
def inserer_client(conn, nom, prenom, datenaiss, numero, rue, ville, codep, telephone):
    # pas de vérification sur la date de naissance car ca sera a terme un choix sur un calendrier

    # vérifications sur numéro de telephone
    try:
        int(telephone)
    except ValueError:
        raise ("Erreur : le numéro de télephone ne doit contenir que des chiffres")

    if len(telephone) != 10:
        raise ("Erreur : Le numéro de télephone doit contenir 10 chiffes")
    if telephone[0] != '0':
        raise ("Erreur : Le numéro de télephone doit commencer par un 0")

    # vérification sur le cde postal
    try:
        int(codep)
    except ValueError:
        raise ("Erreur : le code postal ne doit contenir que des chiffres")

    if len(codep) != 5:
        raise ("Erreur : Le code postal doit contenir 5 chiffes")

    cur = conn.cursor()

    # insertion du client dans la table personne
    query1 = f"INSERT INTO Personne VALUES (DEFAULT, '{nom}', '{prenom}', '{datenaiss}', {numero}, '{rue}', '{ville}', {codep}, {telephone});"
    cur.execute(query1)
    conn.commit()

    # récupération de l'id (généré automatiquement)
    query2 = f"SELECT id FROM Personne WHERE telephone = {telephone};"
    # telephone peut etre utilisé ici pour retrouver une personne, comme la commande à lieu juste après qu'il ait été entré dans la tables, il n'aurras pas eu le temps de changer de numéro
    cur.execute(query2)
    id = cur.fetchall()[0][0]

    # insertion dans la table Client
    query3 = f"INSERT INTO Client VALUES ({id});"
    cur.execute(query3)
    conn.commit()
    cur.close()


def inserer_personnel(conn, nom, prenom, datenaiss, numero, rue, ville, codep, telephone, specialite, poste):
    # pas de vérification sur la date de naissance car ca sera a terme un choix sur un calendrier
    # vérifications sur numéro de telephone
    try:
        int(telephone)
    except ValueError:
        raise ("Erreur : le numéro de télephone ne doit contenir que des chiffres")

    if len(telephone) != 10:
        raise ("Erreur : Le numéro de télephone doit contenir 10 chiffes")
    if telephone[0] != '0':
        raise ("Erreur : Le numéro de télephone doit commencer par un 0")

    # vérification sur le cde postal
    try:
        int(codep)
    except ValueError:
        raise ("Erreur : le code postal ne doit contenir que des chiffres")

    if len(codep) != 5:
        raise ("Erreur : Le code postal doit contenir 5 chiffes")

    # vérification de la spécialité
    if not (specialite in ['félins', 'canidés', 'reptiles', 'rongeurs', 'oiseaux', 'autres']):
        raise ("specialite incorrecte")

    # vérification sur le poste
    if not (poste in ['Veterinaire', 'Assistant']):
        raise ("poste incorrect")

    cur = conn.cursor()

    # insertion dans la table personne
    query1 = f"INSERT INTO Personne VALUES (DEFAULT, '{nom}', '{prenom}', '{datenaiss}', {numero}, '{rue}', '{ville}', {codep}, {telephone});"
    cur.execute(query1)
    conn.commit()

    # récupération de l'id (généré automatiquement)
    query2 = f"SELECT id FROM Personne WHERE telephone = {telephone};"
    # telephone peut etre utilisé ici pour retrouver une personne, comme la commande à lieu juste après qu'il ait été entré dans la tables, il n'aurras pas eu le temps de changer de numéro
    cur.execute(query2)
    id = cur.fetchall()[0][0]

    # insertion dans la table Personnel
    query3 = f"INSERT INTO Personnel VALUES ({id}, '{specialite}');"
    cur.execute(query3)
    conn.commit()

    if poste == 'Veterinaire':

        query4 = f"INSERT INTO Veterinaire VALUES ({id});"
        cur.execute(query4)
        conn.commit()

    else:
        query4 = f"INSERT INTO Assistant VALUES ({id});"
        cur.execute(query4)
        conn.commit()


# fonction permettant d'insérer un nouveau médicament dans la table Medicament
def inserer_medicament(conn, mol, effets):
    cur = conn.cursor()

    # on vérifie qu'il n'exista pas déjà un medicament qui à la même molécule (clé primaire)
    query1 = f"SELECT molecule FROM Medicament WHERE molecule = '{mol}';"
    cur.execute(query1)
    list = cur.fetchall()
    print(list)

    if list:
        raise ("Erreur : cette molécule existe déja")
    print('test')
    query2 = f"INSERT INTO Medicament VALUES ('{mol}','{effets}')"
    cur.execute(query2)
    conn.commit()

    cur.close()


# Fonction permettant d'insérer un animal dans la table animal
def inserer_animal(conn, nom, espece, date_naissance=None, puce=None, passeport=None):
    # pas de vérifications sur la date car elle sera à terme demandé via un calendrier
    # meme chose pour espece qui sera indiquée via un menu

    # véfificaton que la puce ne comporte que des chiffre ou traduit le type None de python en NULL sql
    if puce != None:
        try:
            int(puce)
        except ValueError:
            raise ("Erreur : la puce ne doit contenir que des chiffres")
    else:
        puce = 'NULL'

    # véfificaton que le nimero de passeport ne comporte que des chiffre ou traduit le type None de python en NULL sql
    if passeport != None:
        try:
            int(passeport)
        except ValueError:
            raise ("Erreur : le numero de passeport ne doit contenir que des chiffres")
    else:
        passeport = 'NULL'

    cur = conn.cursor()

    query = f"INSERT INTO Animal VALUES (DEFAULT,'{nom}','{date_naissance}',{puce},{passeport},'{espece}');"

    cur.execute(query)
    conn.commit()

    cur.close()


def inserer_appartenance(conn, id_animal, id_client, ddebut, dfin=None):
    # pas de vérification car les données seront toutes entrées a terme via des menus ou des calendriers
    # verif sur la date de début < date de fin à traiter
    if dfin == None:
        dfin = 'NULL'
    else:
        dfin = f"\'{dfin}\'"

    cur = conn.cursor()
    query = f"INSERT INTO Appartient VALUES ('{id_animal}','{id_client}','{ddebut}',{dfin});"
    cur.execute(query)
    conn.commit()
    cur.close()


def inserer_poids(conn, id_animal, poids):
    try:
        float(poids)
    except ValueError:
        raise ("Erreur : le poids dois être un flottant")

    cur = conn.cursor()

    query = f"INSERT INTO Poids VALUES (DEFAULT,{poids},now(),{id_animal});"
    cur.execute(query)
    conn.commit()
    cur.close()


def inserer_taille(conn, id_animal, taille):
    try:
        float(taille)
    except ValueError:
        raise ("Erreur : la taille dois être un flottant")

    cur = conn.cursor()

    query = f"INSERT INTO Taille VALUES (DEFAULT,{taille},now(),{id_animal});"
    cur.execute(query)
    conn.commit()
    cur.close()


def inserer_analyse(conn, id_animal, lien):
    cur = conn.cursor()
    query = f"INSERT INTO Analyses VALUES (DEFAULT,'{lien}', now(),{id_animal});"
    cur.execute(query)
    conn.commit()
    cur.close()


def inserer_procedure(conn, id_animal, nom, descriprion):
    cur = conn.cursor()
    query = f"INSERT INTO Procedure VALUES (DEFAULT,'{nom}','{descriprion}',now(),{id_animal});"
    cur.execute(query)
    conn.commit()
    cur.close()


def inserer_traitement(conn, ddebut, duree, medicament, veto, animal):
    try:
        int(duree)
    except ValueError:
        raise ("Erreur : la durée dois être un entier")

    if int(duree) < 1:
        raise ("Erreur : un traitement doit au mois durrer 1 jour")

    medicament = medicament.split(" ")

    cur = conn.cursor()
    query1 = f"INSERT INTO Traitement VALUES (DEFAULT,'{ddebut}','{duree}',now(),{veto},{animal});"
    cur.execute(query1)
    conn.commit()

    query2 = f"SELECT id FROM Traitement ORDER BY id DESC"
    cur.execute(query2)
    id = cur.fetchall()[0][0]

    for couple in medicament:
        medicament, quantite = couple.split(":")

        try:
            float(quantite)
        except ValueError:
            raise ("Erreur : la quantite dois être un flottant")

        if float(quantite) <= 0:
            raise ("Erreur : la quantité de médiacament doit etre strictement positive")

        query3 = f"SELECT molecule FROM Medicament WHERE molecule = '{medicament}';"
        cur.execute(query3)
        if medicament != cur.fetchall()[0][0]:
            raise ("Erreur : un des médicaments de fait pas parti de la base de donnée")

        query4 = f"INSERT INTO Prescrit VALUES ('{medicament}',{id},{quantite});"
        cur.execute(query4)
        conn.commit()

    cur.close()


def inserer_consultation(conn, id_animal, date, id_personnel, observation=None):
    if observation == None:
        observation = 'NULL'
    else:
        observation = f"\'{observation}\'"

    cur = conn.cursor()
    query = f"INSERT INTO Consultation VALUES (DEFAULT,'{date}',{observation},now(),'{id_animal}', '{id_personnel}');"
    cur.execute(query)
    conn.commit()
    cur.close()


def afficher(liste):
    len3 = 0
    m = len(liste[1])
    tab = '\t'
    if m == 0:
        raise ("Erreur : liste a afficher vide")
    taille = [0 for i in range(m)]
    for row in liste:
        for i in range(m):
            taille[i] = max(len(row[i]) // 4 + 1, taille[i])

    print("", end="|")
    for i in range(m):
        if len(liste[0][i]) % 4 == 3: len3 = 1
        print(f"{liste[0][i]}{(taille[i] - len(liste[0][i]) // 4 - len3) * tab}", end="|")
        len3 = 0
    print()
    print("", end="|")
    for i in taille[:-1]:
        print((i * 4 - 1) * "-", end="+")
    print((taille[m - 1] * 4 - 1) * "-", end="|\n")

    for row in liste[1:]:
        print("", end="|")
        for i in range(m):
            if len(row[i]) % 4 == 3: len3 = 1
            print(f"{row[i]}{(taille[i] - len(row[i]) // 4 - len3) * tab}", end="|")
            len3 = 0
        print()


def affichage_simple(conn, table):  # affichage d'une table passée en paramètre
    cur = conn.cursor()
    query = f"SELECT * FROM {table};"
    cur.execute(query)

    retour = cur.fetchall()


    for i in range(len(retour)) :
        retour[i]= list(retour[i])
        for j in range(len(retour[i])) :
            retour[i][j] = str(retour[i][j])

    querytitres = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}';"
    print(querytitres)
    cur.execute(querytitres)
    titres = cur.fetchall()
    print(titres)
    for i in range (len(titres)) :
       titres[i] = titres[i][0]

    print(titres)
    retour.insert(0,titres)
    cur.close()
    afficher(retour)


def affichage_personne(conn,
                       table):  # affichage d'une table passée en paramètre en jointure externe avec la table Personne
    cur = conn.cursor()
    query = f"SELECT p.id,p.nom,p.prenom FROM {table} t LEFT OUTER JOIN Personne p ON t.id=p.id WHERE p.id IS NOT NULL;"
    cur.execute(query)

    retour = cur.fetchall()

    cur.close()

    for i in range(len(retour)) :
        retour[i]= list(retour[i])
        for j in range(len(retour[i])) :
            retour[i][j] = str(retour[i][j])

    retour.insert(0, ["id", "Nom", "Prenom"])

    afficher(retour)

def affichage_veterinaire(conn):  # affichage d'une table passée en paramètre en jointure externe avec la table Personne
    cur = conn.cursor()
    query = f"SELECT * FROM Veterinaire v LEFT OUTER JOIN Personnel pl ON v.id=pl.id LEFT OUTER JOIN Personne p ON pl.id=p.id WHERE p.id IS NOT NULL AND pl.id IS NOT NULL;"
    cur.execute(query)

    retour = cur.fetchall()
    cur.close()

    for i in range(len(retour)) :
        retour[i]= list(retour[i])
        for j in range(len(retour[i])) :
            retour[i][j] = str(retour[i][j])

    retour.insert(0, ["id", "Nom", "Prenom"])

    afficher(retour)



def liste_quantite_medicament(conn, debut_periode, fin_periode):
    cur = conn.cursor()
    sql = f"SELECT m.molecule, (t.duree * p.quantite * COUNT(*)) AS nombre FROM Medicament m INNER JOIN Prescrit p ON m.molecule = p.medicament INNER JOIN Traitement t ON p.traitement = t.id WHERE t.date_debut - '{debut_periode}' > 0 AND '{fin_periode}' - t.date_debut > t.duree GROUP BY m.molecule, t.duree, p.quantite;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"[{raw[0]}] : {raw[1]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def liste_quantite_traitement(conn, debut_periode, fin_periode):
    cur = conn.cursor()
    sql = f"SELECT m.molecule, (t.duree * p.quantite * COUNT(*)) AS nombre FROM Medicament m INNER JOIN Prescrit p ON m.molecule = p.medicament INNER JOIN Traitement t ON p.traitement = t.id WHERE t.date_debut - '{debut_periode}' > 0 AND '{fin_periode}' - t.date_debut > t.duree GROUP BY m.molecule, t.duree, p.quantite;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"Le nombre de traitements prescrits est : {raw[0]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def liste_procedure_animal(conn, var_animal):
    cur = conn.cursor()
    sql = f"SELECT Procedure.nom, date_saisie FROM Procedure INNER JOIN Animal ON Procedure.animal = Animal.id WHERE '{var_animal}' = Animal.nom ORDER BY date_saisie;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"Procédure : {raw[0]} faite le {raw[1]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def nb_animal_par_espece(conn):
    cur = conn.cursor()
    sql = f"SELECT COUNT(Animal.id), espece FROM Animal INNER JOIN Traitement ON Traitement.animal = Animal.id GROUP BY espece;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"[{raw[1]}] {raw[0]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def animal_par_client(conn, prenom_client, nom_client):
    cur = conn.cursor()
    sql = f"SELECT Animal.nom, Animal.date_naissance, Animal.espece, Animal.puce, Animal.passeport,Appartient.date_debut,Personne.prenom,Personne.nom FROM Animal,Appartient,Personne WHERE Appartient.animal = Animal.id AND Personne.nom = '{nom_client}' AND Personne.prenom = '{prenom_client}' AND Appartient.proprietaire = Personne.id;"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"{raw[6]} {raw[7]} : \n")
    while raw:
        print(f"[{raw[0]}] {raw[1]} {raw[2]} {raw[3]} {raw[4]} {raw[5]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def animal_actuel_par_client(conn, prenom_client, nom_client):
    cur = conn.cursor()
    sql = f"SELECT Animal.nom, Animal.date_naissance, Animal.espece, Animal.puce, Animal.passeport,Appartient.date_debut,Personne.prenom,Personne.nom FROM Animal,Appartient,Personne WHERE Appartient.animal = Animal.id AND Personne.nom = '{nom_client}' AND Personne.prenom = '{prenom_client}' AND Appartient.proprietaire = Personne.id;"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"{raw[6]} {raw[7]} :")
    while raw:
        print(f"[{raw[0]}] {raw[1]} {raw[2]} {raw[3]} {raw[4]} {raw[5]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def taille_poids(conn):
    print("Le poids :")
    cur = conn.cursor()
    sql = f"SELECT Animal.nom, Poids.mesure, Poids.date_saisie FROM Animal, Poids WHERE Poids.animal = Animal.id ORDER BY date_saisie;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"[{raw[0]}] {raw[1]} {raw[2]} ")
        raw = cur.fetchone()
    conn.commit()
    print("La taille :")
    sql = f"SELECT Animal.nom, Taille.mesure, Taille.date_saisie FROM Animal, Taille WHERE Taille.animal = Animal.id ORDER BY date_saisie;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"[{raw[0]}] {raw[1]} {raw[2]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def traitement_subi_par_animal(conn, nom_animal):
    cur = conn.cursor()
    sql = f"SELECT Animal.nom, Prescrit.medicament, Traitement.duree FROM Animal, Prescrit, Traitement WHERE Prescrit.traitement = Traitement.id AND Traitement.animal = Animal.id AND Animal.nom = '{nom_animal}' ORDER BY date_debut;"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"[{nom_animal}]")
    while raw:
        print(f"{raw[1]} {raw[2]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def traitement_en_cours(conn, nom_animal):
    cur = conn.cursor()
    sql = f"SELECT P.medicament, P.quantite, T.date_debut, T.duree FROM Traitement T JOIN Animal A ON T.animal = A.id JOIN Prescrit P ON P.traitement = T.id WHERE (A.nom = '{nom_animal}') AND ((CURRENT_DATE - T.date_debut) <= T.duree) ORDER BY T.date_debut;"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"[{nom_animal}]")
    while raw:
        print(f"{raw[0]} {raw[1]} {raw[2]} {raw[3]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def membre_personnel_reptiles(conn):
    print(f"Les vétérinaires :")
    cur = conn.cursor()
    sql = f"SELECT p.prenom, p.nom, p.date_naissance, p.numero, p.rue, p.ville, p.code_postal, p.telephone AS poste FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Veterinaire v ON v.id = pl.id WHERE pl.specialite = 'reptiles';"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"{raw[0]} {raw[1]} {raw[2]} {raw[3]} {raw[4]} {raw[5]} {raw[6]} 0{raw[7]}")
        raw = cur.fetchone()
    conn.commit()
    print("Pour les assistants :")
    sql = f"SELECT p.prenom, p.nom, p.date_naissance, p.numero, p.rue, p.ville, p.code_postal, p.telephone, 'Assistant' AS poste FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Assistant a ON a.id = pl.id WHERE pl.specialite = 'reptiles';"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"{raw[0]} {raw[1]} {raw[2]} {raw[3]} {raw[4]} {raw[5]} {raw[6]} 0{raw[7]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def animal_suivi_par_veterinaire(conn, prenom_veterinaire, nom_veterinaire):
    cur = conn.cursor()
    sql = f"SELECT id FROM Personne WHERE Personne.prenom = '{prenom_veterinaire}' AND Personne.nom = '{nom_veterinaire}'"
    cur.execute(sql)
    raw = cur.fetchone()
    id_veto = raw[0]
    conn.commit()
    sql = f"SELECT a.nom, a.espece FROM Animal a INNER JOIN Suit s ON a.id = s.animal INNER JOIN Personnel pl ON pl.id = s.personnel INNER JOIN Veterinaire v ON v.id = pl.id WHERE v.id = {id_veto} AND ((s.date_fin IS NULL) OR (CURRENT_DATE - s.date_fin <= 30));"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"[{prenom_veterinaire} {nom_veterinaire}]")
    while raw:
        print(f"{raw[0]} {raw[1]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def veterinaire_suivant_un_animal(conn, nom_animal):
    cur = conn.cursor()
    sql = f"SELECT id FROM Animal WHERE Animal.nom = '{nom_animal}'"
    cur.execute(sql)
    raw = cur.fetchone()
    id_animal = raw[0]
    conn.commit()
    sql = f"SELECT p.prenom, p.nom, s.date_debut, s.date_fin FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Veterinaire v ON pl.id = v.id INNER JOIN Suit s ON v.id = s.personnel WHERE s.animal = {id_animal} ORDER BY s.date_debut DESC;"
    cur.execute(sql)
    raw = cur.fetchone()
    print(f"[{nom_animal}]")
    while raw:
        print(f"{raw[0]} {raw[1]} {raw[2]} {raw[3]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def medicament_consomme_periode(conn, date_debut, date_fin):
    cur = conn.cursor()
    sql = f"SELECT m.molecule, (t.duree * p.quantite * COUNT(*)) AS nombre FROM Medicament m INNER JOIN Prescrit p ON m.molecule = p.medicament INNER JOIN Traitement t ON p.traitement = t.id WHERE t.date_debut - '{date_debut}' > 0 AND '{date_fin}' - t.date_debut > t.duree GROUP BY m.molecule, t.duree, p.quantite;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"[{raw[0]}] {raw[1]} ")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def traitement_par_periode(conn, date_debut, date_fin):
    cur = conn.cursor()
    sql = f"SELECT COUNT(*) AS nombre_traitements FROM Traitement WHERE date_debut - '{date_debut}' > 0 AND '{date_fin}' - date_debut > duree;"
    cur.execute(sql)
    raw = cur.fetchone()
    while raw:
        print(f"{raw[0]}")
        raw = cur.fetchone()
    conn.commit()
    cur.close()


def main():
    print("début")
    conn = connexion()
    # inserer_client(conn, "Drucker", "Michel", "1942-09-12", "80", "rue de l Université", "Paris", "75007", "0140760089")

    # inserer_personnel(conn, 'Dichel', 'Mrucker', "1985-06-21", "56", "rue des paparazis", "Paris", "75012", "0658987421", "reptiles", "Veterinaire")

    # insérer_medicament(conn,"Propylene glycol", "anti histaminique")

    # inserer_animal(conn, 'Isia', 'chien','2012-03-08')
    # inserer_appartenance(conn, 1, 1, '2016-08-09')

    # inserer_poids(conn, 3,'12.5','2022-12-03', '01:38')

    # inserer_taille(conn, 3, '32.4', '2022-12-03', '01:42')
    # inserer_analyse(conn, 3, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '2022-12-03', '01:42')
    # inserer_procedure(conn, 3, 'toilettage','lavage, shampoing, rincage, manucure, maquillage', '2022-12-03', '02:11')

    # inserer_traitement(conn, '2022-12-04','10', "Paracetamol:5 Dulcolax:2", 5, 3)

    continuer = True

    while continuer:
        print("1 : Insérer des données\n2 : Sélectionner des données\n")
        print("Entrez un autre chiffre pour quitter\n")
        choix = int(input("Votre choix : "))

        if choix == 1:  # Insertions
            print("\n1 : Insérer un membre du personnel\n2 : Insérer un client\n")
            print("3 : Insérer une information de propriétaire pour un animal\n")
            print("4 : Insérer un animal\n5 : Insérer un médicament\n")
            print("6 : Insérer une entrée dans un dossier médical\n")
            choix = int(input("Votre choix : "))

            if choix == 1:  # Insérer un membre du personnel
                nom = input("Nom : ")
                prenom = input("Prénom : ")
                date_naiss = input("Date de naissance : ")
                numero = input("Adresse, numéro de rue : ")
                rue = input("Adresse, nom de la rue : ")
                ville = input("Adresse, ville : ")
                codep = input("Adresse, code postal : ")
                telephone = input("Numéro de téléphone : ")
                specialite = input("Spécialité (félins, canidés, reptiles, rongeurs, oiseaux, autres) : ")
                poste = input("Poste (Veterinaire ou Assistant) : ")

                inserer_personnel(conn, nom, prenom, date_naiss, numero, rue, ville, codep, telephone, specialite,
                                  poste)

            elif choix == 2:  # Insérer un client
                nom = input("Nom : ")
                prenom = input("Prénom : ")
                date_naiss = input("Date de naissance : ")
                numero = input("Adresse, numéro de rue : ")
                rue = input("Adresse, nom de la rue : ")
                ville = input("Adresse, ville : ")
                codep = input("Adresse, code postal : ")
                telephone = input("Numéro de téléphone : ")

                inserer_client(conn, nom, prenom, date_naiss, numero, rue, ville, codep, telephone)

            elif choix == 3:  # Insérer une info de propriétaire pour un animal
                affichage_personne(conn,"Client")
                id_client = input("Entrez l'id du propriétaire : ")

                affichage_simple(conn,"animal")
                id_animal = input("Entrez l'id de l'animal : ")

                inserer_appartenance(conn, id_client, id_animal)

            elif choix == 4:  # Insérer un animal
                nom = input("Nom de l'animal : ")
                espece = input("Espèce : ")

                facultatif = input("Connaissez-vous sa date de naissance ? (o/n) ")
                if facultatif == "o":
                    date_naiss = input("Entrez sa date de naissance : ")
                else:
                    date_naiss = None

                facultatif = input("A-t-il un numéro de puce ? (o/n) ")
                if facultatif == "o":
                    puce = input("Entrez le numéro de puce : ")
                else:
                    puce = None

                facultatif = input("Possède-t-il un passeport ? (o/n) ")
                if facultatif == "o":
                    passeport = input("Entrez le numéro de passeport : ")
                else:
                    passeport = None

                inserer_animal(conn, nom, espece, date_naiss, puce, passeport)

            elif choix == 5:  # Insérer un médicament
                molecule = input("Entrez le nom de la molécule : ")
                effets = input("Entrez les effets du médicament : ")

                inserer_medicament(conn, molecule, effets)

            elif choix == 6:  # Insérer une entrée dans un dossier médical
                affichage_simple(conn,"animal")
                animal = input("Entrez l'id de l'animal : ")

                facultatif = input("Voulez-vous entrer une mesure de poids ? (o/n) ")
                if facultatif == "o":
                    mesure = input("Entrez la mesure de poids : ")
                    inserer_poids(conn, animal, mesure)

                facultatif = input("Voulez-vous entrer une mesure de taille ? (o/n) ")
                if facultatif == "o":
                    mesure = input("Entrez la mesure de taille : ")
                    inserer_taille(conn, animal, mesure)

                facultatif = input("Voulez-vous entrer des résultats d'analyse ? (o/n) ")
                if facultatif == "o":
                    lien = input("Entrez le lien vers les résultats d'analyse : ")
                    inserer_analyse(conn, animal, lien)

                facultatif = input("Voulez-vous entrer une observation réalisée lors d'une consultation ? (o/n) ")
                if facultatif == "o":
                    affichage_personne(conn,"Personnel")
                    personnel = input("Entrez l'id du personnel ayant réalisé l'observation : ")
                    date = input("Entrez la date à laquelle l'observation a été effectuée : ")
                    observation = input("Entrez l'observation : ")
                    inserer_consultation(conn, animal, personnel, date, observation)

                facultatif = input("Voulez-vous entrer une procédure réalisée sur le patient ? (o/n) ")
                if facultatif == "o":
                    nom = input("Entrez le nom de la procédure : ")
                    description = input("Entrez la description de la procédure : ")
                    inserer_procedure(conn, animal, nom, description)

                facultatif = input("Voulez-vous entrer un traitement pour un patient ? (o/n) ")
                if facultatif == "o":
                    affichage_veterinaire(conn)
                    veto = input("Entrez l'id du vétérinaire qui prescrit le traitement : ")
                    date_debut = input("Entrez la date de début du traitement : ")
                    duree = input("Entrez la durée du traitement : ")

                    affichage_simple(conn,"medicament")
                    medicament = input("Entrez la/les molécule/s à prescrire et leur quantite (molecule1:quantite1 molecule2:quantite2): ")


                    inserer_traitement(conn, date_debut, duree, medicament, veto, animal)

        elif choix == 2:
            print("\n1 : Lister les quantités de médicaments consommés pour une période donnée")
            print("2 : Lister le nombre de traitements prescrits au cours d'une période donnée")
            print("3 : Lister les procédures effectuées sur un animal donné, avec et triées par date")
            print("4 : Compter le nombre d'animaux traités groupés par espèce")
            print(
                "5 : Lister les animaux ayant appartenus à un client donné, triés par date d'adoption, avec le nom et prénom du client, et les informations d'identification de l'animal, sa date de naissance et son espèce")
            print(
                "6 : Lister les animaux qui appartiennent à un client donné, triés par date d'adoption, avec le nom et prénom du client, et les informations d'identification de l'animal, sa date de naissance et son espèce")
            print(
                "7 : Lister les animaux ayant appartenus mais n'appartenant plus à un client donné, triés par date d'adoption, avec le nom et prénom du client, et les informations d'identification de l'animal, sa date de naissance et son espèce")
            print("8 : Lister l'évolution de croissance taille et poids d'un animal donné, par ordre chronologique")
            print(
                "9 : Lister les traitements subis par un animal donné avec leurs dates, triés chronologiquement, sans plus de détails")
            print(
                "10 : Lister les traitements en cours pour un animal donné, avec leurs dates, avec le détail des prescriptions (médicaments et quantités par jour)")
            print(
                "11 : Lister les membres de personnel spécialisés dans les reptiles, avec leur poste et toutes leurs informations")
            print("12 : Lister les animaux ayant été suivis par un vétérinaire donné au cours du dernier mois")
            print(
                "13 : Lister les vétérinaires ayant suivi un animal donné, avec et triés par leur date de suivi le plus récent\n")
            choix = int(input("Votre choix : "))

            if choix == 1:
                date_debut = str(input("Date de début : (Y-M-J) \n"))
                date_fin = str(input("Date de fin : (Y-M-J) \n"))
                medicament_consomme_periode(conn, date_debut, date_fin)


            elif choix == 2:
                date_debut = str(input("Date de début : (Y-M-J) \n"))
                date_fin = str(input("Date de fin : (Y-M-J) \n"))
                traitement_par_periode(conn, date_debut, date_fin)


            elif choix == 3:
                nom_animal = str(input("Le nom de l'animal : \n"))
                liste_procedure_animal(conn, nom_animal)

            elif choix == 4:
                date_debut = str(input("Date de début : (Y-M-J) \n"))
                date_fin = str(input("Date de fin : (Y-M-J) \n"))
                liste_quantite_traitement(conn, date_debut, date_fin)

            elif choix == 5:
                date_debut = str(input("Date de début : (Y-M-J) \n"))
                date_fin = str(input("Date de fin : (Y-M-J) \n"))
                liste_quantite_medicament(conn, date_debut, date_fin)

            elif choix == 6:
                nb_animal_par_espece(conn)

            elif choix == 7:
                prenom_client = str(input("Le prénom de client : \n"))
                nom_client = str(input("Le nom de client : \n"))
                animal_par_client(conn, prenom_client, nom_client)

            elif choix == 8:
                taille_poids(conn)

            elif choix == 9:
                nom_animal = str(input("Le nom de l'animal : \n"))
                traitement_subi_par_animal(conn, nom_animal)

            elif choix == 10:
                nom_animal = str(input("Le nom de l'animal : \n"))
                traitement_en_cours(conn, nom_animal)

            elif choix == 11:
                membre_personnel_reptiles(conn)

            elif choix == 12:
                prenom_veto = str(input("Le prénom du véto : \n"))
                nom_veto = str(input("Le nom du véto : \n"))
                animal_suivi_par_veterinaire(conn, prenom_veto, nom_veto)

            elif choix == 13:
                nom_animal = str(input("Le nom de l'animal : \n"))
                veterinaire_suivant_un_animal(conn, nom_animal)


        else:
            continuer = False

    conn.close()


if __name__ == "__main__":
    main()
