## Descripción del Proyecto
Este proyecto es un asistente IoT diseñado para estudios de grabación caseros y guitarristas. El sistema simula la captura de señal de audio, calcula el nivel de presión sonora real mediante el **Valor RMS (Root Mean Square)** utilizando el ADC del ESP32, y activa alertas visuales (Semáforo LED) y auditivas (Buzzer) para evitar la saturación de la señal (*clipping*).

## Simulación en Wokwi
Puedes probar el funcionamiento del firmware interactivo en el siguiente enlace:
👉 **[https://wokwi.com/projects/479716984050926593](https://wokwi.com/projects/479716984050926593)**

## Organización del Código (`main.py`)
El código está estructurado en 4 bloques modulares:
1. **Configuración de Pines:** Se definen los pines GPIO como salidas y el pin 34 como entrada analógica (ADC1).
2. **Umbrales:** Variables constantes que definen cuándo el sistema cambia de estado.
3. **Funciones (`calcular_rms` y `actualizar_estado`):** Contienen la lógica matemática para calcular la energía de la onda, aislando la lógica de los actuadores.
4. **Bucle Principal:** Muestrea la señal infinitamente con un pequeño retardo para proteger la CPU.