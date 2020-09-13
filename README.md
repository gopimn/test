# Telemetry system proposal
La mayoría de los fabricantes usa sockets para la comunicación a través de la red celular con sus dispositivos (si bien alguos soportan http o mqtt entre otros). Si bien a primera vista esto puede parecer algo engorroso a desarrollar, desde mi perspectiva es genial porque se tiene más control de lo que se hace a nivel de comunicación (http por ejemplo siempre cierra la comunicación después de un request).

Es importante saber cuáles son las necesidades del cliente (de existir), porque no todos los fabricantes entregan la misma información y no todos lo hacen de la misma manera. Para fines de este ejercicio asumiremos que lo que se necesita es velocidad, geolocalización, timestamp (abstrayéndonos de la problemática de la detección de ignición de los vehículos, entre otras)
La solución propuesta se ejemplifica como sigue:

![solution_diag](https://user-images.githubusercontent.com/5314353/93008387-76ef4a00-f54a-11ea-8a0c-e9da6a63cfbd.png)

Que tiene los siguientes componentes:
- __Devices__,
Dependiendo del modelo y marca del dispositivo (queclink ruptela, galileosky, teltonika, etc) se tendrá un tipo específico de trama, que el parser debe saber diferenciar. 

Por supuesto que la recomendación es tener en caliente no más de tres meses de datos en la DB para que el rendimiento de las querys sea constante en el tiempo.
