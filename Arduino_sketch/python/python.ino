/*
SKETCH DE CONTROL PARA JUEGO PYGAME (4 BOTONES + LED)

- D2: Botón Arriba (UP)

- D3: Botón Derecha/Enter (RIGHT)

- D4: Botón Abajo (DOWN)

- D5: Botón Izquierda/Escape (LEFT)

- D13: LED indicador

*/

// --- Configuración de Pines ---
const int BOTON_UP = 2;
const int BOTON_RIGHT = 3; // D3 -> Flecha Derecha / Enter
const int BOTON_DOWN = 4;
const int BOTON_LEFT = 5;  // D5 -> Flecha Izquierda / Escape
const int LED = 13;

// --- Variables de Estado (para antirebote) ---
int estadoUpAnterior = HIGH;
int estadoRightAnterior = HIGH;
int estadoDownAnterior = HIGH;
int estadoLeftAnterior = HIGH;

// --- Tiempos de Antirebote (Debounce) ---
long tiempoUltimoUp = 0;
long tiempoUltimoRight = 0;
long tiempoUltimoDown = 0;
long tiempoUltimoLeft = 0;
const long retardoDebounce = 50; // 50 milisegundos

void setup() {
Serial.begin(9600); // Inicia la comunicación serial
  
// Configurar pines de botones como entrada con resistencia PULLUP interna
pinMode(BOTON_UP, INPUT_PULLUP);
pinMode(BOTON_RIGHT, INPUT_PULLUP);
pinMode(BOTON_DOWN, INPUT_PULLUP);
pinMode(BOTON_LEFT, INPUT_PULLUP);
  
// Configurar LED como salida
pinMode(LED, OUTPUT);
}

void loop() {
// Obtener el tiempo actual una sola vez
long tiempoActual = millis();

// --- Leer el estado actual de los botones ---
int estadoUp = digitalRead(BOTON_UP);
int estadoRight = digitalRead(BOTON_RIGHT);
int estadoDown = digitalRead(BOTON_DOWN);
int estadoLeft = digitalRead(BOTON_LEFT);

// --- Manejo del Botón UP (D2) ---
if (estadoUp != estadoUpAnterior && (tiempoActual - tiempoUltimoUp) > retardoDebounce) {
if (estadoUp == LOW) {
Serial.println("UP_DOWN"); // Mensaje al presionar
} else {
Serial.println("UP_UP");   // Mensaje al soltar
}
tiempoUltimoUp = tiempoActual;
estadoUpAnterior = estadoUp;
}

// --- Manejo del Botón RIGHT (D3) ---
if (estadoRight != estadoRightAnterior && (tiempoActual - tiempoUltimoRight) > retardoDebounce) {
if (estadoRight == LOW) {
Serial.println("RIGHT_DOWN"); // Mensaje al presionar
} else {
Serial.println("RIGHT_UP");   // Mensaje al soltar
}
tiempoUltimoRight = tiempoActual;
estadoRightAnterior = estadoRight;
}

// --- Manejo del Botón DOWN (D4) --- <--- BLOQUE CORREGIDO con Debounce
if (estadoDown != estadoDownAnterior && (tiempoActual - tiempoUltimoDown) > retardoDebounce) {
if (estadoDown == LOW) {
Serial.println("DOWN_DOWN"); // Mensaje al presionar
} else {
Serial.println("DOWN_UP");    // Mensaje al soltar
}
tiempoUltimoDown = tiempoActual;
estadoDownAnterior = estadoDown;
}

// --- Manejo del Botón LEFT (D5) ---
if (estadoLeft != estadoLeftAnterior && (tiempoActual - tiempoUltimoLeft) > retardoDebounce) {
if (estadoLeft == LOW) {
Serial.println("LEFT_DOWN"); // Mensaje al presionar
} else {
Serial.println("LEFT_UP");   // Mensaje al soltar
}
tiempoUltimoLeft = tiempoActual;
estadoLeftAnterior = estadoLeft;
}

// --- Manejo del LED (D13) ---
// El LED se enciende si CUALQUIER botón está presionado (LOW)
if (estadoUp == LOW || estadoRight == LOW || estadoDown == LOW || estadoLeft == LOW) {
digitalWrite(LED, HIGH);
} else {
digitalWrite(LED, LOW);
}

// Pequeña pausa para estabilizar el bucle
delay(5);
}