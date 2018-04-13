# Curso Udemy: REST API con Flask y Python

##Descripción
Repositorio con el código creado durante dicho curso.
Lo adaptaremos para utilizarlo con Apache y mod_wsgi
en un entorno Ubuntu Server 16.04. Utilizaremos una
base de datos Postgresql.
##Instalación
Instalar el entorno de ejecución miniconda y generar el entorno virtual para Flask con:
```
conda env create -f py3visenv.yml
```
##Modo de ejecución (Linux):
Activar el entorno virtual Python con las librerias que hemos instalado:
```
source activate py3visenv
```
situarnos en el directorio seccion6/codigo y ejecutar:
```
python app.py
```

![Captura](https://github.com/RndMnkIII/rest-api-flask/blob/master/images/captura_app_py.png)

Para hacer pruebas con el API REST se recomienda el entorno de desarrollo de API's Postman.

https://www.getpostman.com/
