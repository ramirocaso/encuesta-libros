# Encuesta de Opinión de Libros

Una aplicación web para recopilar y almacenar opiniones sobre libros leídos en grupos de lectura.

## 📚 Descripción

Esta aplicación permite a los miembros de un grupo de lectura calificar y compartir sus opiniones sobre los libros que han leído. Cada participante puede evaluar los libros en tres dimensiones (valoración general, estructura e historia) y agregar comentarios adicionales. Todas las respuestas se almacenan automáticamente en Google Sheets para su fácil acceso y análisis.

## ✨ Características

- Formulario intuitivo y atractivo para calificar libros
- Escalas de valoración de 1 a 5 para diferentes aspectos del libro
- Almacenamiento automático en Google Sheets
- Interfaz completamente en español
- Accesible desde cualquier dispositivo con navegador web
- Diseño responsive para móviles y computadoras

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework de Python para crear aplicaciones web de datos
- **Google Sheets API**: Para almacenar las respuestas en la nube
- **gspread**: Biblioteca de Python para interactuar con Google Sheets
- **OAuth2**: Para la autenticación segura con Google

## 🚀 Despliegue

La aplicación está desplegada en Streamlit Cloud y es accesible públicamente en:

```
https://grupitolector.streamlit.app
```

## 💻 Desarrollo Local

Para ejecutar esta aplicación en tu entorno local:

1. Clona este repositorio:
```
git clone https://github.com/ramirocaso/encuesta-libros.git
```

2. Instala las dependencias:
```
pip install -r requirements.txt
```

3. Configura las credenciales de Google:
   - Crea un proyecto en Google Cloud Platform
   - Habilita las APIs de Google Sheets y Drive
   - Crea y descarga las credenciales de una cuenta de servicio
   - Guarda el archivo como `credentials.json` en la carpeta del proyecto

4. Ejecuta la aplicación:
```
streamlit run app.py
```

## 🔒 Seguridad

La aplicación utiliza variables de entorno seguras para almacenar las credenciales de Google, garantizando que la información sensible no se exponga en el código fuente.

## 👥 Autores

- **Ramiro Caso** - Desarrollo y despliegue
- **Claude (Anthropic)** - Asistencia en desarrollo y documentación

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

Desarrollado para facilitar la recopilación de opiniones en grupos de lectura. ¡Esperamos que ayude a enriquecer las discusiones literarias de tu comunidad!
