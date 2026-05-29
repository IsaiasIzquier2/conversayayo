import edge_tts
import asyncio
import pygame
import io

VOZ = "es-ES-AlvaroNeural"  # Cambia a "es-ES-ElviraNeural" si prefieres voz femenina

pygame.mixer.init()


async def _hablar_async(texto: str):
    communicate = edge_tts.Communicate(texto, VOZ)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    sound = pygame.mixer.Sound(io.BytesIO(audio_data))
    sound.play()
    while pygame.mixer.get_busy():
        await asyncio.sleep(0.05)


def hablar(texto: str):
    print("Asistente:", texto)
    asyncio.run(_hablar_async(texto))