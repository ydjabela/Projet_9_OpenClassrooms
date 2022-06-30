## Projet 9 OpenClassrooms
## Développez une application Web en utilisant Django

###Description du projet :
l'objectif est de commercialiser un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

### Récupérer le projet :

```
git clone https://github.com/ydjabela/Projet_9_Openclassrooms
```

### Création de l'environnement virtuel

Assurez-vous d'avoir installé python et de pouvoir y accéder via votre terminal, en ligne de commande.

Si ce n'est pas le cas : https://www.python.org/downloads/

```
python -m venv Projet_9
```

### Activation de l'environnement virtuel du projet

Windows :

```
Projet_9\Scripts\activate.bat
```

MacOS/Linux :
```
source Projet_9/bin/activate
```

### Installation des packages necessaire pour ce projet
```
pip install -r requirements.txt
```

### Fonctionnement:
Une fois activé, pour démarrer le serveur local, il faudra utiliser la commande :
```
python manage.py runserver 
```
Accéder au site
Il suffit d'entrer l'url du serveur local dans votre navigateur, dans mon cas http://127.0.0.1:8000/
Un utilisateur devra pouvoir :
- se connecter et s’inscrire – le site ne doit pas être accessible à un utilisateur non connecté 
- consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'il suit, classés par ordre chronologique, les plus récents en premier ; 
- créer de nouveaux tickets pour demander une critique sur un livre/article ;
- créer des critiques en réponse à des tickets ;
- créer des critiques qui ne sont pas en réponse à un ticket. Dans le cadre d'un processus en une étape, l'utilisateur créera un ticket puis un commentaire en réponse à son propre ticket ;
- voir, modifier et supprimer ses propres tickets et commentaires ; 
- suivre les autres utilisateurs en entrant leur nom d'utilisateur ;
- voir qui il suit et suivre qui il veut ; 
- cesser de suivre un utilisateur


#### Cette commande sera obligatoire à chaque fois que vous voudrez travailler avec le cours. Dans le même terminal, tapez maintenant
```
pip install -r requirements.txt
```
###Vérifier la qualité du code :
Pour lancer la vérification de la qualité du code : 
```
flake8 --format=html --htmldir=flake-report --exclude=env --max-line-length=119
```
### Contributeurs
- Yacine Djabela 
- Stephane Didier

