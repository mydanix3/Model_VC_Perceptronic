# perceptronico
Modelo de Visión por Computador para estimar la posición de los objetos en la escena con la intención de servir de asistencia a personas invidentes 

#Detecció d'objectes i estimació de distàncies per a persones invidents

### Daniel Alonso Pérez 1531551
### Carlos Garay Aguinagalde 1530356

# Abstract
El nostre projecte té la finalitat de orientar a persones invidents en llocs desconeguts. Té una motivació personal i amb l’objectiu de tenir un impacte social i amb el punt fort de ser un projecte multidisciplinar. 
El projecte consta per una app, entorn cloud, i 2 models per la Visió per Computadors.
Una de les tasques més complexes era la d’estimar la profunditat dels objectes, que és un camp de la Visió per Computadors que encara no s’ha trobat una solució òptima. Per tal d'aconseguir no sobrepasar el pressupost, vam optar per un model  que ens proporciona un mapa de profunditats, a partir de una imatge 2d. Per la detecció d’objectes hem optat per un model popular com es el de YOLO, que es capaç de donar-nos bons resultat. Per tal d’adaptar aquest model al nostre caa hem optat per reentrenar el model amb imatges tretes directament del simulador i així obtenir millors resultats, a més de reentrenar-lo amb un dataset d’escales.

# Introducció

El nostre projecte té la finalitat d'orientar a persones invidents en llocs desconeguts, i facilitar el realitzar tasques que ens poden semblar quotidianes; com passejar, anar a un restaurant, a la casa d'un amic, o anar a l'oficina...
La motivació d’aquest projecte es personal, en el mon existeixen 40 milions[1] de persones cegues entre aquestes el pare d'un dels integrants del grup. Hem intentat crear un projecte que combini diferents àmbits i tingui un impacte social i millori la situació d'aquestes persones que estan en una posició desfavorable.

Els mòduls de programari del nostre projecte són:
Una aplicació mòbil.
Dues infraestructures cloud:
Una capaç de connectar una aplicació mòbil a un robot i executar els models de visió per computador.
I un altre entorn creat amb Google Cloud Platform.

La part de VC conté els següent mòduls:
Un model que genera un mapa de profunditat.
Un model que detecta els objectes.
Un mòdul que genera un àudio, amb els objectes de l'escena i les seves posicions.




Fig. 1. Escena on podem veure a l'usuari guiat pel robot com si fos un gos guia, el robot utilitza un line tracker per poder seguir un trajecte.
El nostre projecte té 2 vessants per executar els models de VC:

Una amb un robot Fig1, amb una base capaç de seguir una trajectòria indicada, moure un braç robòtic segons uns angles especificats amb l’acceleròmetre del mòbil de l’usuari, i fer fotografies amb una càmera monocular que es troba a l’extrem del braç. El motiu pel que no utilitzem un altre sistema es abaratir el cost per fer el dispositiu més accessible perquè teniem un pressupost al que cenyir-nos. Aquestes imatges seran processades en un sistema que utilitza un entorn col·lab per executar el model de Visió per Computadors, la Api de Google drive com a sistema d'emmagatzematge, i un sistema basat en sockets per a la comunicació.
L'altra manera utilitza únicament el telèfon i consta d'un entorn creat completament amb Google Cloud Platform que utilitza Cloud Storage, Cloud Function  i una Cloud Virtual Machine.

# Estat de l’art

## Estimar profunditat dels objectes.
Actualment per estimar la tridimensionalitat de una escena tenim diverses tècniques.
Visió estereoscòpica(triangulació de varies càmeres en t): Aquesta proposta és semblant a la biològica. La separació que hi ha entre els ulls ens permet observar una escena desde dos punts de vista diferents i combinant aquestes imatges podem triangular la posició dels objectes de la escena i així interpretar la profunditat d’una manera senzilla. L’inconvenient de dur a terme aquesta tasca és que ens cal dos sistemes de captació d'imatge.[2][3][4]

Visió monocular(triangulació de la mateixa càmera en t i t+1): Aquesta proposta ens diu que podem realitzar diferents fotografies del mateix objectes desde punts diferents per generar un esquema mes senzill. Hi han molt bons algorismes per obtenir la tridimensionalitat de l’escena, per exemple tenim SLAM(Simultaneous Locations and Mapping)[5] i  Multi-View Stereo[6], però aquests models tenen una restricció, els objectes de l’escena que estem observant s’han de mantenir estàtics en el temps mentres la càmera està en moviment. 

LIDAR(Laser Imaging Detection and Ranging ): És un dispositiu que permet determinar la distància des d'un emissor làser a un objecte o superfície utilitzant un feix làser premut. La distància a l'objecte es determina mesurant el temps de retard entre l'emissió del pols i la seva detecció a través del senyal reflectit. La problemàtica que porta aquest sistema es que sol ser molt costós i difícil de configurar.

Càmera tridimensional(kinect): Aquesta és una tecnologia que utilitza com sensor de profunditats la projecció de infrarrojos i el combina amb un sensor CMOS monocromo que permet al dispositiu estimar la profunditat de l’escenari. Però aquesta tecnologia té un inconvenient, que no està molt estesa i dificulta aconseguir un dataset prou estès com per generar un model. Tampoc hi ha una gran varietat d’entorns, ja que està centrat en l’ús d’interiors[7,8].

Aprenentatge de profunditat a partir de observar persones quietes: Com hem vist fins ara els mètodes existents per recuperar la profunditat de la escena són escasos. Aquest mètode està basat en dades compostes per milers de vídeos d’Internet en el qual la gent imita a maniquins, és a dir, a gent parada en diverses poses mentres una càmera recobreix l’escena. Per crear les dades d’entrenament s’ha utilitzat els models de Multi-View Stereo (MVS)[6], per tal de dissenyar un model que s’aplica a l’escena dinàmica en temps d'inferència [9]
	
## Identificar diferents objectes a l’escena.
La part d’identificació d’objectes és un camp molt estudiat dintre de la visió per computador i la intel·ligència artificial. És per aquest motiu que ja hi han molts estudis i eines al respecte.

Els sistemes de detecció d’objectes solien utilitzar classificadors o localitzadors per tal de fer la identificació. Aplicaven el model a una imatge en diverses ubicacions i tamanys i finalment, depenent d’un threshold, consideraven que es detectava un objecte si en algunes d’aquestes permutacions obtenien una puntuació alta.

Però,  fa uns anys, va sortir a la llum un projecte anomenat YOLO (You Only Look Once) [10], que tenia una forma de funcionar completament diferent. El que proposa YOLO és, en comptes de basar-nos en un sistema de classificació, fer servir una xarxa neural amb només una sola avaluació de la imatge sencera. D’aquesta manera obtenim una velocitat de processament 1000 vegades superior al paradigma anterior podent arribar a funcionar fins i tot a temps real que és justament el que necessitem.

Aquest projecte ha patit moltes actualitzacions en aquests anys més recents. Actualment ja van per la versió 5 i s’han volgut centrar, entre d’altres coses, en millorar l’accesibilitat del projecte a molta gent. Amb l’última versió amb una GPU d’alta gamma però que molta gent té a casa seva es pot executar l’algorisme en un temps decent. També l’han fet compatible amb Google Collabs facilitant el seu ús. Finalment, en la versió més recent, han afegit que es pugui fer una inferència directa de qualsevol video de YouTube passant el seu link directament.

És un model molt utilitzat i famós, per aquest motiu hi ha un munt d’informació en relació a com entrenar el model, com hem de passar les dades per a que les interpreti millor, etc. En conclusió, hi ha molta informació de cara a com utilitzar de manera adient el model.

Un altre punt és el dataset que utilitzarem per tal d’entrenar l’algorisme. La càmera amb la qual llegirem informació de l’entorn es trobarà situat a un braç robòtic el qual pot estar o al terra, o a sobre d’una taula, etc. És per aquest motiu que ens agradaria generalitzar i no agafar imatges preses només desde un cert angle. 
A kaggle hi ha un munt de datasets orientats concretament a aquest problema, però hem trobat que hi ha un dataset que és el característic d’aquest problema que és el COCO (Common Objects in Context) [11] . Després d’observar més a fons aquest dataset hem vist que conté  objectes molt interessants per a la gent invident, tals com persones, cotxes, coberts, etc. 

També hem vist un altre model anomenat YOLACT++[12], forçament inspirat el YOLO, però, en aquest cas, en comptes de fer detecció d'objectes, fa instanciació de segments, és a dir, no et retorna una capsa al voltant de l’objecte sino que directament et retorna l’àrea d’aquest. Aquest model ens resoldria molts problemes però hem vist que té un rendiment inferior i també una precisió pitjor que YOLO.

# Proposta
## Arquitectura software.


Fig. 2. Esquema que representa la arquitectura software del projecte.

La nostra aplicació té dues maneres d'executar el model de VC.

La part de l'esquerra és la que utilitza el robot.

Els components per a aquesta connexió són: l'App, la Api de Google drive, un entorn col·lab, un servidor socket i un client socket en el simulador.
L'usuari, a través de l'aplicació, especifica el moviment del robot i es pugen les dades al drive.

Quan hi hagi el fitxer al servidor, aquest enviarà les dades al robot i aquest rota els motors en la posició indicada, posteriorment capturarà una imatge i finalment s'envia al servidor i aquest el pujarà al drive.

Un entorn col·lab espera la imatge per aplicar el mòdul de Visió per computador i retornar el resultat en format àudio al drive perquè l'usuari pugui accedir a ell a partir de l'aplicació.

La part de la dreta utilitza únicament el telèfon.

Consta d'un entorn creat completament amb Google Cloud Platform- Utilitzem el Cloud Function per executar un codi encarregat d’encendre la màquina cada vegada que detecta que l'usuari envia la imatge a processar al Cloud Storage. La màquina, un cop encesa, automàticament executa el model que processa la imatge i un cop generat l'àudio, es puja al Cloud Storage i això fa que s'executi un altra funció que apaga la màquina per estalviar recursos.
## Algorítmica.

### Estimar profunditat
Per la complexitat computacional que comporta estimar les profunditats d’objectes en una escena hem decidit optar per un model que ha estat entrenat prèviament amb milers de vídeos d’Internet. El dataset que ha utilitzat s’ha extret de gent que realitzava un repte que consistia en estar parat imitant a maniquins mentre una càmera recorria l’escena. Aquest mètode és el comentat anteriorment, “Learning the Depths of Moving People by Watching Frozen People”[9] .

### Detecció d’objectes

Fig. 3. LabelImg[12] Programa per realitzar etiquetatge de imatges[12].

Com hem explicat en el segon apartat, de cara a utilitzar el YOLO[10], el que hem fet ha sigut reentrenar el model, que previamente s’ha entrenat fent servir el dataset de COCO[11].

Pensant en la seguretat dels usuaris, hem arribar a la conclusió de que un dels objectes que hauriem de prioritzar de cara a que el model pogués detectar serien escales, ja que l’usuari podria fer-se molt mal en cas de caure’s. 

Hem trobat un dataset d’escales d’aproximadament 2000 imatges que ens ha sigut molt útil. El van crear per fer un detector d’objectes i l’han deixat públic[13]. Hem reentrenat el model amb aquest model per tal de que pugui detectar-les.

També, per tal de que el model funcioni millor amb imatges preses del simulador, hem decidit crear el nostre propi dataset d’imatges. Hem pres aproximadament 100 fotografies del simulador Webots, de diferents angles i amb diferents objectes i les hem etiquetat amb un programa anomenat LabelImg.[12] Fig2 
Com eren poques imatges, hem aplicat unes tècniques de data augmentation. En concret, hem rotat les imatges de 3 maneres diferents per tal de quadruplicar el nostre dataset i fer el nostre model més robust de cara a imatges en diferents angles. 

Hem rotat les imatges a l’eix horitzontal, vertical i ambdós alhora obtenint així un dataset de quasi 400 (392) imatges.

### Generació de audio

Finalment tenim el mòdul que genera un àudio, amb els objectes de l'escena i les seves profunditats. 

Per realitzar aquesta tasca, per cada objecte que ens retorna el YOLO[10], hem volgut calcular lo desplaçat que estava l’objecte respecte la càmera en les coordenades  x,y i z. 

Per calcular les coordenades x i y de cada objecte el que hem fet ha sigut agafar el punt mitjà de les bounding box que ens retorna el model YOLO[10] i mirar respecte a la imatge quin desplaçament tenen les coordenades respecte el punt central d’aquesta. Tindrem 5 modes diferents depenent la posició de l’objecte en la coordenada X. Tindrem “molt a l’esquerra”, “a l’esquerra”, “al centre”, “a la dreta” i “molt a la dreta”. D’igual manera a l’eix de les Y, “molt amunt”, “amunt”, “al mig”, “a sota” i “molt a sota”. 

Per tal de calcular la coordenada Z farem ús de detector de profunditat. Calcularem una mitjana també amb els valors de tots els píxels a dintre de la bounding box que el detector d’objectes. En aquest cas només hi hauran tres casos, “Molt lluny”, “no molt lluny” i “a prop”.
#   Experiments, resultats i anàlisi
## Estimar distancia

Fig. 4. Imatge treta de la simulació.

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)

Fig. 5. Imatge treta per la càmera del robot i procesada pels models de VC.

Per aquest apartat visualitzem directament els resultat ja que el model utilitzat “Learning the Depths of Moving People by Watching Frozen People”[9], no permet realitzar un entrenament. En la Fig4 podem veure una captura de la simulació, i en la Fig5 el resultat, de les imatges processades pel model de profunditat i el detector d'objectes. 









## Detecció de objectes

Graf. 1. Confusion Matrix model sense entrenar amb dades de la simulació.

Graf. 2. Confusion Matrix model entrenat amb dades de la simulació.

Graf. 3. F1-score model sense entrenar amb dades de la simulació.

Graf. 4. F1-score model entrenat amb dades de la simulació.


Com podem veure al Graf 1 podem veure com YOLO sense realitzar l’entrenament amb el dataset extret del simulador, no aconsegueix tenir gaire bons resultats, en canvi al Graf.2 es el model entrenat amb dades extretes del simulador. Aconseguim molts millors resultats, fent d’aquesta manera que la confusion matrix, de quasi no encertar cap objecte, sigui capaç d’encertar una gran quantitat. 

# Conclusió

Com a conclusions podem extreure que estimar la profunditat dels objectes a partir d’una imatge encara està en desenvolupament i els resultats obtinguts, tot i que han sigut prou bons, són millorables.
Hem après a etiquetar imatges i a entrenar un model YOLO, aplicant tècnique de data augmentation i després verificant què tan bé funciona el model obtingut. Hem aconseguit millorar el seu rendiment de manera satisfactòria. 
També ens ha semblat complicat fer un model de so per estimar la posició dels objectes. Ajuntar els dos models diferents ha sigut una tasca costosa però hem pogut assolir-la correctament.
Creiem que com a punt fort hem aconseguit combinar diferents assignatures, aconseguint una solució més polivalent, per exemple fent que els models s'executin completament al cloud, i poder accedir des de diferents dispositius. 
Relacionat amb el projecte global, ens ha motivat fer un projecte ambiciós i sobretot el fet de que estigui orientat a ajudar a un grup necessitat de persones que no ho tenen tan fàcil com nosaltres en el seu dia a dia.

## Github

VC: https://github.com/mydanix3/perceptronico
Robòtica: https://github.com/fguasch/Perceptronico

# Bibliografia

[1] «En el món hi ha uns 45 milions de ciegos, i la cifra va en ument ».
OMS,2020
https://www.who.int/mediacentre/news/releases/2003/pr73/es/

[2] «Què és la visió estereoscòpica?».  
Blog de Clínica Baviera, 21-04-2017.
https://www.clinicabaviera.com/blog/bye-bye-gafasconoce-tus-ojosque-es-la-vision-estereoscopica/

[3]  «Com desenvolupar la visió estereoscòpica?». 
IMO, 13-07-2011.
https://www.imo.es/es/noticias/como-desarrollamos-la-vision-estereoscopica

[4] «Què és la visió estereoscòpica?».
 Medical Óptica Audición, 27-10-2016.
https://medicaloptica.es/blog/vision-estereoscopica/

[5] Localització i mapeig simultani (SLAM).
IEEE, 26-08-2006
https://ieeexplore.ieee.org/abstract/document/1678144

[6]Una comparació i avaluació d'algoritmes de reconstrucció estèreo multivista. 
Vision Middlebury,2006
https://vision.middlebury.edu/mview/seitz_mview_cvpr06.pdf
https://vision.middlebury.edu/mview/

[7] Assignatura de profunditat amb patrons projectats. 
Google Patents, 22-07-2014
https://patents.google.com/patent/US20100118123

[8] Tècniques d’imatge de referència per a la detecció de tridimensional.
Google Patents, 23-07-2013
https://patents.google.com/patent/US20100225746

[9]. Learning the Depths of Moving People by Watching Frozen People.
Google,2019.
https://google.github.io/mannequinchallenge/www/index.html

[10] You Only Look YOLO versió 5. 
Github, 11-03-2020.
https://github.com/ultralytics/yolov5

[11] COCO Dataset. Objectes comuns en context. 
Web COCO, 2020.
https://cocodataset.org/#home

[12]Imagel Label 
Github, 03-12-2018
https://github.com/tzutalin/labelImg.

[13]Dataset escales. 
Blog AKSHAY KULKARNI, 2019.
https://akshayk07.weebly.com/real-time-stair-detection.html


