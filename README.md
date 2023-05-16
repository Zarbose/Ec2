# Ec2
Projet de spécialité en Master 1 Informatique par Simon Pieto

### Sujet
L'application RTE-Eco2Mix permet de comprendre les productions et les consommations d'électricité en France.
Toutes les données sont accessibles en open-data, par HTTP sans avoir à lancer l'application. Le projet consiste à
parcourir les données disponibles puis simuler une STEP et en optimiser son rendement. Mots-clefs : temps-réel, opendata, bourse.


#### Pré Requis avant installation
- Docker engine
- Docker compose

### Structure du projet
Le schéma suivant représente comment s'organisent les différents services utilisés par le projet
![Structure](/image/structure.png)

### Configuration
Dans le répertoire [secrets](https://github.com/Zarbose/Ec2/tree/main/secrets) vous trouverez 3 fichiers qui vont permettre de configurer les différents services à utiliser. :
- **.env_gf**
- **.env_influxdb**
- **.env_python**

Le fichier ```.env_gf```  permet de configurer grafana
```
GF_SECURITY_ADMIN_USER=...          # Login
GF_SECURITY_ADMIN_PASSWORD=...      # Password
```
Le fichier ```.env_influxdb```  permet de configurer influxdb
```
DOCKER_INFLUXDB_INIT_USERNAME=...       # Login     
DOCKER_INFLUXDB_INIT_PASSWORD=...       # Password
```

Le fichier ```.env_python```  permet de configurer l'application web développée à l'aide du framework Django. Par défaut, il n'y a rien à modifier.

### Démarrer l'application
```bash
    docker compose up
```

L'utilisation de l'application se fait à partir des urls suivantes :
- Page de configuration des simulateur <http://localhost:8000/> 
- Page de visualisation des résultat <http://localhost:3000>
