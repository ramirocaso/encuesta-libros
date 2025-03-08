import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
import os

# Configuración de página
st.set_page_config(
    page_title="Encuesta de Opinión de Libros",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos personalizados
st.markdown("""
    <style>
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        color: #4B5563;
        margin-bottom: 30px;
    }
    .stForm {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título y descripción
st.markdown('<p class="title">Encuesta de Opinión de Libros</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Por favor, comparte tu opinión sobre el libro que has leído.</p>', unsafe_allow_html=True)

# Función para conectar con Google Sheets
def get_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Intentar leer desde variable de entorno o desde archivo local
    if 'GOOGLE_CREDENTIALS' in os.environ:
        json_creds = os.environ.get('GOOGLE_CREDENTIALS')
        cred_dict = json.loads(json_creds)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    
    client = gspread.authorize(credentials)
    sheet = client.open('Book Opinions Survey').sheet1
    
    # Verificar si necesitamos agregar encabezados
    values = sheet.get_all_values()
    
    # Si la hoja está vacía, agregamos encabezados
    if not values:
        headers = [
            'Nombre del Participante',
            'Título del Libro',
            'Valoración General (1-5)',
            'Valoración de la Estructura (1-5)',
            'Valoración de la Historia (1-5)',
            'Comentarios',
            'Fecha de Envío'
        ]
        sheet.append_row(headers)
    
    return sheet

# Formulario de Streamlit
with st.form("book_survey", border=False):
    col1, col2 = st.columns(2)
    
    with col1:
        participant_name = st.text_input("Tu Nombre:", placeholder="Escribe tu nombre")
    
    with col2:
        book_title = st.text_input("Título del Libro:", placeholder="Nombre del libro")
    
    # Ratings con sliders - más intuitivos que radio buttons
    st.write("### Valoraciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Valoración General**")
        st.write("¿Qué te pareció el libro en general?")
        overall_rating = st.slider("General", 1, 5, 3, label_visibility="collapsed", 
                                 help="1 = Muy malo, 5 = Excelente")
        st.caption("1 = Muy malo, 5 = Excelente")
    
    with col2:
        st.write("**Valoración de la Estructura**")
        st.write("¿Cómo valoras la organización y estructura del libro?")
        structure_rating = st.slider("Estructura", 1, 5, 3, label_visibility="collapsed", 
                                   help="1 = Muy mala, 5 = Excelente")
        st.caption("1 = Muy mala, 5 = Excelente")
    
    st.write("**Valoración de la Historia**")
    st.write("¿Qué te pareció la trama o contenido del libro?")
    story_rating = st.slider("Historia", 1, 5, 3, label_visibility="collapsed", 
                           help="1 = Muy mala, 5 = Excelente")
    st.caption("1 = Muy mala, 5 = Excelente")
    
    # Comentarios
    st.write("### Comentarios")
    comments = st.text_area("Comentarios Adicionales (Opcional):", 
                          placeholder="Comparte tus pensamientos sobre el libro...",
                          height=150)
    
    # Botón de envío
    submitted = st.form_submit_button("Enviar Opinión", use_container_width=True, type="primary")

# Procesar el formulario cuando se envía
if submitted:
    # Validación básica
    if not participant_name.strip():
        st.error("Por favor, ingresa tu nombre.")
    elif not book_title.strip():
        st.error("Por favor, ingresa el título del libro.")
    else:
        try:
            # Barra de progreso simulada
            with st.spinner("Enviando tu opinión..."):
                # Obtener fecha actual
                date_submitted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Conectar a Google Sheets y enviar datos
                sheet = get_google_sheet()
                sheet.append_row([
                    participant_name,
                    book_title,
                    overall_rating,
                    structure_rating,
                    story_rating,
                    comments,
                    date_submitted
                ])
                
                # Pequeña pausa para mejor experiencia de usuario
                import time
                time.sleep(1)
            
            # Mostrar mensaje de éxito
            st.success("¡Gracias por enviar tu opinión!")
            st.balloons()  # Efecto visual divertido
            
            # Opción para enviar otra respuesta
            if st.button("Enviar otra opinión"):
                st.experimental_rerun()
            
        except Exception as e:
            st.error(f"Error al enviar tu respuesta: {str(e)}")
            st.info("Por favor, verifica tu conexión a internet e inténtalo de nuevo.")

# Footer
st.markdown("---")
st.caption("Grupo de Lectura | Creado con Streamlit")