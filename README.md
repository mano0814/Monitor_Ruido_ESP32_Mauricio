# Monitor de Audio Profesional - Gain Staging e Historial (IoT)

## Descripción del Proyecto
Este proyecto es un asistente IoT diseñado para estudios de grabación caseros y guitarristas. El sistema simula la captura de señal de audio, calcula el nivel de presión sonora real mediante el **Valor RMS (Root Mean Square)** utilizando el ADC del ESP32, y activa alertas visuales (Semáforo LED) y auditivas (Buzzer) para evitar la saturación de la señal (*clipping*). 

Actualmente funciona bajo una **arquitectura bidireccional centralizada**, donde la interfaz gráfica en Python actúa como el "cerebro" (evaluando umbrales) y el ESP32 como el hardware ejecutor (capturando audio y encendiendo luces según las órdenes del software).

## Simulación en Wokwi
Puedes probar el funcionamiento del firmware interactivo en el siguiente enlace:
👉 **[https://wokwi.com/projects/479716984050926593](https://wokwi.com/projects/479716984050926593)**

## Organización del Código (`main.py` - Hardware)
El código en MicroPython para el ESP32 se ha simplificado al delegar la lógica de decisiones a Python. Sus bloques principales son:
1. **Configuración Inicial:** Definición de pines GPIO para entradas analógicas (ADC1) y salidas (LEDs y Buzzer), junto con la conexión a la red Wi-Fi.
2. **Cliente MQTT Bidireccional:** Configuración para publicar lecturas y suscribirse al tópico de control de luces.
3. **Funciones de Procesamiento:** `calcular_rms` para el muestreo de energía de onda (100 muestras continuas) y `callback_leds` para ejecutar los cambios físicos de luces comandados por Python.
4. **Bucle Principal:** Muestrea la señal, envía el valor, y revisa la llegada de nuevas instrucciones constantemente sin bloquear la CPU.

## Interfaz Gráfica (Tkinter)
Ubicada en el directorio `/interfaz`, desarrollada completamente en Python usando librerías nativas:

- **`main_app.py`:** Ventana principal y controlador central. Implementa un menú de navegación con botones redondeados. Recibe los datos del ESP32 (`estudio/monitor/gain`), evalúa los umbrales dependiendo del módulo activo en pantalla, y envía las órdenes de color de vuelta al hardware (`estudio/monitor/leds`).
- **`modulo_gain.py` (Gain Staging):** Medidor VU analógico en forma de arco (Verde, Amarillo, Rojo) con aguja dinámica calculada mediante trigonometría para evitar el clipping. Opera con umbrales de advertencia altos (15000 y 25000 RMS).
- **`modulo_ambiente.py` (Ruido Ambiental):** Mide el piso de ruido de la sala. Incluye una pantalla de configuración para ingresar las dimensiones del cuarto (L x A x H). Opera con alta sensibilidad (Amarillo en 2500, Rojo en 6000) para asegurar un entorno silencioso antes de grabar.
- **`modulo_datos.py` (Historial CSV):** Tabla de registro (`Treeview`) vinculada al módulo de ruido ambiental. Captura una lectura por segundo en segundo plano e incluye funcionalidades para **Exportar** e **Importar** sesiones completas en formato `.csv`.

## Estado Actual y Últimos Cambios
- **Solución de Simulación:** Se resolvió el bloqueo de ejecución en Wokwi eliminando archivos de configuración de dependencias problemáticos.
- **Transición de Arquitectura (IoT Bidireccional):** Se implementó una comunicación MQTT a doble vía. El ESP32 ya no decide los colores; publica datos de audio puro y obedece las órdenes de color enviadas por la interfaz.
- **Corrección de Lógica Visual:** Se ajustó la fórmula de cálculo angular del VU Meter para que la aguja inicie a la izquierda con el silencio, sincronizándolo con un arco de colores corregido según los estándares de audio (Verde a la izquierda, Rojo a la derecha).
- **Desarrollo de Módulos Funcionales:** Finalización e integración del Módulo 1 (verificación de piso de ruido con dimensiones de sala) y el Módulo 3 (historial de captura de datos con exportación a CSV).