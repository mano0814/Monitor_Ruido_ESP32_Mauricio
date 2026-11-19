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


### Interfaz Gráfica (Tkinter)
Ubicada en el directorio `/interfaz`, desarrollada completamente en Python usando librerías nativas:

* **`main_app.py`:** Ventana principal de la aplicación. Implementa un menú de navegación superior con botones redondeados personalizados creados mediante el componente `Canvas` de Tkinter, evitando el uso de librerías externas.
* **`modulo_gain.py`:** Módulo de Asistente de Gain Staging. Incluye:
  * **VU Meter Analógico:** Medidor en forma de arco (rojo, amarillo, verde) con una aguja dinámica calculada mediante trigonometría para reflejar los niveles de audio.
  * **Semáforo Visual:** Tres indicadores LED en pantalla que alertan sobre el estado de la señal (Óptimo, Advertencia o Clipping).

## Próximos Pasos
* Integración del Módulo de Ruido Ambiental.
* Integración del Módulo de exportación de datos a CSV.
* Conexión entre el hardware (ESP32) y la interfaz gráfica para la transmisión de datos en tiempo real.
* ## Estado Actual y Últimos Cambios

### Avances Implementados
* **Conexión MQTT Modular (`interfaz/cliente_mqtt.py`):** Se desacopló la recepción de datos en tiempo real utilizando `paho-mqtt`, conectada a `broker.hivemq.com` en el tópico `estudio/monitor/gain`.
* **Calibración del Medidor VU (`interfaz/main_app.py`):** Se ajustó la escala de lectura a valores RMS de 16 bits (`0` a `32768`) con limitador de rango para la aguja, sincronizando el semáforo con los umbrales del ESP32 (`15000` advertencia y `25000` clipping).
* **Simulador Local de Hardware (`interfaz/simulador_hardware.py`):** Se creó un script independiente que emula el envío de lecturas RMS del microcontrolador vía MQTT para probar el funcionamiento de la interfaz gráfica.

### Problemas Conocidos / Pendientes
* **Simulación en Wokwi:** El simulador web no inicia la ejecución del proyecto en MicroPython (sin salida en consola). Mientras se soluciona este bloqueo o se pasa al hardware físico (ESP32), las pruebas de visualización se realizan mediante `simulador_hardware.py`.
* **Módulo de Ruido Ambiental:** Pendiente de implementación e integración en la interfaz gráfica.