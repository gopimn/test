# Telemetry system proposal
La mayoría de los fabricantes usa sockets para la comunicación a través de la red celular con sus dispositivos (si bien alguos soportan http o mqtt entre otros). Si bien a primera vista esto puede parecer algo engorroso a desarrollar, desde mi perspectiva es genial porque se tiene más control de lo que se hace a nivel de comunicación (http por ejemplo siempre cierra la comunicación después de un request).

Es importante saber cuáles son las necesidades del cliente (de existir), porque no todos los fabricantes entregan la misma información y no todos lo hacen de la misma manera. Para fines de este ejercicio asumiremos que lo que se necesita es velocidad, geolocalización, timestamp (abstrayéndonos de la problemática de la detección de ignición de los vehículos, entre otras).

La solución propuesta se ejemplifica como sigue:

![solution_diag](https://user-images.githubusercontent.com/5314353/93008387-76ef4a00-f54a-11ea-8a0c-e9da6a63cfbd.png)

Que tiene los siguientes componentes:
- __Devices__,los dispositivos de telemetría, podemos enfrentarnos a un environment multimarca (queclink ruptela, galileosky, teltonika, etc).

- __Input and Output queues__, estas son colas de mensajes que bufferean la información desde y hacia los dispositivos. Esto entrega versatilidad a la solución puesto que si uno de los elementos aguas abajo de las colas deja de funcionar, no se pierde información de os clientes. La tecnología específica puede variar, Apache Kafka, Google pub/sub, Amazon MQ, RabbitMQ, y dependerá de las necesidades de la empresa, capacidad del equipo y presupuesto. Asumiremos que estamos usando rabbitMQ, dada mi familiaridad con pika.

- __Collections__, si bien para la permanencia de datos se puede utilizar un sinnúmero de tecnologías (PostgreSQL, MongoDB, Mysql, SQLserver) para fines de este ejercicio se utilizará MongoDB, principalmente porque al ser no relacional entrega versatilidad al tratamiento de datos. Tenemos tres colecciones (tablas):
  + _socket_, su función principal es tener un respaldo de todo el raw que entra y sale del sistema, desde y hacia las colas de entrada y salida.
  + _sender_, guarda toda la información que se escribe (o no) en la cola de salida
  + _input_, aquí vive la información con la que se obtendrán indicadores del uso de los vehículos.
  + Se puede necesitar más colecciones, como por ejemplo para identificar los modelos/marca de los vehículos dependiendo de la data cruda que llega.
_Por supuesto que la recomendación es tener en caliente no más de tres meses de datos en la DB para que el rendimiento de las querys sea constante en el tiempo._

- __Parser__, es el encargado de consumir la cola de entrada y parsear los datos, dependiendo del modelo/marca del dispositivo de origen. Una de los desafíos es identificar el tipo de dispositivo desde los datos crudos, un buen approach es tener de antemano esta información dependiendo de la IMEI (Identificador único de módulo de comunicación celular), es decir, tener otra colección con el IMEI -> modelo/marca. La implementación de este servicio puede ser en cualquier lenguaje. Para fines de este ejercicio se usará python.

- __Sender__, su función es insertar los datos/comandos en la cola de salida, esta información también esta amarrada al modelo/marca de los dispositivos, y se obtendría de una API (que usaría el cliente a través de un front end).
La implementación de este servicio puede ser en cualquier lenguaje. Para fines de este ejercicio se usará python.
Dado que la versatilidad y tolerancia a fallos es algo necesesario, es conveniente separar estas dos entidades (API y sender) a través de una cola, por lo que el diagrama quedaría como sigue:

![sda](https://user-images.githubusercontent.com/5314353/93008965-92aa1e80-f551-11ea-9bac-9248178245f7.png)

- __Socket master__, es donde pegan los devices, para fines de este ejercicio, asumiremos que el nombre de dominio apunta a este servicio o que los devices envían directamente a la IP/port. Dado que existe el requerimiento de una comunicación bidireccional, se tiene una cola de entrada y una cola de salida. Con la cola de entrada no hay problema, se tiene una nuevo cliente(device) que genera una conexión con el socket, se añade un thread para manejar esta conexión, y todo lo que llegue desde esta conexión se envía a la cola de entrada. El problema es cuando se tienen comandos que van hacia el dispositivo. dado que generar una cola para cada dispositivo es contraproducente, se debe idear un mecanismo para poder enviar la información que corresponde al dispositivo, identificandolo por la imei; algo que se puede hacer es ponerle un parámetro al objeto cliente que sea la imei, y que la clase que genera los threads tenga un diccionario con el identificador de estos clientes y la IMEI, de tal manera que al consumir la cola, se sepa a que objeto entregarle el comando. MMMM no es una tarea trivial y pienso que es un buen ejercicio para mañana, principalmente por esta dificultad. Los otros subsistemas son bien straigthfordward.

Cabe recalcar que esto si se podría inmplementar en un una herramienta como Kafka.

# Testing 
Ahora bien, este sistema hay que estresarlo y poder sacar resultados de por ejemplo, tiempo de permanencia de los mensajes. para este fin se debería implementar algo como lo que indica el siguiente diagrama:



# 


