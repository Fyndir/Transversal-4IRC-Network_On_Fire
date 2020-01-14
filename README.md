# Projet Transversal 4IRC

Membres : 
* Antoine Gamain (https://github.com/Fyndir)
* Tom Blanchet (https://github.com/frontBOI)
* léo Meynet (https://github.com/Neexos)
* Lucas Philippe (https://github.com/Tenebry)

## Contexte

Ce projet consiste à simuler des incendies sur une ville, et leur prise en charge par les flottes d’urgence qui vont intervenir.

le projet se découpe en plusieurs briques : 

* Le réseau Virtuel (https://github.com/Fyndir/Transversal-4IRC-Network_On_Fire):

Le but de cette brique est de recreer l'environnement informatique des casernes avec des LAN virtuel interconnecté via une backbone. C'est depuis des VM branchées sur ce réseau que l'on peux accèder à l'ensemble des services.

* Le centre de simulation (https://github.com/Fyndir/Transversal-4IRC-JavaSimulation) : 

Son rôle est de générer des feux dont les coordonnées, l’intensité et la fréquence sont à définir dans le programme. Ces données sont par la site transmit au serveur Flash de simulation à l'aide d'une API mise à disposition par le dit serveur.
Par la site la gestion des déplacements des camions sera également gérer par ce programme et sera envoyée sur le serveur de l'emergencyManager à l'aide d'une API mis à disposition par celui-ci.

* Le serveur de simulation (https://github.com/Fyndir/FireSimulation) :

Son role est d'afficher la simulation en temps réel pour voir l'état des feu sur une map. Il permet également de récuper les données à un instant T grace a une URL qui renvoi les données sous un format prédéfinies.

* La brique IOT (https://github.com/Fyndir/Transversal-4IRC-IOT):

Son role est de transmettre les information du serveur de simulation au serveur d'emergency manager à l'aide de deux microcontrolleur , 2 rasberry et d'APIs devellopées sur les deux serveurs.

* Le serveur Emergency Manager (https://github.com/Fyndir/Transversal-4IRC-EmergencyManager):

Son role est d'inserer les données qu'il recoit dans la base de données à l'aide d'API. Il permet également d'afficher en temps réel le contenu de la base (feu / déplacement des camions)

* La base de données de l'emergency Manager (https://github.com/Fyndir/Transversal-4IRC-BddEmergencyManager)): 

Son role est de stocker les données des feux et d'affecté les camions au dit feux à l'aide d'un ensemble de trigger SQL

## Le  réseau Virtuel

### Fonctionnement

Les technologies réseau mis en oeuvre sur les routeurs :
  - **configuration IP** : configuration basique des équipements réseau via leurs adresses IP uniques et le masques permettant de définir les différent sous-réseau.
  - **OSPF** : Open Shortest Path First, un protocol de routage mis en place dans la backbone et ne servant qu'a annoncer les différents sous-réseau de l'Autonomous System BGP. Les interfaces étant connectés à un autre AS sont passé en passive et ne participerons pas à l'OSPF.
  - **BGP** : Border Gateway Protocol est un protocol de routage permettant une forte redondance 
    - **IBGP**: les voisins IBGP sont les routeur du même AS, on utilise l'attribut next-hop self et update-source loopback
    - **EBGP**: les voisins EBGP sont les routeurs d'un autre AS, dans notre cas le ou les routeur des casernes. On utilise l'attribut multihop et remote-private AS pour la balance de charge sur des interconnexion avec multiple lien et pour palier au problème d'un AS diviser sur plusieurs LAN.
    - **peer-group**: un "objet" servant à factorier le code BGP via un template, j'ai définis un template EBGP et IBGP contennant les commandes habituels.
    - **route reflector**: route reflector est une technologie permetant de mettre en place un "serveur" BGP et donc de ne pas recourir à une topologie full mesh (en IBGP une route IBGP n'est pas retranmise pour éviter les boucle), on factorise le code correspondant à BGP.
  - **ACL**: Filtrage du traffic entrant et sortant sur internet et sur le LAN datacenter via des règles définis
  - **routage**: 
  - **VRRP**: Virtual Rouder Redondancy Protocol, mis en place sur le LAN 2, il permet d'assurer une redondance des routeurs via une adresse IP virtuel unique connus des hôtes.
 
 Les technologies mis en oeuvre sur l'infrastructure virtuel : 
  - **Serveurs** : L'intégralité des serveurs de production sont externalisés dans le cloud Azure : simulation & emergency_manager
  - **DHCP** : Seul serveur local, présent dans la caserne "data-center", et servant à octroyer des IP dynamiquement aux hôtes dans tout les LAN des casernes.
  - **Client** : VM MXLinux sous VirtualBox, elle peux joindre les autres casernes et sortir sur internet pour accèder a l'emergency manager.

 Les technologies de templating des LAN de casernes :
  - **Template JINJA**: Fichier de template faisant appel aux variables définis dans le fichier data.yaml. 
  - **Fichier Python**: Fichier de compilation et de "rendu" du template.
  - **Fichier DATA YAML**: Fichier dictionnaire de données à remplir par l'administrateur réseau avec les informations nécessaire au déploiement.

![schéma_réseau](https://github.com/Tenebry/Network_On_Fire/blob/master/Capture.PNG)
