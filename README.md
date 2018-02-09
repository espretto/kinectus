
Kinectus
---
Kinectus est une application de reconnaissance d'image. Plus spécifiquement, elle reconnait les signes de la main du jeu pierre-feuille-papier à l'aide d'une camera XBOX 360 Kinect. La reconnaissance repose sur le calcul de trois critères, dits features, basés sur des mesures d'une forme d'un signe de la main. Ces trois features constituent un points dans un espace 3D, car trois features:

1. La circularité : 4pi * surface / perimetre ^ 2
2. L'ellipticité : la plus courte axe / la plus longe axe
3. La convexivité : le surface convexe / le surface effectif

On ne peut reconnaître ce qu'on n'a jamais vu avant. Afin de faire de l'expérience, l'application permet d'enregistrer de points qui correspondent aux signes "pierre", "feuille" et "papier". Un groupe de vecteurs de features par forme, peut être consideré comme un nuage de points. Son centroide sert comme point de référence pour la reconnaissance.

Préréquis
---
L'application necessite l'installation des logiciels suivants :

- [Kinect for Windows SDK v1.8][1]
- [Kinect for Windows Developer Toolkit v1.8][2]
- [python 2.7.14][5] (cocher l'option "ajouter au PATH")
- [Microsoft Visual C++ Compiler for Python 2.7][3] (pour compiler scikit-image)

Malheureusement, le compilateur C++ manque le fichier `stdint.h` (voir `assets`). Copiez-le dans le dossier `%USERPROFILE%\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\include\` comme l'indique [cette réponse sur stackoverflow][4].

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

Le module `pykinect@2.1` contient une erreur. Dans le dossier de votre environnement virtuel, modifier le module `Lib/site-packages/pykinect/nui/struct.py` sur la ligne `212` : Remplacer `return desc.height.value` par `return desc.height`. [Un issue correspondant][6] a déjà été créé.

Utilisation
---
L'application offre deux scripts : `kinectus.py` et `evaluate.py`.

### Faire de l'expérience
Branchez la camera et lancer le script suivant:
```sh
python kinectus.py
```
Un fenêtre pygame va s'ouvrir et afficher le flux d'images filtrés provenant de la camera. Le filtre ne reconnait que des objets à une distance d'environ 50cm de la camera. Pour enregistrer des points de features, utiliser les touches de clavier. Montrez le signe désiré à la camera, puis appuyez sur la lettre :
- `p` pour enregistrer un pierre
- `c` pour enregistrer des ciseaux
- `f` pour enregistrer une feuille
Les données ainsi enregistrées, sont écrites dans le dossier `./assets/samples`.

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