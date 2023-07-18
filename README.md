# DIGITALIA

### Configuración

Crear el entorno virtual con anaconda y activarlo

```console
conda create -n digitalia python
activate digitalia
```

Entrar al proyecto e instalar dependencias

```console
cd digitalia
pip install -r requirements-dev.txt
```
Acceder al settings
```console
cd settings
```

Añadiendo las migraciones
```console
python manage.py makemigrations api
python manage.py migrate
```

Creando superusuario, para cuando te loguees en la aplicación
```console
python manage.py createsuperuser
```

Correr la aplicación

```console
cd settings
python manage.py runserver
```

# Para correr los TESTS
1. En el archivo settings.py, modificar el valor de API_KEY_FOR_TESTS por el valor de la api key de Open AI
2. Abres una nueva terminal, activas el entorno virtual, te diriges a la ruta de digitalia\settings
3. Ejecutas python manage.py test api

Referenciado de [Giovanni Rojas](https://github.com/giovannirm/digitalia)