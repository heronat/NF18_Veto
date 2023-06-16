# Note de clarification

## Utilisateurs
- Nathan Piteux
- Thomas Lepretre
- Robin Lacroix
- Valentin Corazza

## Livrables
Voici le planning des livrables à rendre :
- Dimanche 16/08 : Lien vers notre gitlab + Projet 1 (NDC + MCD v1)
- Dimanche 06/11 : Projet 2 (MCD v2 + MLD v1)
- Dimanche 13/11 : Projet 3 (MLD v2 + SQL CREATE et INSERT)
- Dimanche 04/12 : Projet 4 (Finalisation SQL, SELECT et GROUP BY, première applic. python) au lieu du 20/11
- Dimanche 08/01 : Projet 5 (Application python finalisée)
- Dimanche 15/01 : Projet 6 (NoSQL R-JSON)

Chaque livrable sera publié dans la branche main dans le dossier correspondant de notre gitlab et dans le dépot de moodle associé.
Les v2 seront mis à jour directement sur le gitlab.

## Objectif du système
Ce projet nous permet de développer une application de gestion d'une base de données d'une clinique vétérinaire. Le gestionnaire de la clinique pourra ajouter et mettre à jour la liste des personnels, des clients, des animaux traités et les médicaments utilisés. Il pourra obtenir facilement des rapports d'activité et des informations statistiques, comme les quantités de médicaments consommés, le nombre de traitement ou de procédure effectuées dans la clinique, ou encore des statistiques sur les espèces d'animaux traités.

## Détail du système
**personne** : nom, prenom, date de naissance, numero_rue, rue, ville, code_postal, téléphone (clé)
- est une classe abstraite

**client** :
- héritage de personne

**personnel** : poste (vétérinaire ou assistant), specialité (félins, canidés, reptiles, rongeurs, oiseaux, autres)
- héritage de personne
- Un personnel ne peut pas être client.
- connait une spécialité, correspondant à une catégorie (*-1)

**animal** : nom, date de naissance (peut être NULL), puce d'identification (peut être NULL), un numéro de passeport (peut être NULL)
- appartient à une liste de propriétaires, avec la période durant laquelle il était avec eux. Il peut avoir plusieurs propriétaires et un proriétaire peut avoir plusieurs animaux. (\*-\*)
- est associé à une liste de vétérinaires qui l'ont suivi, avec la période durant laquelle il a été suivi. Il peut avoir été suivi par plusieurs vétérinaires et un vétérinaire peut suivre plusieurs animaux. (\*-\*)
- appartient à une espèce. Un animal ne possède qu'une seule espèce. Une espèce est associée à plusieurs animaux. (\*-1)

**espèce** : nom (clé), categorie (félins, canidés, reptiles, rongeurs, oiseaux, autres)
- est incluse dans une catégorie. Une espèce est incluse dans une seule catégorie. Une catégorie peut inclure plusieurs espèces. (*-1)

**dossier médical** :
- l'animal concerné pèse un poids (1-\*)
- l'animal concerné mesure une taille (1-\*)
- comprend des consultations (1-\*)
- l'animal concerné suit un traitement (1-\*)
- contient une analyse (1-\*)
- suit une procédure (1-\*)
- Un dossier médical est associé à un unique animal. Un animal possède un seul dossier médical. (1-1)
- Un dossier médical est modifié par un vétérinaire

**poids** : mesure, date_saisie

**taille** : mesure, date_saisie

**consultation** : date, observation, date_saisie
- est réalisée par un personnel. (\*-1)

**traitement** : date_début, durée, date_saisie
- ne peut être prescrit que par un vétérinaire
- comprend un ou plusieurs médicaments (\*-\*), avec la quantité à prendre par jour, pour chaque médicament

**analyse**: lien, date_saisie

**procédure** : nom, description, date_saisie

**médicament** : nom(clé), effets
- Il peut être autorisé pour plusieurs espèces. Une espèce peut prendre plusieurs médicaments. (\*-\*)
- Plusieurs médicaments peuvent être prescrits pour un seul traitement. Un même médicament peut apparaître dans plusieurs traitements.(\*-\*)

## Opérations que les utilisateurs pourront effectuer
Le gestionnaire de la clinique peut ajouter et mettre à jour :
- la liste des personnels
- la liste des clients
- la liste des animaux traités
- les médicaments utilisés
    
Il peut aussi obtenir facilement des rapports d'activité et des informations statistiques sur :
- les quantités de médicaments consommés
- le nombre de traitement ou de procédure effectuées dans la clinique
- les espèces d'animaux traités

Les personnels soignants peuvent ajouter, consulter et mettre à jour :
- la liste des clients
- les dossiers médicaux


