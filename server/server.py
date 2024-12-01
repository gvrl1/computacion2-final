import socket
import asyncio
from tasks import process_message

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received: {message}")
        
        if "process" in message:
            # Envía la tarea a Celery
            result = process_message.delay(message)
            response = f"Task submitted. Result: {result.get(timeout=10)}"
        else:
            response = f"Echo: {message}"
        
        writer.write(response.encode())
        await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 5555)
    print("Server listening on port 5555...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())