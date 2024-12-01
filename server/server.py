import socket
import asyncio
from tasks import process_jdm_question

menu = """
Bienvenido al Chatbot de JDM 🚗
Selecciona una opción:
1. Historia de JDM
2. Modelos icónicos
3. Piezas y modificaciones
4. Eventos y cultura
5. Salir
"""

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión nueva desde {addr}")
    writer.write(menu.encode())
    await writer.drain()

    while True:
        data = await reader.read(100)
        if not data:
            break
        option = data.decode().strip()
        print(f"Cliente seleccionó: {option}")

        if option == "1":
            response = "JDM se refiere a autos fabricados exclusivamente para el mercado japonés."
        elif option == "2":
            response = "Modelos icónicos: Nissan Skyline GT-R, Toyota Supra, Mazda RX-7."
        elif option == "3":
            # Usa Celery para manejar tareas más complejas
            result = process_jdm_question.delay("Detalles de piezas y modificaciones")
            try:
                # Espera a que la tarea se complete con un timeout
                response = result.get(timeout=10)
            except Exception as e:
                response = f"Error al procesar la tarea: {str(e)}"
        elif option == "4":
            response = "Eventos populares: Tokyo Auto Salon, eventos de drifting en Japón."
        elif option == "5":
            response = "Gracias por usar el Chatbot de JDM. ¡Hasta luego!"
            writer.write(response.encode())
            await writer.drain()
            break
        else:
            response = "Opción no válida. Por favor selecciona del 1 al 5."

        writer.write(response.encode())
        await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5555)
    print("Servidor escuchando en el puerto 5555...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())