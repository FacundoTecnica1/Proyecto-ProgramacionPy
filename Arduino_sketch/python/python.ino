// Configuración de pines
const int boton = 2; // Pin donde está conectado tu botón
const int led = 13;  // LED integrado (opcional)

// Variables para el manejo del estado y antirebote (debounce)
int estadoBotonAnterior = HIGH; // Estado del botón en el ciclo anterior
long tiempoUltimaPulsacion = 0; // Almacena el último tiempo de pulsación
const long retardoDebounce = 50; // Retardo mínimo entre pulsaciones (50ms)

void setup() {
  Serial.begin(9600);           // Inicia la comunicación serial
  pinMode(led, OUTPUT);
  pinMode(boton, INPUT_PULLUP); // Botón con resistencia pull-up
}

void loop() {
  // Lee el estado actual del botón
  int estadoBotonActual = digitalRead(boton);

  // 1. Detectar si el botón acaba de ser presionado (cambio de HIGH a LOW)
  // 2. Asegurarse de que ha pasado suficiente tiempo desde la última pulsación
  if (estadoBotonActual == LOW && estadoBotonAnterior == HIGH && (millis() - tiempoUltimaPulsacion) > retardoDebounce) {
    
    // El botón ha sido presionado de forma válida
    digitalWrite(led, HIGH);    // Enciende el LED
    
    // **ENVÍA EL COMANDO AL SCRIPT DE PYTHON**
    Serial.println("SPACE"); 
    
    tiempoUltimaPulsacion = millis(); // Actualiza el tiempo de la última pulsación
  }

  // 3. Apagar el LED cuando el botón se suelta
  if (estadoBotonActual == HIGH) {
    digitalWrite(led, LOW);
  }
  
  // Actualiza el estado del botón para el próximo ciclo
  estadoBotonAnterior = estadoBotonActual;
}