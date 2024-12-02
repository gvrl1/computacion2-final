# Chatbot JDM

Información general y ayuda de uso

Un chatbot interactivo que permite consultar información sobre el
mercado automovilístico Japanese Domestic Market (JDM). Los clientes pueden conectarse al servidor y seleccionar preguntas relacionadas con la historia, modelos icónicos, piezas y eventos de la cultura JDM.

Características principales

1. Menú interactivo con las siguientes opciones: 
    - Historia de JDM
    - Modelos icónicos
    - Piezas y modificaciones (procesados por Celery)
    - Eventos y cultura
2. Gestión concurrente de múltiples clientes mediante asyncio.
3. Procesamiento de tareas complejas con Celery y Redis.

Requisitos

- Python 3.8+
- Redis para el manejo de la cola de tareas.
- Dependencias instaladas en el archivo requirements.txt.

Cómo usar

1. Inicia Redis: redis-server
2. Inicia Celery: celery -A tasks worker --loglevel=info
3. Inicia el servidor: python server/server.py
4. Conectate como cliente: python client/client.py --host 127.0.0.1 --port 5555
5. Interacción: una vez conectado, selecciona una opción del menú.