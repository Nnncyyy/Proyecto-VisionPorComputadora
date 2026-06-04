# Registro de Errores y Hallazgos

Este documento centraliza los problemas técnicos encontrados, los descubrimientos sobre el comportamiento de los modelos (SAM 3, YOLO, ByteTrack) y las decisiones arquitectónicas tomadas a lo largo del proyecto Copa FutBotMX.

---

## Plantilla de Registro (Cómo documentar)
Para cada nueva entrada, utilizar el siguiente formato:
* **[Tipo: Error | Hallazgo | Decisión] - Título breve**
  * **Contexto:** (En qué issue, notebook o script ocurrió)
  * **Descripción:** (Qué sucedió, qué intentaban hacer o qué comportamiento notaron en el modelo)
  * **Solución / Impacto:** (Cómo se resolvió el error o qué camino se decidió tomar a partir de este hallazgo)

---

## Milestone 1: Segmentación Baseline con SAM 3

* **[Hallazgo] - Tiempos de carga y ejecución en procesador**
  * **Contexto:** Issue M1-02 (Verificar carga de SAM 3).
  * **Descripción:** Al ejecutar inferencia en un entorno local sin aceleración de GPU dedicada (usando un procesador AMD Ryzen), el modelo SAM 3 toma un tiempo considerable tanto en la carga en memoria como en la generación de máscaras.
  * **Solución / Impacto:** Se debe forzar el parámetro `device="cpu"` en la inicialización del modelo para evitar crashes. La carga inicial de SAM 3 toma alrededor de 30 segundos ejecutándose en CPU.

---