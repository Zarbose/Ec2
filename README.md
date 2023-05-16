# Ec2
Projet de spécialité en Master 1 Informatique par Simon Pieto

### Sujet
L'application RTE-Eco2Mix permet de comprendre les productions et les consommations d'électricité en France.
Toutes les données sont accessibles en open-data, par HTTP sans avoir à lancer l'application. Le projet consiste à
parcourir les données disponibles puis simuler une STEP et en optimiser son rendement. Mots-clefs : temps-réel, opendata, bourse.


#### Prérequis avant instalation
- Docker engine
- Docker compose

### Structure du projet
![Structure](/image/structure.png)

### Configuration
Dans le repertoire [secrets](https://github.com/Zarbose/Ec2/tree/main/secrets) vous trouverez trois fichier qui von permetre de configurer les différent service utiliser :
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

Le fichier ```.env_python```  permet de configurer l'application web déveuloper a l'aide du framework Django. Par defaut il n'y a rien a modifier

### Démarer l'application
```bash
    docker compose up
```

L'utilisation de l'application se fait a partir des urls suivant :
- Page de configuration des simulateur <http://localhost:8000/> 
- Page de visualisation des résultat <http://localhost:3000>
