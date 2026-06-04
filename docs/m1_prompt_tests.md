# Pruebas de prompts SAM 3 — M1

| Prompt | Frame | Resultado | Problema |
|---|---|---|---|
| robot | frame_0050 | Detecta varios robots en la cancha. | - |
| ball | frame_0050 | Detecta el balón de manera correcta. | Podría detectar otros círculos falsos en la imagen o manchas en el campo. |
| soccer robot | frame_0001 | Detecta los robots de la cancha | Detecta mejor los robots al estar más separados. |
| player | frame_0100 | Identifica los jugadores. | Identifica también a las personas como jugadores. |
| person | frame_0050 | Aísla a las personas de los robots. | - |