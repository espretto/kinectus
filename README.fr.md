
Kinectus
---
Kinectus est une application de reconnaissance d'images. Plus spécifiquement, elle reconnait les signes de la main du jeu pierre-feuille-ciseaux à l'aide d'une Kinect XBOX 360. La reconnaissance repose sur le calcul de trois critères, dits features, basés sur les mesures prises à partir des signes de la main. Ces trois features constituent un point dans un espace 3D. Celles-ci sont:

1. La circularité : 4pi * surface / périmetre ^ 2
2. L'ellipticité : l'axe le plus court / l'axe le plus long
3. La convexivité : la surface convexe / la surface effective

On ne peut reconnaître ce qu'on n'a jamais vu avant. Afin de concevoir une base de référence, l'application permet d'enregistrer des points qui correspondent aux signes "pierre", "feuille" et "ciseaux". Chaque nuage de points distinct peut être considéré comme un ensemble de vecteurs de features(soit de formes). Son centroide sert de point de référence pour la reconnaissance.

Prérequis
---
L'application nécessite l'installation des logiciels suivants :

- [Kinect for Windows SDK v1.8][1]
- [Kinect for Windows Developer Toolkit v1.8][2]
- [python 2.7.14][5] (cocher l'option "ajouter au PATH")
- [Microsoft Visual C++ Compiler for Python 2.7][3] (pour compiler scikit-image)

Malheureusement, le compilateur C++ ne dispose pas du fichier `stdint.h` (voir `assets`). Copiez-le dans le dossier `%USERPROFILE%\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\include\` comme l'indique [cette réponse sur stackoverflow][4].

Installation
---
Il est recommandé d'installer les dépendences du projet dans un [environnement virtuel][7] dédié à ce dernier.
```sh
pip install virtualenvwrapper-win
mkvirtualenv --python path/to/python-2.7.14/python.exe kinectus
cd path/to/kinectus
pip install numpy # réquis par scikit-image
pip install -r requirements.txt
```

Le module `pykinect@2.1` contient une erreur. Dans le dossier de votre environnement virtuel, modifier le module `Lib/site-packages/pykinect/nui/struct.py` sur la ligne `213` : Remplacer `return desc.height.value` par `return desc.height`. [Un issue correspondant][6] a déjà été créé.

Utilisation
---
L'application offre deux scripts : `kinectus.py` et `evaluate.py`.

### Création d'une base de référence
Branchez la camera et lancez le script suivant:
```sh
python kinectus.py
```
Un fenêtre pygame va s'ouvrir et afficher le flux d'images filtrés provenant de la camera. Le filtre ne reconnait que des objets à une distance d'environ 50cm de la camera. Pour enregistrer des points de features, utiliser les touches de clavier. Montrez le signe désiré à la camera, puis appuyez sur la lettre :
- `p` pour enregistrer un pierre
- `c` pour enregistrer des ciseaux
- `f` pour enregistrer une feuille
Les données ainsi enregistrées sont écrites dans le dossier `./assets/samples`.

### Evaluer les données
Le deuxième script permet d'afficher les nuages de points précédemment enregistrés dans un système de coordonnées à trois dimensions.
```sh
python evaluate.py 
```
Pour alimenter système avec d'autres données, il faut passer le chemin à la méthode `main`.

[1]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40278
[2]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40276
[3]: https://wiki.python.org/moin/WindowsCompilers
[4]: https://stackoverflow.com/questions/44865576/python-scikit-image-install-failing-using-pip
[5]: https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
[6]: https://github.com/Microsoft/PTVS/issues/3717
[7]: https://virtualenvwrapper.readthedocs.io/en/latest/