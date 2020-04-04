# COVID-19 | Server
Procesos para extracción de datos.

## Helpers
Agrupé distintas funcionalidades en Helpers con el fin de mantener un orden.

### `Helper.py`
Funcionalidades globales o comunes a los distintos módulos.

### `ECDC_Helper.py`
Funcionalidades relacionadas con el _European Centre for Disease Prevention and Control (ECDC)_.

### `Google_Helper.py`
Funcionalidades relacionadas con data que se pueda obtener de _Google_.

## Ejemplos de uso
1. Obtener data del _ECDC_ y almacenarla en JSON

```python
from lib.helpers.ECDC_Helper import *

# 1. Obtengo la data del ECDC
data = ecdc_get_data()

# 2. Guardo en json
if(data):
  ecdc_save_data_to_json(data['rows'])
```

2. Obtener data del _ECDC_ y almacenarla en MongoDB

```python
from lib.helpers.ECDC_Helper import *
from lib.MongoDBClient import MongoDBClient

# 1. Obtengo la data del ECDC
data = ecdc_get_data()

# 2. Guardo en Mongo
# Conexión a MongoDB
mc = MongoDBClient()
if(mc.isConnected()):  
  if(data and data['update']):
    for index, row in data['rows'].iterrows():
      #Convierto a diccionario
      data_row = row.to_dict()

      # Upsert
      condition = {
        'date_report': data_row['date_report'],
        'country_code': data_row['country_code']
      }
      mc.update('cases', data_row, condition)
  else:
    print('No hay data por actualizar')
else:
  print('Error de conexión a la DB')
```

## Configuración para almacenamiento en MongoDB
1. Obtener la info de conexión a la base de datos: host, usuario, contraseña y nombre de la DB
2. Almacenarla en `config/config.ini`

En el ejemplo usé [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), en caso de utilizar otra funciona sin problemas. La única precación al respecto es con el nombre de la sección "MongodbAtlas" en el archivo de configuración, si se agrega o modifica dicho nombre, habrá que hacer el ajuste correspondiente en `lib/MongoDBClient.py`