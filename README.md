# DORS/CLUC 2022: Kako pomoću otvorenih kockica napraviti robustan sustav u svijetu kontejnera

Danas živimo u svijetu koji se brzo mijenja i u kojem se očekuju brzi rezultati, živimo agilne živote. Pri tome se očekuje da gradimo stabilne i skalabilne sustave koje će uz to biti jednostavno i održavati. Mudro je ne kretati ispočetka i prigrliti što više gotovih stvari i od njih slagati složene cjeline, a ako se pri tome koristimo otvorenim tehnologijama i standardima onda smo korak bliže našem cilju. Više svoj kod ne dijelimo kroz pakete već kontejnere pa svoj razvoj i produkciju moramo prilagoditi tom svijetu. Ako se pitate kako započeti razvoj u tom svijetu i ne otkrivati sve ispočetka onda je ovo radionica za vas.

U radionici će se pokazati kako razvijati i debugirati backend i frontend u kontejnerima, kako od kontejnera složiti funkcionalnu cjelinu i kako svoj kod u kontejnerima prilagoditi produkciji i pri tome vas pomalo uvesti u DevOps svijet. Koristit ćemo Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, RabbitMQ, Treafik i nezaobilazni javascript/typescript (neki framework kao npr. [aurelia.io](http://aurelia.io/)) ako želimo imati i neki frontend. A sve to ćemo kodirati i debugirati korištenjem VS Code.

# Postavljanje razvojne okoline

## Razvojna okolina

Razvojna okolina prilagođena je razvoju u kontejnerima. Za razvoj se koristiti Visual Studio Code zajedno s ekstenzijom Remote-Containers koja olakšava razvoj i testiranje u kontejnerima. Više o Remote-Container ekstenziji i razvoju koda u kontejneru možete naći u članku [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers).

### Priprema kontejnerske okoline

Za razvoj se koriste kontejneri i docker. Da bi se uspostavila razvojna okolina potrebno je instalirati docker ili sličan kontejnerski sustav. Ovdje je **važno** napomenuti da nije podržana snap verzija dockera zbog nemogućnosti pristupa [home direktoriju](https://github.com/microsoft/vscode-remote-release/issues/2817). Docker dolazi s početno definiranim opsegom mreža /16 što je previše za razvojnu okolinu te je preporuka da istu smanjimo na /24. Na linux sustavima treba kreirati ili urediti datoteku /etc/docker/daemon.json u kome će se postaviti željeni mrežni raspon.

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

Ukoliko imate od ranije kreirane docker mreže potrebno je iste obrisati prije promjene ospega adresnog prostora zbog mogućih preklapanja istih što će dovesti do poteškoća prilikom podizanja docker servisa.

```shell
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
baf620f8f015   bridge    bridge    local
ec40fa749265   host      host      local
0937386ff5c7   none      null      local
9ce001177c4e   proxy     bridge    local
$ docker network rm proxy
```
