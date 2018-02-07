

installation de l'environnement de développement
---

- installer [Kinect for Windows SDK v1.8][1]
- installer [Kinect for Windows Developer Toolkit v1.8][2]
- installer [python 2.7.14][5]
- installer [Microsoft Visual C++ Compiler for Python 2.7][3] pour pouvoir compiler `scikit-image`
- suiver les instruction sur [stackoverflow][4] pour réparer le compilateur C++

```bat
cd path/to/projet
pip install virtualenvwrapper-win
mkvirtualenv --python path/to/python-2.7.14/python.exe imagerie
pip install -r requirements
```
Corriger une erreur dans `%USERPROFILE%\Envs\imagerie\Lib\site-packages\pykinect\nui\struct.py` ligne 213 : Remplacer `return desc.height.value` par `return desc.height`.

Finalement, vous pouver executer l'application
```
start cmd /c python kinectus.py
```

[1]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40278
[2]: https://www.microsoft.com/en-us/download/confirmation.aspx?id=40276
[3]: https://wiki.python.org/moin/WindowsCompilers
[4]: https://stackoverflow.com/questions/44865576/python-scikit-image-install-failing-using-pip
[5]: https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi