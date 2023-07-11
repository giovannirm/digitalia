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

Añadiendo las migraciones
```console
python manage.py makemigrations api
python manage.py migrate
```

Creando superusuario
```console
python manage.py createsuperuser
```

Correr la aplicación

```console
cd settings
python manage.py runserver
```
Referenciado de [Giovanni Rojas](https://github.com/giovannirm/digitalia)