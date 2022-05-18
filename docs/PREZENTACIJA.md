---
marp: true
theme: default
---
# DORS/CLUC 2022
## Kako pomoću otvorenih kockica napraviti robustan sustav u svijetu kontejnera
Albert Novak https://github.com/anovak006/dc2022
albert.novak@carnet.hr

---
# Kontejneri nasuprot virtualnim poslužiteljima
![Kontejneri nasuprot virtualnim poslužiteljima](https://www.docker.com/wp-content/uploads/Blog.-Are-containers-..VM-Image-1-1024x435.png)
Izvor: https://www.docker.com/blog/containers-replacing-virtual-machines/

---
# Kontejner u virtualnom poslužitelju

![w:700](https://www.docker.com/wp-content/uploads/Are-containers-..-vms-image-2-1024x759.png)
Izvor: https://www.docker.com/blog/containers-replacing-virtual-machines/

---
# Instalirajmo potrebne alate
### VS Code - https://code.visualstudio.com/docs/setup/linux
```shell
sudo apt install ./code_*.deb
```

### Docker
```shell
# sudo apt install docker.io
```
Ne koristiti snap verziju!

---
# Podesiti adresni prostor

```shell
# vi /etc/docker/daemon.json
{
  "default-address-pools":
  [
    {"base":"172.18.0.0/16","size":24}
  ]
}
# systemctl restart docker
```

---
### Docker Compose - https://docs.docker.com/compose/install/
```shell
$ DOCKER_CONFIG=$DOCKER_CONFIG:-$HOME/.docker}
$ mkdir -p $DOCKER_CONFIG/cli-plugins
$ curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 \
-o $DOCKER_CONFIG/cli-plugins/docker-compose
```
```shell
 $ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
 # Ako je umjesto $HOME /usr/local/lib/
 $ sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
 ```
---
# Preuzmimo projektnu razvojnu okolinu
```shell
> git clone https://github.com/anovak006/dc2022.git
```
## I vratimo se na početak
```shell
$ git checkout 8a9467879e536
```
I automatizirajmo pomicanje unaprijed
```shell
$ git config --local alias.child-sha "!git rev-list HEAD..main | tail -n 1"
$ git checkout $(git child-sha)
```
---
# Visual Studio Code - remote plugin
![alt](https://code.visualstudio.com/assets/docs/remote/containers/architecture-containers.png)

---
# Podesiti remote plugin
## Ukoliko koristimo samo jedan kontejner
Urediti potrebne postavke u datoteci `.devcontainer/devcontainer.json`
## Ukoliko radimo istovremeno s više kontejnera
Urediti potrebne postavke u datoteci `container-1/.devcontainer.json`
## Ostale postavke VS Code
Nalaze se u direktoriju `.vscode`

<!-- _footer: 1. Debug containerized apps https://code.visualstudio.com/docs/containers/debug-common <br> 2. Multiple Containers - https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers -->
---
# Slojevi slike kontejnera
![alt](https://cdn.buttercms.com/CLQJN3yRRcS7oGqm7yKb)
Izvor: https://www.metricfire.com/blog/how-to-build-optimal-docker-images/

---
# Višestupanjska (multi-stage) slika kontejnera
![alt](https://cdn.buttercms.com/PpIR4HUFTuSMirdt5pxC)
Izvor: https://www.metricfire.com/blog/how-to-build-optimal-docker-images/

---
# Priprema kontejnera

## Kroz terminal
```shell
# Napravi novi kontejner
$ docker build -t dcapi:latest -f Dockerfile.dcapi .
# Napravi novi kontejner specifičnog stupnja (stage)
$ docker build --target dcapi-dev -t dcapi-dev:latest -f Dockerfile.dcapi .
```

## Kroz VS Code

F1 pa odabrati `Remote-Containers: Rebuild and Reopen in Container `
Izvor: https://code.visualstudio.com/docs/remote/create-dev-container

<!-- _footer: `git checkout ede3fed2b00cd`-->
---
# FastAPI - RESTful API u par linija koda
![HTTP Methods](https://ws.apms.io/api/_files/WScS4PCt2atRRbGB8YUCE8/download/)
Izvor: https://appmaster.io/blog/what-rest-api-and-how-it-differs-other-types


---
# I malo složeniji primjer s elementima CRUD-a
## Dodat ćemo i jedan FastAPI router da bude zanimljivije

<!-- _footer: `git checkout 8e4c4534f0cc7`-->

---
# A kako da pristupim kontejnerima izvana?
## Traži se proxy - Traefik
![Traefik architecture w:640](https://traefik.io/static/83ea42c9e8101dcf2a16f380fe3aac08/053ba/diagram.webp)
Izvor: https://traefik.io/traefik/

---
# TLS kako postaviti certifikat
```shell
$ openssl req -x509 -out dc2022.crt -keyout dc2022.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=dc2022.dorscluc.org' -extensions EXT -config <( \
   printf "[dn]\nCN=dc2022.dorscluc.org\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:dc2022.dorscluc.org\nke<br> `git checkout d2a84d47b1ccf`yUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```
```shell
# vi /etc/hosts
127.0.0.1 dc2022.dorscluc.org
```
`git checkout d2a84d47b1ccf`
<!-- _footer: 1. Traefik TLS101 - https://traefik.io/blog/traefik-2-tls-101-23b4fbee81f1/<br>2. Selfsigned certificte - https://letsencrypt.org/docs/certificates-for-localhost/ 
-->

---
# Dodajmo sada bazu podataka
- Dodajmo novi kontejner u docker-compose.yml i stavimo ga u zasebnu mrežu
- Dodajmo SqlAlchemy ORM model baze podataka
- Rebuildajmo kontejnere
- Inicijalizirajmo Alembic `$ alembic init alembic`
<!-- _footer: `git checkout e73572cfec606` -->

---
# Podesimo Alembic - vi alembic/env.py
```python
# Add config from ENV
import os
import sys

# Add parenth dir to path
sys.path = ['', '..'] + sys.path[1:]

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db = os.environ["POSTGRES_DB"]
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (f"postgresql://{user}:{password}"
                           f"@udata_db_1/{db}")
...
# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
...
from dcdb import models
target_metadata = models.Base.metadata
```

<!-- _footer: `git checkout e52ed46534020` -->
---
# Rad s bazom
## Inicijalizacija i promjene baze
```shell
# Revizija baze u odnosu na ORM model
$ alembic revision --autogenerate -m "Init DB"
# Upgrade baze
$ alembic upgrade head
# Downgrade baze korak unazad
$ alembic downgrade -1
# Downgrade baze na početak
$ alembic downgrade base
```
## Backup i restore baze
```shell
# Backup
$ docker exec -it dors2022_db_1 pg_dumpall -c -U dors| gzip -9 > backups/cluc_dumpall_`date +%d-%m-%Y"_"%H_%M_%S`.sql.gz
# Restore
$ $ cat backups/cluc_dumpall_18-05-2022_08_30_00.sql.gz | gunzip | docker exec -i dors2022_db_1 psql -U dors -d postgres
# Delete
docker exec -it dors2022_db_1 psql -U dors -d postgres -c "DROP DATABASE IF EXISTS cluc"
```
---
# Povezivanje RESTful API-a s bazom podataka
## Kreirajmo sudionika u bazi podataka
- Podesimo konektor prema kontejneru s bazom podataka
- Kreirajmo pmoćnu funkciju sa sesijom prema bazi podataka
- Dodajmo API prema bazi podataka i povežimo API s RESTful-om
<!-- _footer: `git checkout 266719b728406` -->
---
# Prilagodi ostatak RESTful API-a pohrani sudionika u bazi podataka
- Kreiraj validaciju izlaznih podataka i dodaj model podataka u OpenAPI
- Paziti na redosljed kreiranja fukncija RESTful API-a

<!-- _footer: `git checkout 266719b728406` -->
---
# Dodaj bazi ekstenziju pg_trgm
- U alembic version datoteci ručno dodaj kod za dodavanje i uklanjanje ekstenzije kod primjene alembic revizije
<!-- _footer: `git checkout 953ef57abcf92` -->
---
# Asinkrono izvođenje zahtjevnih zadataka
![Celery Architecture](https://www.cloudamqp.com/img/blog/celery-rabbitmq.png)

Izvor: https://www.cloudamqp.com/blog/how-to-run-celery-with-rabbitmq.html

---
# Napravimo pripremu za Celery - dodajmo Redis i RabbitMQ u kontejnerima
<!-- _footer: `git checkout d70f2b71735bd` -->
---
# Dodajmo worker za "teške" poslove i RESTful API prema njemu
<!-- _footer: `git checkout 266c9e1b90a12` -->
---
# Dodajmo RESTful API prema Redisu
<!-- _footer: `git checkout 266c9e1b90a12` -->
---
# Sve što sam još mislio, ali nije stalo u ovu radionicu
- SSG (Static Site Generator)
https://about.gitlab.com/blog/2022/04/18/comparing-static-site-generators/
- SPA (Single Page Application)
https://aurelia.io/
---
# Ova prezentacija je izrađena kao kod
https://github.com/anovak006/dc2022/blob/main/docs/PREZENTACIJA.md
## Korišten je Marp
https://marp.app/

## Nažalost Marp ne podržava Mermaid
https://mermaid-js.github.io/
Pomoču kojega možete napraviti super grafove

---
# Hvala svima koji na bilo koji način doprinose otvorenom kodu jer bez njih svijet bi bio nezamislivo drugačije mjesto!
https://www.wired.com/insights/2013/07/in-a-world-without-open-source/

---
# DC2022 Singe Page Application - dcspa

## Prvo treba instalirati noviju verziju node.js
Za instlaciju ćemohttps://aurelia.io/ koristiti nvm (Node Version Manager)
```shell
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
$ source ~/.bashrc
# Lista svih dostupnih verzija
$ nvm list-remote
# Instalacija zadnje LTS verzije
$ nvm install lts/gallium
$ node -v
```
---
# DC2022 Singe Page Application - dcspa

## Instalirati ćemo Aurelia framework (aurelia.io)

```shell
$ npx makes aurelia
makes v3.0.2 https://makes.js.org
[makes] Using remote skeleton github:aurelia/new
[makes] Fetching tarball https://codeload.github.com/aurelia/new/tar.gz/master

         #
      ######   xxx
     ########  xxxx   ####         _                  _ _         ____
   x   ########    ########       / \  _   _ _ __ ___| (_) __ _  |___ \
     x  ######  #############    / _ \| | | | '__/ _ \ | |/ _` |   __) |
  xxxxx  ##  ###############    / ___ \ |_| | | |  __/ | | (_| |  / __/
   xxxxx  ###############      /_/   \_\__,_|_|  \___|_|_|\__,_| |_____|
    x ###############  xxx
    ##############  #   xx
 ##############  ######          https://aurelia.io
  ########## x  ########         https://github.com/aurelia
    #####  xxxx   ########       https://twitter.com/aureliaeffect
     #   x  x      ######
                     #

✔ Please name this new project: › dcspa
✔ Would you like to use the default setup or customize your choices? › Default TypeScript Aurelia 2 App
[makes] Project dcspa has been created.
✔ Do you want to install npm dependencies now? › Yes, use npm
```
