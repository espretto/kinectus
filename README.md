
Kinectus
---
Kinectus is an image recognition application. It is capable of recognizing the hand-signs rock, paper, scissors within an image. The algorithm is based on an experience/reference model. The feature-vector is composed of the following geometric measurements:

1. circularity : 4pi * surface / perimeter ^ 2
2. ellipticity : shortest axis / longest axis
3. convexivity : convex surface / effective surface

In order to create a reference database, the application allows to store measurements for each hand-sign. Collectively, these measurements form clouds of points in 3d-space (3-feature-vectors). Each cloud's centroid is then used as a reference point for sign recognition, more specifically, the euclidian distance to it.

A video demonstration of the application can be found here [./assets/samples.wmv](assets/samples.wmv).

Prerequisites
---
The application needs the following programs to be installed:

- [Kinect for Windows SDK v1.8][1]
- [Kinect for Windows Developer Toolkit v1.8][2]
- [python 2.7.14][5] (tick the option "add to PATH")
- [Microsoft Visual C++ Compiler for Python 2.7][3] (in order to compile scikit-image)

Unfortunately, the C++ compiler is missing a header file. For convenience it is included in this repository at `assets/stdint.h`. Copy it to the directory `%USERPROFILE%\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\include\` as suggested by [this answer on stackoverflow][4].

Installation
---
It is recommended to install the dependencies in a python [virtual environnement][7]
```sh
pip install virtualenvwrapper-win
mkvirtualenv --python path/to/python-2.7.14/python.exe kinectus
cd path/to/kinectus
pip install numpy # required by scikit-image
pip install -r requirements.txt
```

The module `pykinect@2.1` contains an error. To correct it, change the file `Lib/site-packages/pykinect/nui/struct.py` on line `213`: replace `return desc.height.value` by `return desc.height`. [An issue][6] has already been created.

Usage
---
The application has two entrypoints: `kinectus.py` and `evaluate.py`.

### Create a reference database
In order to record samples the camera Kinect XBOX 360 was used. Connect it and run the following script:
```sh
python kinectus.py
```
A `pygame` window opens up and shows the current video stream. It is filtered to only show objects at a close distance of about 50cm. In order to store the measurements, use the given keyboard shortcuts. Show the desired hand-sign in front of the camera and hit the corresponding key (the original version is french, hence no good matches):
- `p` for rock
- `c` for scissors
- `f` for paper 
Data is stored to `./assets/samples.csv`.

### Evaluation
The second script allows to show the dot-clouds previously stored to disk in a 3d-coordinate system.
```sh
python evaluate.py 
```
In order to load a different dataset, you currently need to modify the the `main` method or replace the file `assets/samples.csv`.

[1]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40278
[2]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40276
[3]: https://wiki.python.org/moin/WindowsCompilers
[4]: https://stackoverflow.com/questions/44865576/python-scikit-image-install-failing-using-pip
[5]: https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi
[6]: https://github.com/Microsoft/PTVS/issues/3717
[7]: https://virtualenvwrapper.readthedocs.io/en/latest/