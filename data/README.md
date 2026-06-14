# Directorio de Datos (Data)

Esta carpeta contiene la información necesaria para trabajar con los videos usados en el proyecto **FutBot Ghost Replay**.

## Fuente del Video
Los videos oficiales utilizados para este proyecto provienen del repositorio de la competencia. Pueden ser descargados desde el siguiente enlace de Google Drive:
[Videos Copa FutBotMX (Drive)](https://drive.google.com/drive/folders/1vYXFP8cdKx7OtxbJ_CFYaa4-lUZOt18k)

## IMPORTANTE: Regla de Control de Versiones
**NUNCA SUBIR VIDEOS A GITHUB.** Para mantener la agilidad del desarrollo en equipo, los archivos de video pesado (`.mp4`, `.avi`, etc.) deben permanecer en local y están ignorados por el `.gitignore`.

## Video usado en M1

Para el Milestone M1 se utilizó el siguiente video:

| Campo | Información |
|---|---|
| Nombre del archivo en línea | `video-1080_singular_display.mov` |
| Nombre del archivo local | `videoInstrucciones.mov` |
| Fuente | Repositorio oficial de videos Copa FutBotMX |
| URL de descarga | `https://drive.google.com/file/d/1-39yAydXRA_O4dOj6KW_NeLdwjAcXPsN/view?usp=drive_link` |
| Fecha de descarga | `2026-05-31` |
| Uso dentro del proyecto | Extracción de frames para pruebas iniciales de segmentación con SAM 3 |
| Ubicación local esperada | `data/raw/videoInstrucciones.mov` |

## Instrucciones de descarga

1. Descargar el video desde la URL oficial indicada arriba.
2. Crear la carpeta `data/raw/` si no existe.
3. Colocar el archivo descargado `video-1080_singular_display.mov` y renombrarlo con el siguiente nombre:`videoInstrucciones.mov`
* **Evidencias:** Los frames ligeros extraídos para comprobación visual se guardan en `docs/assets/m1/frames/`.