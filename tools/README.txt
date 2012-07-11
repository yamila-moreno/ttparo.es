Para completar la instalación del entorno:

1. Instalar nodejs
2. Instalar npm: curl http://npmjs.org/install.sh | sudo sh
3. Instalar less: sudo npm install less -g
4. Instalar tools/requirements.txt (con pip)


Para poner en marcha el entorno:

src/$: python manage.py reset --csv=/ruta/al/CSV
(1) el csv DEBE estar en UTF-8
(2) el csv NO DEBE contener la primera fila con los nombres de las columnas
