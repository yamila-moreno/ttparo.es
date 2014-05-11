===============
Plataforma TTDP
===============

Esta documentación es una guía de instalación y actualización.

Requisitos del sistema
======================

Componentes del sistema
-----------------------

En la máquina donde vayamos a desplegar, hay que instalar los siguientes componentes:

  * Python 2.7

  * virtualenv, virtualenvwrapper

  * Pip (para instalar paquetes de python). **$ apt-get install python-pip**

  * Postgresql 9.2

  * node.js(0.10.19-1)

  * npm (curl https://npmjs.org/install.sh | sudo sh)

  * less (sudo npm install less -g)

  * R (pacman -S r)

  * gcc-fortran

Componentes del entorno virtual
-------------------------------

Además de los componentes del sistema, estos son específicos del entorno virtual y que se instalan tras la creación de éste. Si no se usa entorno virtual, entonces se instalan en el sistema. En el fichero requirements.txt están listados, con sus respectivas versiones, estos componentes del entorno virtual. Lo más operativo es instalarlos con::

    pip install -r tools/requirements.txt

Node
----

* En la carpeta `src`, ejecutamos::

    make dependences

* Tras esta operación, los sucesivos cambios se propagarán con::

    make

R
--

Tras instalar R hay que añdir algunas librerías; la más importante es MicroDatosEs (está en un repositorio oficial) que tiene algunas dependencias. Para instalar, en R, hay que abrir una consola de R::

    $ R

y dentro de esta consola, ejecutar::

    install.packages("memisc", repos= c("http://R-Forge.R-project.org", getOption("repos")))
    install.packages("Hmisc", repos= c("http://R-Forge.R-project.org", getOption("repos")))
    install.packages("MicroDatosEs", repos= c("http://R-Forge.R-project.org", getOption("repos")))


Actualización manual
--------------------

* Descargar el fichero zip de ftp://www.ine.es/temas/epa/datos_1t14.zip

* Descomprimirlo dentro de scripts/epa-raw. El script en R parseará todos los ficheros que estén en ese directorio. Si hay ficheros que ya estuvieran cargados no afecta puesto que no se cargarán de nuevo, aunque tiene coste de procesamiento.

* Hay que parsear este fichero en crudo con el script en R. Para invocarlo, primero hay que setear correctamente el working directory::

    setwd('path/to/csv')

por defecto está seteado en el directorio `epa-raw` relativo a `scripts`. Tras esto, se invoca el sript::

    R CMD BATCH leer_epa.R

Este script genera un fichero datos_epa.csv que tenemos que cargar en la bbdd.

* Para cargar el csv en la bbdd usamos el script::

    scripts/load_microdata.py /ruta/al/CSV

.. warning::

    (1) el csv debe estar en UTF-8
    (2) el csv no debe contener la primera fila con los nombres de las columnas
    (3) en este script hay que poner manualmente el nombre de la bbdd

* Para recalcular las tasas de paro, usamos el script::

    scripts/load_ratequeries.py

.. warning::

    (1) en este script hay que poner manualmente el nombre de la bbdd

* Conviene borrar tanto el fichero.zip inicial, como el raw.csv como datos_epa.csv después de que termine el proceso exitosamente.


Notas
-----

* Para descargarse todos los .zip se puede usar el script ``descarga-datos.sh`` (hay que mantenerlo actualizado)

* El script incluído en ``scripts/load_epa_data.py`` automatiza el proceso de descarga de datos, procesado en R y carga de datos. Se invoca empleando como parámetro la URL de fichero ZIP de datos de la EPA::

        python load_epa_data.py --zipfile_url ZIPFILE_URL -v

.. warning::

    (1) Este script emplea el fichero .R original (``leer_epa.R`)
    (2) Antes de ejecutar el script, hay que poner manualmente el nombre de la bbdd en los scripts ``load_microdata.py`` y ``load_ratequeries.py`` 
