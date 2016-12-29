# votes_master
Appli web pour gestion des votes des projets master

Créer la base MySQL avec le fichier votes_master.sql
Changer les informations de connexion à la base au début du fichier controller.py au niveau de la ligne con = mdb.connect

- Pour lancer l'application : export FLASK_APP=controller.py
- Puis : flask run
- Pour activer le mode débug :  export FLASK_DEBUG=1

La gestion des démos/posters n'est pas visible dans le menu mais est accessible via les urls suivantes :
- /add_demo
- /add_poster