# 🤟 GLOSSA - Traductor de LESCO

**Traductor de Lengua de Señas Costarricense (LESCO) en tiempo real**

## 📋 Descripción

GLOSSA es una aplicación que facilita la comunicación entre personas oyentes y no oyentes mediante la traducción de LESCO (Lengua de Señas Costarricense).

### ✨ Características

- 📹 **Señas a Texto**: Traduce señas capturadas por cámara a texto
- ✍️ **Texto a Señas**: Muestra cómo hacer una seña al escribir una palabra  
- 📚 **Diccionario**: Explora todas las palabras disponibles en LESCO

## 🚀 Instalación

### Requisitos previos
- Python 3.7 o superior
- Cámara web (para la función de traducción de señas)

### Pasos de instalación

1. **Clona o descarga el proyecto**

git clone [URL_DEL_REPOSITORIO]
cd glossa-lesco-translator


2. **Ejecuta el script de configuración**

python setup.py


3. **O instala manualmente las dependencias**

pip install -r requirements.txt


## 🎮 Uso

### Ejecutar la aplicación

python main.py


### Funcionalidades

#### 📹 Señas a Texto
1. Haz clic en "Iniciar Cámara"
2. Realiza una seña frente a la cámara
3. Presiona "Traducir Seña" para obtener la traducción

#### ✍️ Texto a Señas  
1. Escribe una palabra en el campo de texto
2. Haz clic en "Buscar Seña" para ver la descripción
3. Sigue las instrucciones para realizar la seña

#### 📚 Diccionario
1. Explora la lista de palabras disponibles
2. Haz doble clic en cualquier palabra para ver su descripción

## 📖 Palabras Disponibles

- **Saludos**: hola, gracias, por favor
- **Respuestas**: sí, no  
- **Necesidades**: agua, comer
- **Lugares**: casa
- **Personas**: familia
- **Actividades**: trabajo

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica de usuario
- **OpenCV**: Captura y procesamiento de video
- **Pillow**: Procesamiento de imágenes

## 🔧 Estructura del Proyecto

glossa-lesco-translator/
├── main.py              # Aplicación principal
├── setup.py             # Script de configuración
├── requirements.txt     # Dependencias
└── README.md           # Documentación

## 🎯 Próximas Mejoras

- [ ] Implementar reconocimiento real de señas con Machine Learning
- [ ] Agregar más palabras al diccionario
- [ ] Incluir imágenes y videos demostrativos
- [ ] Soporte para frases completas
- [ ] Modo de aprendizaje interactivo

