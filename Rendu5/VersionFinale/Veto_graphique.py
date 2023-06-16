from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
# ATTENTION : il faut installer le package tkcalandar pour que l'appli fonctionne ("pip install tkcalendar" en console qi vous avez pip)
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime
import psycopg2 as ps


# fonction de connexion à la base de donnée
def connexion(dbname="dbnf18a029", user="nf18a029", password="Y1odKfZJ", host="tuxa.sme.utc", port="5432"):
    conn = ps.connect(host=host, database=dbname, user=user, password=password, port=port)
    return conn


class Fenetre(Tk):

    # on ajoute un objet de connexion a la bdd dans la classe fenetre
    def __init__(self):
        Tk.__init__(self)
        self.conn = connexion()

    # on modifie la fonction destroy pour que l'objet de connexion soit aussi detruit lorsqu'on ferme la fenêtre
    def destroy(self) -> None:
        self.conn.close()
        Tk.destroy(self)

    # fonction qui permet de retirer tous les éléments présents sur la fenetre qui permet de changer l'affichage sans avoir besoin d'ouvrir une nouvelle fenetre
    def effacer_tout(self):
        for widget in self.winfo_children():
            widget.destroy()

    # premier menu qui sépare les fonctions permettant d'insérer des éléments dans la bdd et celles qui permettent d'afficher des éléments de la bdd
    def fenetre_principale(self):
        self.effacer_tout()

        button1 = Button(self, text="Insérer des données", height=4, width=50, command=self.fenetre_insert)
        button2 = Button(self, text="Afficher des données", height=4, width=50, command=self.fenetre_select)
        button3 = Button(self, text="Quitter", height=4, width=50, bg="red", command=self.destroy)

        button1.grid(column=0, row=0)
        button2.grid(column=0, row=1)
        button3.grid(column=0, row=2)

    # deuxième menu avec toutes les fonctions d'insertion demandées =
    def fenetre_insert(self):
        self.effacer_tout()

        button1 = Button(self, text="Insérez un membre du personnel", height=4, width=50,
                         command=self.insertion_membre_personnel1)
        button2 = Button(self, text="Insérez un client", height=4, width=50, command=self.insertion_client1)
        button3 = Button(self, text="Insérez un propriétaire pour un animal", height=4, width=50,
                         command=self.insertion_proprietaire1)
        button4 = Button(self, text="Insérez un animal", height=4, width=50, command=self.insertion_animal1)
        button5 = Button(self, text="Insérez un médicament", height=4, width=50, command=self.insertion_medicament1)
        button6 = Button(self, text="Insérez une entrée dans un dossier médical", height=4, width=50,
                         command=self.fenetre_insert_dossier_medical)
        button7 = Button(self, text="Retour", height=4, width=50, bg="red", command=self.fenetre_principale)

        button1.grid(column=0, row=0)
        button2.grid(column=0, row=1)
        button3.grid(column=0, row=2)
        button4.grid(column=0, row=3)
        button5.grid(column=0, row=4)
        button6.grid(column=0, row=5)
        button7.grid(column=0, row=6)

    # fonction qui permet d'afficher la table renvoyée par une requete de type SELECT avec en plsu le titres des colonnes
    def afficher_table(self, requete):
        self.effacer_tout()
        cur = self.conn.cursor()

        # exécuter une requête pour récupérer les données de la table
        cur.execute(requete)
        rows = cur.fetchall()
        if len(rows) == 0:  # si la requête ne retourne aucune ligne
            messagebox.showinfo(message="Aucune donnée à afficher")
            self.fenetre_select()
        else:
            # récupérer les noms des colonnes de la table
            colnames = [desc[0] for desc in cur.description]

            # ajouter les noms des colonnes en haut de la grille
            for i, colname in enumerate(colnames):
                label = Label(self, text=colname, bg="grey65")
                label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

            # ajouter les données de la table dans la grille
            for i, row in enumerate(rows):
                for j, cell in enumerate(row):
                    label = Label(self, text=str(cell))
                    label.grid(row=i + 1, column=j)
        cur.close()
        button = Button(self, text="Retour", height=4, width=50, bg="red", command=self.fenetre_select)
        button.grid(column=0, columnspan=len(colnames), row=len(rows) + 1, sticky="nsew")

    # troisième menu avec toutes les fontion d'affichae demandées
    def fenetre_select(self):
        self.effacer_tout()

        button1 = Button(self, text="Quantités de médicaments consommés pour une période", height=4, width=50,
                         command=self.fenetre_qte_medoc1)
        button2 = Button(self, text="Nombre de traitements prescrits au cours d'une période", height=4, width=50,
                         command=self.fenetre_traitement_par_periode1)
        button3 = Button(self, text="Procédures effectuées sur un animal", height=4, width=50,
                         command=self.fenetre_procedures_animal1)
        button4 = Button(self, text="Nombre d'animaux traités groupés par espèce", height=4, width=50,
                         command=self.fenetre_animaux_par_espece)
        button5 = Button(self, text="Animaux ayant appartenus à un client", height=4, width=50,
                         command=self.fenetre_animaux_par_client1)
        button6 = Button(self, text="Animaux qui appartiennent à un client", height=4, width=50,
                         command=self.fenetre_animaux_actuel_par_client1)
        button7 = Button(self, text="Animaux ayant appartenus mais n'appartenant plus à un client", height=4, width=50,
                         command=self.fenetre_animaux_ayant_appartenu_par_client1)
        button8 = Button(self, text="Évolution de croissance taille et poids d'un animal", height=4, width=50,
                         command=self.fenetre_evolution_croissance_animal1)
        button9 = Button(self, text="Traitements subis par un animal donné", height=4, width=50,
                         command=self.fenetre_taitement_par_animal1)
        button10 = Button(self, text="Traitements en cours pour un animal", height=4, width=50,
                          command=self.fenetre_taitement_en_cours_par_animal1)
        button11 = Button(self, text="Membres de personnel spécialisés dans les reptiles", height=4, width=50,
                          command=self.fenetre_membre_specialise_reptile)
        button12 = Button(self, text="Animaux ayant été suivis \npar un vétérinaire donné au cours du dernier mois",
                          height=4, width=50, command=self.fenetre_animal_suivi_par_veterinaire1)
        button13 = Button(self, text="Vétérinaires ayant suivi un animal", height=4, width=50,
                          command=self.fenetre_veterinaire_suivant_un_animal1)
        button14 = Button(self, text="Retour", height=4, width=50, bg="red", command=self.fenetre_principale)

        button1.grid(column=0, row=0)
        button2.grid(column=0, row=1)
        button3.grid(column=0, row=2)
        button4.grid(column=0, row=3)
        button5.grid(column=0, row=4)
        button6.grid(column=0, row=5)
        button7.grid(column=0, row=6)
        button8.grid(column=1, row=0)
        button9.grid(column=1, row=1)
        button10.grid(column=1, row=2)
        button11.grid(column=1, row=3)
        button12.grid(column=1, row=4)
        button13.grid(column=1, row=5)
        button14.grid(column=1, row=6)

    # fonction intermédiaire à l'affichage des quantitées de médicaments permettant de sélectionne la periode voulue
    def fenetre_qte_medoc1(self):
        self.effacer_tout()
        self.cal1 = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.cal1.grid(column=0, row=2)
        self.cal2 = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.cal2.grid(column=1, row=2)
        lab1 = Label(self, text="Choisissez une période:")
        lab1.grid(column=0, row=0, columnspan=2)
        lab2 = Label(self, text="Date de début:")
        lab2.grid(column=0, row=1)
        lab3 = Label(self, text="Date de fin:")
        lab3.grid(column=1, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50, command=self.fenetre_qte_medoc2)
        button.grid(column=0, row=3, columnspan=2, sticky="nsew")

    # fonction qui récupère les valeurs des calendriers et crée la requete pour afficher les quantitées de médicaments puis appele afficher_table avec cette requete
    def fenetre_qte_medoc2(self):
        self.effacer_tout()
        date1 = self.cal1.get_date()
        date2 = self.cal2.get_date()
        if datetime.strptime(date1, "%Y-%m-%d") > datetime.strptime(date2, "%Y-%m-%d"):
            messagebox.showerror("Erreur", "La date de début doit être antérieure à la date de fin")
            self.fenetre_qte_medoc1()
        else:
            query = f"SELECT m.molecule, (t.duree * p.quantite * COUNT(*)) AS nombre FROM Medicament m INNER JOIN Prescrit p ON m.molecule = p.medicament INNER JOIN Traitement t ON p.traitement = t.id WHERE t.date_debut - '{date1}' > 0 AND '{date2}' - t.date_debut > t.duree GROUP BY m.molecule, t.duree, p.quantite;"
            self.afficher_table(query)

    # meme chase que les médicaments amis avec les traitements
    def fenetre_traitement_par_periode1(self):
        self.effacer_tout()
        self.cal1 = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.cal1.grid(column=0, row=2)
        self.cal2 = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.cal2.grid(column=1, row=2)
        lab1 = Label(self, text="Choisissez une période:")
        lab1.grid(column=0, row=0, columnspan=2)
        lab2 = Label(self, text="Date de début:")
        lab2.grid(column=0, row=1)
        lab3 = Label(self, text="Date de fin:")
        lab3.grid(column=1, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_traitement_par_periode2)
        button.grid(column=0, row=3, columnspan=2, sticky="nsew")

    def fenetre_traitement_par_periode2(self):
        self.effacer_tout()
        date1 = self.cal1.get_date()
        date2 = self.cal2.get_date()
        if datetime.strptime(date1, "%Y-%m-%d") > datetime.strptime(date2, "%Y-%m-%d"):
            messagebox.showerror("Erreur", "La date de début doit être antérieure à la date de fin")
            self.fenetre_traitement_par_periode1()
        else:
            query = f"SELECT COUNT(*) AS nombre_traitements FROM Traitement WHERE date_debut - '{date1}' > 0 AND '{date2}' - date_debut > duree;"
            self.afficher_table(query)

    # fonction qui récupère le nom des animaux de la base de données et les met dans une liste qui sera utilisée pour les menus déroulants (combobox)
    def get_animaux(self):
        cur = self.conn.cursor()
        cur.execute("SELECT nom FROM Animal ORDER BY nom;")
        animaux = cur.fetchall()
        cur.close()
        return animaux

    # fonction intermédiaire qui permet de sélectionner l'animal dont on veut connaitre les procédures
    def fenetre_procedures_animal1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez un animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50, command=self.fenetre_procedures_animal2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_procedures_animal2(self):
        self.effacer_tout()
        animal = self.animal.get()
        query = f"SELECT Procedure.nom, date_saisie FROM Procedure INNER JOIN Animal ON Procedure.animal = Animal.id WHERE '{animal}' = Animal.nom ORDER BY date_saisie;"
        self.afficher_table(query)

    # ici pas de paramêtre donc pas besoin de fonction intermédiaire
    def fenetre_animaux_par_espece(self):
        self.effacer_tout()
        query = f"SELECT COUNT(Animal.id) as Nombre, espece FROM Animal INNER JOIN Traitement ON Traitement.animal = Animal.id GROUP BY espece;"
        self.afficher_table(query)

    # fonction qui récupère les clients de la base de données et els met dans une liste
    def get_clients(self):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT p.nom,p.prenom FROM Client t LEFT OUTER JOIN Personne p ON t.id=p.id WHERE p.id IS NOT NULL ORDER BY p.nom;")
        clients = cur.fetchall()
        cur.close()
        return clients

    # fontion intermédiare qui fonctionne qur le même principe que les précédentes
    def fenetre_animaux_par_client1(self):
        self.effacer_tout()
        clients = self.get_clients()
        self.client = StringVar()
        self.client.set(clients[0][0] + " " + clients[0][1])
        lab1 = Label(self, text="Choisissez un client:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.client, values=clients, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50, command=self.fenetre_animaux_par_client2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_animaux_par_client2(self):
        self.effacer_tout()
        client = self.client.get().split(" ")
        query = f"SELECT Animal.nom, Animal.date_naissance, Animal.espece, Animal.puce, Animal.passeport,Appartient.date_debut,Personne.prenom,Personne.nom FROM Animal,Appartient,Personne WHERE Appartient.animal = Animal.id AND Personne.nom = '{client[0]}' AND Personne.prenom = '{client[1]}' AND Appartient.proprietaire = Personne.id;"
        self.afficher_table(query)

    def fenetre_animaux_actuel_par_client1(self):
        self.effacer_tout()
        clients = self.get_clients()
        self.client = StringVar()
        self.client.set(clients[0][0] + " " + clients[0][1])
        lab1 = Label(self, text="Choisissez un client:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.client, values=clients, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_animaux_actuel_par_client2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_animaux_actuel_par_client2(self):
        self.effacer_tout()
        client = self.client.get().split(" ")
        query = f"SELECT Animal.nom, Animal.date_naissance, Animal.espece, Animal.puce, Animal.passeport,Appartient.date_debut,Personne.prenom,Personne.nom FROM Animal,Appartient,Personne WHERE Appartient.animal = Animal.id AND Personne.nom = '{client[0]}' AND Personne.prenom = '{client[1]}' AND Appartient.proprietaire = Personne.id AND Appartient.date_fin IS NULL;"
        self.afficher_table(query)

    def fenetre_animaux_ayant_appartenu_par_client1(self):
        self.effacer_tout()
        clients = self.get_clients()
        self.client = StringVar()
        self.client.set(clients[0][0] + " " + clients[0][1])
        lab1 = Label(self, text="Choisissez un client:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.client, values=clients, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_animaux_ayant_appartenu_par_client2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_animaux_ayant_appartenu_par_client2(self):
        self.effacer_tout()
        client = self.client.get().split(" ")
        query = f"SELECT Animal.nom, Animal.date_naissance, Animal.espece, Animal.puce, Animal.passeport,Appartient.date_debut,Personne.prenom,Personne.nom FROM Animal,Appartient,Personne WHERE Appartient.animal = Animal.id AND Personne.nom = '{client[0]}' AND Personne.prenom = '{client[1]}' AND Appartient.proprietaire = Personne.id AND Appartient.date_fin IS NOT NULL;"
        self.afficher_table(query)

    def fenetre_evolution_croissance_animal1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez un animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_evolution_croissance_animal2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_evolution_croissance_animal2(self):
        self.effacer_tout()
        animal = self.animal.get()
        cur = self.conn.cursor()
        query1 = f"SELECT Poids.mesure, Poids.date_saisie FROM Animal, Poids WHERE Poids.animal = Animal.id AND '{animal}' = Animal.nom ORDER BY date_saisie;"
        cur.execute(query1)
        poids = cur.fetchall()
        lab1 = Label(self, text="Evolution du poids de l'animal:")
        lab1.grid(column=0, row=0)
        titres = ["Poids", "Date"]
        for i, colname in enumerate(titres):
            label = Label(self, text=colname, bg="grey65")
            label.grid(row=1, column=i, sticky="nsew", padx=1, pady=1)
        for i, row in enumerate(poids):
            for j, value in enumerate(row):
                label = Label(self, text=value)
                label.grid(row=i + 2, column=j, sticky="nsew", padx=1, pady=1)
        query2 = f"SELECT Taille.mesure, Taille.date_saisie FROM Animal, Taille WHERE Taille.animal = Animal.id AND '{animal}' = Animal.nom ORDER BY date_saisie;"
        cur.execute(query2)
        taille = cur.fetchall()
        lab2 = Label(self, text="Evolution de la taille de l'animal:")
        lab2.grid(column=0, row=len(poids) + 2)
        titres = ["Taille", "Date"]
        for i, colname in enumerate(titres):
            label = Label(self, text=colname, bg="grey65")
            label.grid(row=len(poids) + 3, column=i, sticky="nsew", padx=1, pady=1)
        for i, row in enumerate(taille):
            for j, value in enumerate(row):
                label = Label(self, text=value)
                label.grid(row=i + len(poids) + 4, column=j, sticky="nsew", padx=1, pady=1)
        cur.close()
        button = Button(self, text="Retour", height=4, width=50, command=self.fenetre_select, bg="red")
        button.grid(column=0, row=len(poids) + len(taille) + 4, columnspan=2, sticky="nsew")

    def fenetre_taitement_par_animal1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez un animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_taitement_par_animal2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_taitement_par_animal2(self):
        self.effacer_tout()
        animal = self.animal.get()
        query = f"SELECT Animal.nom, Prescrit.medicament, Traitement.date_debut, Traitement.duree FROM Animal, Prescrit, Traitement WHERE Prescrit.traitement = Traitement.id AND Traitement.animal = Animal.id AND Animal.nom = '{animal}' ORDER BY date_debut;"
        self.afficher_table(query)

    def fenetre_taitement_en_cours_par_animal1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez un animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_taitement_en_cours_par_animal2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_taitement_en_cours_par_animal2(self):
        animal = self.animal.get()
        query = f"SELECT P.medicament, P.quantite, T.date_debut, T.duree FROM Traitement T JOIN Animal A ON T.animal = A.id JOIN Prescrit P ON P.traitement = T.id WHERE (A.nom = '{animal}') AND ((CURRENT_DATE - T.date_debut) <= T.duree) ORDER BY T.date_debut;"
        self.afficher_table(query)

    # ici non plus, pas besoin de fonction intermédiaire par contre comme il falait ajouter le poste au titre des colones on se passe de afficher_table()
    def fenetre_membre_specialise_reptile(self):
        self.effacer_tout()
        query1 = f"SELECT p.prenom, p.nom, p.date_naissance, p.numero, p.rue, p.ville, p.code_postal, p.telephone, 'Veterinaire'as poste FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Veterinaire v ON v.id = pl.id WHERE pl.specialite = 'reptiles';"
        cur = self.conn.cursor()
        cur.execute(query1)
        veterinaires = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        query2 = f"SELECT p.prenom, p.nom, p.date_naissance, p.numero, p.rue, p.ville, p.code_postal, p.telephone, 'Assistant' AS poste FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Assistant a ON a.id = pl.id WHERE pl.specialite = 'reptiles';"
        cur.execute(query2)
        assistants = cur.fetchall()
        personnel = veterinaires + assistants
        if len(personnel) == 0:
            messagebox.showinfo(message="Aucune donnée à afficher")
            self.fenetre_select()
        else:
            for i, colname in enumerate(colnames):
                label = Label(self, text=colname, bg="grey65")
                label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

            # ajouter les données de la table dans la grille
            for i, row in enumerate(personnel):
                for j, cell in enumerate(row):
                    if j == 7:  # si c'est le numéro de téléphone
                        label = Label(self, text="0{}".format(str(cell)))  # on ajoute un zéro au début
                    else:
                        label = Label(self, text=str(cell))
                    label.grid(row=i + 1, column=j)

        cur.close()
        button = Button(self, text="Retour", height=4, width=50, bg="red", command=self.fenetre_select)
        button.grid(column=0, columnspan=len(colnames) or 1, row=len(personnel) + 1, sticky="nsew")

    # fonction qui récupère les vétérinaires de la base de données et les met dans une liste
    def get_veterinaires(self):
        query = "SELECT p.nom, p.prenom FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Veterinaire v ON v.id = pl.id;"
        cur = self.conn.cursor()
        cur.execute(query)
        veterinaires = cur.fetchall()
        cur.close()
        return veterinaires

    # fonction qui récupère les membres du personnel de la base de données et le met dans une liste
    def get_personnel(self):
        query = "SELECT p.nom, p.prenom FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id;"
        cur = self.conn.cursor()
        cur.execute(query)
        personnel = cur.fetchall()
        cur.close()
        return personnel

    def fenetre_animal_suivi_par_veterinaire1(self):
        self.effacer_tout()
        veterinaires = self.get_veterinaires()
        self.veterinaire = StringVar()
        self.veterinaire.set(veterinaires[0][0] + " " + veterinaires[0][1])
        lab1 = Label(self, text="Choisissez un veterinaire:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.veterinaire, values=veterinaires, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_animal_suivi_par_veterinaire2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_animal_suivi_par_veterinaire2(self):
        self.effacer_tout()
        veterinaire = self.veterinaire.get().split(" ")
        cur = self.conn.cursor()
        sql = f"SELECT id FROM Personne WHERE Personne.prenom = '{veterinaire[1]}' AND Personne.nom = '{veterinaire[0]}';"
        cur.execute(sql)
        raw = cur.fetchone()
        id_veto = raw[0]
        cur.close()
        query = f"SELECT a.nom, a.espece FROM Animal a INNER JOIN Suit s ON a.id = s.animal INNER JOIN Personnel pl ON pl.id = s.personnel INNER JOIN Veterinaire v ON v.id = pl.id WHERE v.id = {id_veto} AND ((s.date_fin IS NULL) OR (CURRENT_DATE - s.date_fin <= 30));"
        self.afficher_table(query)

    def fenetre_veterinaire_suivant_un_animal1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez un animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        button = Button(self, text="Valider", bg="green", height=4, width=50,
                        command=self.fenetre_veterinaire_suivant_un_animal2)
        button.grid(column=0, row=2, sticky="nsew")

    def fenetre_veterinaire_suivant_un_animal2(self):
        self.effacer_tout()
        animal = self.animal.get()
        cur = self.conn.cursor()
        sql = f"SELECT id FROM Animal WHERE Animal.nom = '{animal}'"
        cur.execute(sql)
        raw = cur.fetchone()
        id_animal = raw[0]
        cur.close()
        query = f"SELECT p.prenom, p.nom, s.date_debut, s.date_fin FROM Personne p INNER JOIN Personnel pl ON p.id = pl.id INNER JOIN Veterinaire v ON pl.id = v.id INNER JOIN Suit s ON v.id = s.personnel WHERE s.animal = {id_animal} ORDER BY s.date_debut DESC;"
        self.afficher_table(query)

    # fonction qui sera utilisée en plus de la méthode trace des StringVar de tkinter pour ajouter ddes contraintes sur els chaines de caractères dans les entry, n et le nombre maximum de caractères et vaut -1 lorsqu'il n'y a pas de limite, type permet de modicfier les caractères autotrisés dans l'entry
    def character_limit(self, entry_text, n=-1, type=None):
        s = entry_text.get()
        if type == "int":
            try:
                int(s)
            except ValueError:
                entry_text.set(entry_text.get()[:-1])
        elif type == "float":
            try:
                s = s.replace(",", ".")
                float(s)
            except ValueError:
                entry_text.set(entry_text.get()[:-1])
            else:
                entry_text.set(s.replace(",", "."))
        elif type == "alpha":
            if not s.replace("-", "").replace(" ", "").replace("'", "").isalpha(): entry_text.set(entry_text.get()[:-1])
        if len(s) > n and n != -1:
            entry_text.set(entry_text.get()[:-1])

    # comme pour les fontions d'affichage, les fontions d'insertions se font en 2 parties, on récupère les données dans un premier temps puis on vérifie les dernières conraintes et on génère et execute la requête dans un second
    def insertion_membre_personnel1(self):
        self.effacer_tout()
        self.nom = StringVar()
        self.nom.trace("w", lambda name, index, mode, sv=self.nom: self.character_limit(sv, -1, "alpha"))
        self.prenom = StringVar()
        self.prenom.trace("w", lambda name, index, mode, sv=self.prenom: self.character_limit(sv, -1, "alpha"))
        self.numero = StringVar()
        self.numero.trace("w", lambda name, index, mode, sv=self.numero: self.character_limit(sv, -1, "int"))
        self.rue = StringVar()
        self.ville = StringVar()
        self.ville.trace("w", lambda name, index, mode, sv=self.ville: self.character_limit(sv, -1, "alpha"))
        self.code_postal = StringVar()
        self.code_postal.trace("w", lambda name, index, mode, sv=self.code_postal: self.character_limit(sv, 5, "int"))
        self.telephone = StringVar()
        self.telephone.trace("w", lambda name, index, mode, sv=self.telephone: self.character_limit(sv, 10, "int"))
        self.specialite = StringVar()
        self.poste = StringVar()

        lab1 = Label(self, text="Nom:")
        lab1.grid(column=0, row=0)
        lab2 = Label(self, text="Prenom:")
        lab2.grid(column=0, row=1)
        lab3 = Label(self, text="Date de naissance:")
        lab3.grid(column=0, row=2)
        lab4 = Label(self, text="Numero de rue:")
        lab4.grid(column=0, row=3)
        lab5 = Label(self, text="Rue:")
        lab5.grid(column=0, row=4)
        lab6 = Label(self, text="Ville:")
        lab6.grid(column=0, row=5)
        lab7 = Label(self, text="Code postal:")
        lab7.grid(column=0, row=6)
        lab8 = Label(self, text="Telephone:")
        lab8.grid(column=0, row=7)
        lab9 = Label(self, text="Specialite:")
        lab9.grid(column=0, row=8)
        lab10 = Label(self, text="Poste:")
        lab10.grid(column=0, row=9)

        ent1 = Entry(self, textvariable=self.nom)
        ent1.grid(column=1, row=0)
        ent2 = Entry(self, textvariable=self.prenom)
        ent2.grid(column=1, row=1)
        ent4 = Entry(self, textvariable=self.numero)
        ent4.grid(column=1, row=3)
        ent5 = Entry(self, textvariable=self.rue)
        ent5.grid(column=1, row=4)
        ent6 = Entry(self, textvariable=self.ville)
        ent6.grid(column=1, row=5)
        ent7 = Entry(self, textvariable=self.code_postal)
        ent7.grid(column=1, row=6)
        ent8 = Entry(self, textvariable=self.telephone)
        ent8.grid(column=1, row=7)

        self.date_naissance = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date_naissance.grid(column=1, row=2)

        combo1 = Combobox(self, textvariable=self.specialite,
                          values=["félins", "canidés", "reptiles", "rongeurs", "oiseaux", "autres"], state="readonly")
        combo1.grid(column=1, row=8)

        radio1 = Radiobutton(self, text="Vétérinaire", variable=self.poste, value="Véterinaire")
        radio1.grid(column=1, row=9)
        radio2 = Radiobutton(self, text="Assistant", variable=self.poste, value="Assistant")
        radio2.grid(column=2, row=9)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50, command=self.insertion_membre_personnel2)
        button1.grid(column=0, columnspan=3, row=10, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button2.grid(column=0, columnspan=3, row=11, sticky="nsew")

    def insertion_membre_personnel2(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        datenaiss = self.date_naissance.get_date()
        numero = self.numero.get()
        rue = self.rue.get()
        ville = self.ville.get()
        codep = self.code_postal.get()
        telephone = self.telephone.get()
        specialite = self.specialite.get()
        poste = self.poste.get()

        if nom == "" or prenom == "" or datenaiss == "" or numero == "" or rue == "" or ville == "" or codep == "" or telephone == "" or specialite == "" or poste == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        if len(telephone) != 10:
            messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir 10 chiffres")
            return

        if telephone[0] != '0':
            messagebox.showerror("Erreur", "Le numéro de téléphone doit commencer par 0")
            return

        if len(codep) != 5:
            messagebox.showerror("Erreur", "Le code postal doit contenir 5 chiffres")
            return

        # insertion dans la table personne
        cur = self.conn.cursor()
        query1 = f"INSERT INTO Personne VALUES (DEFAULT, '{nom}', '{prenom}', '{datenaiss}', {numero}, '{rue}', '{ville}', {codep}, {telephone});"
        cur.execute(query1)
        self.conn.commit()

        # récupération de l'id (généré automatiquement)
        query2 = f"SELECT id FROM Personne WHERE telephone = {telephone};"
        # telephone peut etre utilisé ici pour retrouver une personne, comme la commande à lieu juste après qu'il ait été entré dans la tables, il n'aurras pas eu le temps de changer de numéro
        cur.execute(query2)
        id = cur.fetchone()[0]

        # insertion dans la table Personnel
        query3 = f"INSERT INTO Personnel VALUES ({id}, '{specialite}');"
        cur.execute(query3)
        self.conn.commit()

        if poste == "Véterinaire":
            query4 = f"INSERT INTO Veterinaire VALUES ({id});"
            cur.execute(query4)
            self.conn.commit()
        else:
            query5 = f"INSERT INTO Assistant VALUES ({id});"
            cur.execute(query5)
            self.conn.commit()

        cur.close()
        messagebox.showinfo("Succès", "Le membre du personnel a bien été ajouté")
        self.fenetre_insert()

    def insertion_client1(self):
        self.effacer_tout()
        self.nom = StringVar()
        self.nom.trace("w", lambda name, index, mode, sv=self.nom: self.character_limit(sv, -1, "alpha"))
        self.prenom = StringVar()
        self.prenom.trace("w", lambda name, index, mode, sv=self.prenom: self.character_limit(sv, -1, "alpha"))
        self.numero = StringVar()
        self.numero.trace("w", lambda name, index, mode, sv=self.numero: self.character_limit(sv, -1, "int"))
        self.rue = StringVar()
        self.ville = StringVar()
        self.ville.trace("w", lambda name, index, mode, sv=self.ville: self.character_limit(sv, -1, "alpha"))
        self.code_postal = StringVar()
        self.code_postal.trace("w", lambda name, index, mode, sv=self.code_postal: self.character_limit(sv, 5, "int"))
        self.telephone = StringVar()
        self.telephone.trace("w", lambda name, index, mode, sv=self.telephone: self.character_limit(sv, 10, "int"))

        lab1 = Label(self, text="Nom")
        lab1.grid(column=0, row=0)
        lab2 = Label(self, text="Prénom")
        lab2.grid(column=0, row=1)
        lab3 = Label(self, text="Date de naissance")
        lab3.grid(column=0, row=2)
        lab4 = Label(self, text="Numéro de rue")
        lab4.grid(column=0, row=3)
        lab5 = Label(self, text="Rue")
        lab5.grid(column=0, row=4)
        lab6 = Label(self, text="Ville")
        lab6.grid(column=0, row=5)
        lab7 = Label(self, text="Code postal")
        lab7.grid(column=0, row=6)
        lab8 = Label(self, text="Téléphone")
        lab8.grid(column=0, row=7)

        ent1 = Entry(self, textvariable=self.nom)
        ent1.grid(column=1, row=0)
        ent2 = Entry(self, textvariable=self.prenom)
        ent2.grid(column=1, row=1)
        ent4 = Entry(self, textvariable=self.numero)
        ent4.grid(column=1, row=3)
        ent5 = Entry(self, textvariable=self.rue)
        ent5.grid(column=1, row=4)
        ent6 = Entry(self, textvariable=self.ville)
        ent6.grid(column=1, row=5)
        ent7 = Entry(self, textvariable=self.code_postal)
        ent7.grid(column=1, row=6)
        ent8 = Entry(self, textvariable=self.telephone)
        ent8.grid(column=1, row=7)

        self.date_naissance = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date_naissance.grid(column=1, row=2)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50, command=self.insertion_client2)
        button1.grid(column=0, columnspan=2, row=8, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button2.grid(column=0, columnspan=2, row=9, sticky="nsew")

    def insertion_client2(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        datenaiss = self.date_naissance.get_date()
        numero = self.numero.get()
        rue = self.rue.get()
        ville = self.ville.get()
        codep = self.code_postal.get()
        telephone = self.telephone.get()

        if nom == "" or prenom == "" or datenaiss == "" or numero == "" or rue == "" or ville == "" or codep == "" or telephone == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        if len(telephone) != 10:
            messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir 10 chiffres")
            return

        if telephone[0] != '0':
            messagebox.showerror("Erreur", "Le numéro de téléphone doit commencer par 0")
            return

        if len(codep) != 5:
            messagebox.showerror("Erreur", "Le code postal doit contenir 5 chiffres")
            return

        cur = self.conn.cursor()
        query1 = f"INSERT INTO Personne VALUES (DEFAULT, '{nom}', '{prenom}', '{datenaiss}', {numero}, '{rue}', '{ville}', {codep}, {telephone});"
        cur.execute(query1)
        self.conn.commit()

        query2 = f"SELECT id FROM Personne WHERE telephone = {telephone};"
        cur.execute(query2)
        id = cur.fetchone()[0]

        query3 = f"INSERT INTO Client VALUES ({id});"
        cur.execute(query3)
        self.conn.commit()

        cur.close()
        messagebox.showinfo("Succès", "Le client a bien été ajouté")
        self.fenetre_insert()

    def insertion_proprietaire1(self):
        self.effacer_tout()
        animaux = self.get_animaux()
        self.animal = StringVar()
        self.animal.set(animaux[0][0])
        lab1 = Label(self, text="Choisissez l'animal:")
        lab1.grid(column=0, row=0)
        self.combo = Combobox(self, textvariable=self.animal, values=animaux, state="readonly")
        self.combo.grid(column=0, row=1)
        clients = self.get_clients()
        self.client = StringVar()
        self.client.set(clients[0][0] + " " + clients[0][1])
        lab2 = Label(self, text="Choisissez le propriétaire:")
        lab2.grid(column=1, row=0)
        self.combo = Combobox(self, textvariable=self.client, values=clients, state="readonly")
        self.combo.grid(column=1, row=1)

        lab3 = Label(self, text="Date d'acquisition")
        lab3.grid(column=0, row=2)

        self.date_acquisition = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date_acquisition.grid(column=1, row=2)

        lab4 = Label(self, text="Date de de séparation")
        lab4.grid(column=0, row=3)

        self.date_separation = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date_separation.grid(column=1, row=3)

        self.boxvar = IntVar()
        box1 = Checkbutton(self, text="C'est actuellemnt votre animal", variable=self.boxvar,
                           command=lambda: self.date_separation.config(
                               state="disabled" if self.boxvar.get() == 1 else "normal"))
        box1.grid(column=0, columnspan=2, row=4)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50, command=self.insertion_proprietaire2)
        button1.grid(column=0, columnspan=2, row=5, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button2.grid(column=0, columnspan=2, row=6, sticky="nsew")

    def insertion_proprietaire2(self):
        animal = self.animal.get()
        client = self.client.get()
        dateacq = self.date_acquisition.get_date()
        if self.boxvar.get() == 1:
            datesep = "NULL"
            dateacq = f"'{dateacq}'"
        else:
            datesep = self.date_separation.get_date()
            if dateacq > datesep:
                messagebox.showerror("Erreur", "La date d'acquisition doit être antérieure à la date de séparation")
                return
            datesep = f"'{datesep}'"
            dateacq = f"'{dateacq}'"
        if animal == "" or client == "" or dateacq == "" or (self.boxvar.get() == 0 and datesep == ""):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"SELECT id FROM Personne WHERE nom = '{client.split()[0]}' AND prenom = '{client.split()[1]}';"
        cur.execute(query2)
        idclient = cur.fetchone()[0]
        query3 = f"INSERT INTO Appartient VALUES ({idanimal}, {idclient},{dateacq},{datesep});"
        cur.execute(query3)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "Le propriétaire a bien été ajouté")
        self.fenetre_insert()

    # fonction qui récupère les expece et les met dans une liste
    def get_espece(self):
        cur = self.conn.cursor()
        query = "SELECT nom FROM Espece;"
        cur.execute(query)
        espece = cur.fetchall()
        cur.close()
        return espece

    def insertion_animal1(self):
        self.effacer_tout()
        self.nom = StringVar()
        self.nom.trace("w", lambda name, index, mode, sv=self.nom: self.character_limit(sv, -1, "alpha"))
        self.espece = StringVar()
        self.espece.set(self.get_espece()[0][0])
        self.date_naissance = StringVar()
        self.puce = StringVar()
        self.puce.trace("w", lambda name, index, mode, sv=self.puce: self.character_limit(sv, -1, "int"))
        self.passport = StringVar()
        self.passport.trace("w", lambda name, index, mode, sv=self.passport: self.character_limit(sv, -1, "int"))

        lab1 = Label(self, text="Nom")
        lab1.grid(column=0, row=0)
        lab2 = Label(self, text="Espèce")
        lab2.grid(column=0, row=1)
        lab3 = Label(self, text="Date de naissance (facultatif)")
        lab3.grid(column=0, row=2)
        lab4 = Label(self, text="Numéro de puce (facultatif)")
        lab4.grid(column=0, row=3)
        lab5 = Label(self, text="Numéro de passport (facultatif)")
        lab5.grid(column=0, row=4)

        ent1 = Entry(self, textvariable=self.nom)
        ent1.grid(column=1, row=0)
        self.combo = Combobox(self, textvariable=self.espece, values=self.get_espece(), state="readonly")
        self.combo.grid(column=1, row=1)
        self.date_naissance = DateEntry(self, selectmode="day", date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date_naissance.grid(column=1, row=2)
        self.boxvar = IntVar()
        box1 = Checkbutton(self, text="Date inconnue", command=lambda: self.date_naissance.configure(
            state="disabled") if self.boxvar.get() == 1 else self.date_naissance.configure(state="normal"),
                           variable=self.boxvar)
        box1.grid(column=2, row=2)
        ent4 = Entry(self, textvariable=self.puce)
        ent4.grid(column=1, row=3)
        ent5 = Entry(self, textvariable=self.passport)
        ent5.grid(column=1, row=4)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50, command=self.insertion_animal2)
        button1.grid(column=0, columnspan=3, row=5, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button2.grid(column=0, columnspan=3, row=6, sticky="nsew")

    def insertion_animal2(self):
        nom = self.nom.get()
        espece = self.espece.get()
        if self.boxvar.get() == 1:
            datenaiss = "NULL"
        else:
            datenaiss = f"\'{self.date_naissance.get_date()}\'"
        puce = self.puce.get()
        passport = self.passport.get()

        if nom == "" or espece == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        if puce == "":
            puce = "NULL"
        if passport == "":
            passport = "NULL"

        cur = self.conn.cursor()
        query1 = f"INSERT INTO Animal VALUES (DEFAULT, '{nom}', {datenaiss}, {puce}, {passport}, '{espece}');"
        cur.execute(query1)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "L'animal a bien été ajouté")
        self.fenetre_insert()

    def insertion_medicament1(self):
        self.effacer_tout()
        self.molecule = StringVar()
        self.effets = StringVar()

        lab1 = Label(self, text="Nom de la molécule")
        lab1.grid(column=0, row=0)
        lab2 = Label(self, text="Effets")
        lab2.grid(column=0, row=1)

        ent1 = Entry(self, textvariable=self.molecule)
        ent1.grid(column=1, row=0)
        ent2 = Entry(self, textvariable=self.effets)
        ent2.grid(column=1, row=1)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50, command=self.insertion_medicament2)
        button1.grid(column=0, columnspan=2, row=2, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button2.grid(column=0, columnspan=2, row=3, sticky="nsew")

    def insertion_medicament2(self):
        molecule = self.molecule.get()
        effets = self.effets.get()

        if molecule == "" or effets == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        cur = self.conn.cursor()
        query1 = f"INSERT INTO Medicament VALUES ('{molecule}','{effets}')"
        cur.execute(query1)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "Le médicament a bien été ajouté")
        self.fenetre_insert()

    # menu intermédiare pour les entrées dans un dossier médical
    def fenetre_insert_dossier_medical(self):
        self.effacer_tout()
        lab1 = Label(self, text="Nom de l'animal")
        lab1.grid(column=0, row=0)
        combobox1 = Combobox(self, values=self.get_animaux(), state="readonly")
        combobox1.bind("<<ComboboxSelected>>", lambda a: [i.configure(state="normal") for i in
                                                          [button1, button2, button3, button4, button5,
                                                           button6]] if combobox1.get() != "" else [
            i.configure(state="disabled") for i in [button1, button2, button3, button4, button5, button6]])
        combobox1.grid(column=0, row=1)

        button1 = Button(self, text="Entrer un poids", height=4, width=50, state="disabled",
                         command=lambda: self.insert_poids1(combobox1.get()))
        button1.grid(column=0, row=2, sticky="nsew")
        button2 = Button(self, text="Entrer une taille", height=4, width=50, state="disabled",
                         command=lambda: self.insert_taille1(combobox1.get()))
        button2.grid(column=0, row=3, sticky="nsew")
        button3 = Button(self, text="Entrer de resultats d'analyse", height=4, width=50, state="disabled",
                         command=lambda: self.insert_analyse1(combobox1.get()))
        button3.grid(column=0, row=4, sticky="nsew")
        button4 = Button(self, text="Entrer une consultation", height=4, width=50, state="disabled",
                         command=lambda: self.insert_consultation1(combobox1.get()))
        button4.grid(column=0, row=5, sticky="nsew")
        button5 = Button(self, text="Entrer une procedure", height=4, width=50, state="disabled",
                         command=lambda: self.insert_procedure1(combobox1.get()))
        button5.grid(column=0, row=6, sticky="nsew")
        button6 = Button(self, text="Entrer un traitement", height=4, width=50, state="disabled",
                         command=lambda: self.insert_traitement1(combobox1.get()))
        button6.grid(column=0, row=7, sticky="nsew")
        button7 = Button(self, text="Retour", height=4, width=50, command=self.fenetre_insert, bg="red")
        button7.grid(column=0, row=8, sticky="nsew")

    def insert_poids1(self, nom_animal):
        self.effacer_tout()
        self.poids = StringVar()
        self.poids.trace("w", lambda name, index, mode, sv=self.poids: self.character_limit(sv, -1, "float"))
        lab1 = Label(self, text="Poids (en kg)")
        lab1.grid(column=0, row=0)
        ent1 = Entry(self, textvariable=self.poids)
        ent1.grid(column=0, row=1)
        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_poids2(nom_animal, self.poids.get()))
        button1.grid(column=0, row=2, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, row=3, sticky="nsew")

    def insert_poids2(self, nom_animal, poids):
        if poids == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"INSERT INTO Poids VALUES (DEFAULT,'{poids}',now(),{idanimal});"
        cur.execute(query2)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "Le poids a bien été ajouté")
        self.fenetre_insert_dossier_medical()

    def insert_taille1(self, nom_animal):
        self.effacer_tout()
        self.taille = StringVar()
        self.taille.trace("w", lambda name, index, mode, sv=self.taille: self.character_limit(sv, -1, "float"))
        lab1 = Label(self, text="Taille (en mètres)")
        lab1.grid(column=0, row=0)
        ent1 = Entry(self, textvariable=self.taille)
        ent1.grid(column=0, row=1)
        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_taille2(nom_animal, self.taille.get()))
        button1.grid(column=0, row=2, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, row=3, sticky="nsew")

    def insert_taille2(self, nom_animal, taille):
        if taille == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"INSERT INTO Taille VALUES (DEFAULT,'{taille}',now(),{idanimal});"
        cur.execute(query2)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "La taille a bien été ajouté")
        self.fenetre_insert_dossier_medical()

    def insert_analyse1(self, nom_animal):
        self.effacer_tout()
        self.analyse = StringVar()
        lab1 = Label(self, text="Analyse")
        lab1.grid(column=0, row=0)
        ent1 = Entry(self, textvariable=self.analyse)
        ent1.grid(column=0, row=1)
        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_analyse2(nom_animal, self.analyse.get()))
        button1.grid(column=0, row=2, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, row=3, sticky="nsew")

    def insert_analyse2(self, nom_animal, analyse):
        if analyse == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"INSERT INTO Analyses VALUES (DEFAULT,'{analyse}',now(),{idanimal});"
        cur.execute(query2)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "L'analyse a bien été ajoutée")
        self.fenetre_insert_dossier_medical()

    def insert_consultation1(self, nom_animal):
        self.effacer_tout()
        self.consultant = StringVar()
        self.observation = StringVar()

        lab1 = Label(self, text="Consultant")
        lab1.grid(column=0, row=0)
        combo1 = Combobox(self, textvariable=self.consultant, values=self.get_personnel(), state="readonly")
        combo1.grid(column=1, row=0)
        lab2 = Label(self, text="Date")
        lab2.grid(column=0, row=1)
        self.date = DateEntry(self, date_pattern="yyyy-mm-dd", maxdate=date.today())
        self.date.grid(column=1, row=1)
        lab3 = Label(self, text="Observation (facultatif)")
        lab3.grid(column=0, row=2)
        ent1 = Entry(self, textvariable=self.observation)
        ent1.grid(column=1, row=2)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_consultation2(nom_animal, self.consultant.get().split(" "),
                                                                   self.date.get(), self.observation.get()))
        button1.grid(column=0, columnspan=2, row=3, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, columnspan=2, row=4, sticky="nsew")

    def insert_consultation2(self, nom_animal, consultant, date, observation):
        if consultant == "" or date == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        if observation == "":
            observation = "NULL"
        else:
            observation = f"'{observation}'"
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"SELECT id FROM Personne WHERE nom = '{consultant[0]}' AND prenom = '{consultant[1]}';"
        cur.execute(query2)
        idpersonnel = cur.fetchone()[0]
        query3 = f"INSERT INTO Consultation VALUES (DEFAULT,'{date}',{observation},now(),{idanimal},{idpersonnel});"
        cur.execute(query3)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "La consultation a bien été ajoutée")
        self.fenetre_insert_dossier_medical()

    def insert_procedure1(self, nom_animal):
        self.effacer_tout()
        self.procedure = StringVar()
        self.description = StringVar()

        lab1 = Label(self, text="Nom de la procédure")
        lab1.grid(column=0, row=0)
        ent1 = Entry(self, textvariable=self.procedure)
        ent1.grid(column=1, row=0)
        lab2 = Label(self, text="Description")
        lab2.grid(column=0, row=1)
        ent2 = Entry(self, textvariable=self.description)
        ent2.grid(column=1, row=1)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_procedure2(nom_animal, self.procedure.get(),
                                                                self.description.get()))
        button1.grid(column=0, columnspan=2, row=2, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, columnspan=2, row=3, sticky="nsew")

    def insert_procedure2(self, nom_animal, procedure, description):
        if procedure == "" or description == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"INSERT INTO Procedure VALUES (DEFAULT,'{procedure}','{description}',now(),{idanimal});"
        cur.execute(query2)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "La procédure a bien été ajoutée")
        self.fenetre_insert_dossier_medical()

    def insert_traitement1(self, nom_animal):
        self.effacer_tout()
        self.veterinaire = StringVar()
        self.duree = StringVar()
        self.duree.trace("w", lambda name, index, mode, sv=self.duree: self.character_limit(sv, -1, "int"))

        lab1 = Label(self, text="Date de début")
        lab1.grid(column=0, row=0)
        self.date_debut = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.date_debut.grid(column=1, row=0)
        lab2 = Label(self, text="Durée (en jours)")
        lab2.grid(column=0, row=1)
        ent1 = Entry(self, textvariable=self.duree)
        ent1.grid(column=1, row=1)
        lab3 = Label(self, text="Vétérinaire")
        lab3.grid(column=0, row=2)
        combo1 = Combobox(self, textvariable=self.veterinaire, values=self.get_veterinaires(), state="readonly")
        combo1.grid(column=1, row=2)

        button1 = Button(self, text="Valider", bg="green", height=4, width=50,
                         command=lambda: self.insert_traitement2(nom_animal, self.date_debut.get(), self.duree.get(),
                                                                 self.veterinaire.get().split(" ")))
        button1.grid(column=0, columnspan=2, row=3, sticky="nsew")
        button2 = Button(self, text="Retour", height=4, width=50, command=lambda: self.fenetre_insert_dossier_medical(),
                         bg="red")
        button2.grid(column=0, columnspan=2, row=4, sticky="nsew")

    def insert_traitement2(self, nom_animal, date_debut, duree, veterinaire):
        if date_debut == "" or duree == "" or veterinaire == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        cur = self.conn.cursor()
        query1 = f"SELECT id FROM Animal WHERE nom = '{nom_animal}';"
        cur.execute(query1)
        idanimal = cur.fetchone()[0]
        query2 = f"SELECT id FROM Personne WHERE nom = '{veterinaire[0]}' AND prenom = '{veterinaire[1]}';"
        cur.execute(query2)
        idpersonnel = cur.fetchone()[0]
        query3 = f"INSERT INTO Traitement VALUES (DEFAULT,'{date_debut}',{duree},now(),{idpersonnel},{idanimal});"
        cur.execute(query3)
        self.conn.commit()
        cur.close()
        messagebox.showinfo("Succès", "Le traitement a bien été ajouté")
        self.fenetre_insert_dossier_medical()


def main():
    fen = Fenetre()
    fen.fenetre_principale()

    fen.mainloop()


if __name__ == "__main__":
    main()
