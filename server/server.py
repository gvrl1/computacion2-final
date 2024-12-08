import asyncio
from tasks import process_jdm_question

menu = """
Bienvenido al Chatbot de JDM 🚗
Selecciona una opción:
1. Historia de JDM
2. Modelos icónicos
3. Piezas y modificaciones
4. Eventos y cultura
0. Salir
"""

# Función para manejar la opción 3 usando Celery
async def handle_option_3():
    result = process_jdm_question.delay("Detalles de piezas y modificaciones")
    try:
        # Espera a que la tarea se complete con un timeout
        return result.get(timeout=10)
    except Exception as e:
        return f"Error al procesar la tarea: {str(e)}"

# Diccionario que mapea opciones a funciones
options = {
    "0": lambda: "Gracias por usar el Chatbot de JDM. ¡Hasta luego!",
    "1": lambda: "JDM se refiere a autos fabricados exclusivamente para el mercado japonés.",
    "2": lambda: "Modelos icónicos: Nissan Skyline GT-R, Toyota Supra, Mazda RX-7.",
    "3": handle_option_3,
    "4": lambda: "Eventos populares: Tokyo Auto Salon, eventos de drifting en Japón.",
}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión nueva desde {addr[0]}:{addr[1]}") #Muestra la IP y puerto del cliente

    # Envia el menu al cliente
    writer.write(menu.encode())
    await writer.drain()

    while True:
        data = await reader.read(100)
        if not data:
            break
        option = data.decode().strip()
        print(f"Cliente {addr} seleccionó: {option}")

        if option in options:
            if option == "0":
                response = options[option]()
                writer.write(response.encode())
                await writer.drain()
                break
            elif option == "3":
                response = await options[option]()
            else:
                response = options[option]()
        else:
            response = "Opción no válida. Por favor selecciona del 1 al 4."

        writer.write(response.encode())
        await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5555)
    print("Servidor escuchando en el puerto 5555...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())