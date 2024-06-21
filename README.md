La version utilizada de python es Python 3.10.4
Se utilizo flask para levantar los servidores.
Para desplegar el programa se deben seguir estos pasos (windows):
- descromprimir e ingresar a la consola en la misma carpeta donde estan los scripts server.py y cliente.py
- escribir en la consola: python server.py y enter
- escribir python cliente.py seguido de la direccion del archivo de configuracion, en este caso se incluyen 3 archivos de ejemplo que se encuentran en la misma carpeta, por lo que quedara como python cliente.py config1.json por ejemplo.
- hacer estos con los otros archivos de configuracion o crear uno.
- el programa se ejecutara solo a partir de aqui, fijarse en la consola de los clientes y servidores para informacion adicional.


---- Log Server -----
Es necesario inicialiazr el servidor de logs con python logging_server.py para que se puedan guardar los datos.
Pre requisitos: instalar pyro
pip install Pyro5

## Pasos para ejecutar el sistema
1. Iniciar el servidor de nombres Pyro5:
    python3 -m Pyro5.nameserver
2. Ejecutar el servidor central de logs serverRMI.py:
    python3 serverRMI.py
3. Ejecutar el cliente RMI para enviar los logs:
    python3 cliente_rmi.py config1.json
    python3 cliente_rmi.py config2.json
    python3 cliente_rmi.py config3.json



