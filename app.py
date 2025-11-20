import streamlit as st
import boto3
import json
import base64
import io
from PIL import Image
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="🤖🎨 Creative AI Studio",
    page_icon="🤖🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de AWS Bedrock
@st.cache_resource
def init_bedrock():
    """Inicializa el cliente de Bedrock usando variables de entorno"""
    # Las credenciales deben configurarse mediante variables de entorno:
    # AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
    # O usar el archivo .streamlit/secrets.toml para Streamlit
    return boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID') or st.secrets.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY') or st.secrets.get('AWS_SECRET_ACCESS_KEY')
    )

bedrock_runtime = init_bedrock()

# Estilos disponibles para Stable Diffusion
STYLE_PRESETS = [
    "None", "3d-model", "analog-film", "anime", "cinematic", 
    "comic-book", "digital-art", "enhance", "fantasy-art", 
    "isometric", "line-art", "low-poly", "modeling-compound", 
    "neon-punk", "origami", "photographic", "pixel-art", 
    "tile-texture"
]

# Funciones para generación de imágenes
def generate_image(prompt, style="None"):
    """Genera imagen usando Amazon Titan Image Generator v2"""
    try:
        # Agregar estilo al prompt si se seleccionó uno
        enhanced_prompt = prompt
        if style != "None":
            style_descriptions = {
                "3d-model": "3D rendered model style",
                "analog-film": "analog film photography style",
                "anime": "anime cartoon style",
                "cinematic": "cinematic movie style",
                "comic-book": "comic book illustration style",
                "digital-art": "digital art style",
                "enhance": "enhanced and detailed",
                "fantasy-art": "fantasy art style",
                "isometric": "isometric view style",
                "line-art": "line art drawing style",
                "low-poly": "low poly 3D style",
                "modeling-compound": "clay modeling style",
                "neon-punk": "neon punk cyberpunk style",
                "origami": "origami paper art style",
                "photographic": "photographic realistic style",
                "pixel-art": "pixel art retro style",
                "tile-texture": "seamless tile texture style"
            }
            style_text = style_descriptions.get(style, "")
            if style_text:
                enhanced_prompt = f"{prompt}, {style_text}"

        # Configuración para Amazon Titan Image Generator v2
        body = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": enhanced_prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "height": 768,
                "width": 768,
                "cfgScale": 8.0,
                "seed": 0
            }
        }

        response = bedrock_runtime.invoke_model(
            body=json.dumps(body),
            modelId="amazon.titan-image-generator-v2:0",
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        image_data = response_body.get("images")[0]
        return base64_to_image(image_data)

    except Exception as e:
        st.error(f"Error generando imagen: {str(e)}")
        return None

def base64_to_image(base64_string):
    """Convierte base64 a imagen PIL"""
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data))

# Funciones para edición de texto con Claude
def edit_text_with_claude(text, operation="improve"):
    """Edita texto usando Claude"""
    try:
        prompts = {
            "improve": f"Mejora el siguiente texto manteniendo su mensaje principal pero haciéndolo más claro y profesional:\n\n{text}",
            "summarize": f"Resume el siguiente texto de manera concisa manteniendo los puntos más importantes:\n\n{text}",
            "expand": f"Expande el siguiente texto agregando más detalles y ejemplos relevantes:\n\n{text}",
            "correct": f"Corrige los errores gramaticales y de estilo en el siguiente texto:\n\n{text}",
            "creative": f"Reescribe el siguiente texto de manera más creativa y atractiva:\n\n{text}"
        }
        
        prompt = prompts.get(operation, prompts["improve"])
        
        body = {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 2000,
            "temperature": 0.7,
            "top_k": 250,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
        }
        
        response = bedrock_runtime.invoke_model(
            body=json.dumps(body),
            modelId="anthropic.claude-v2",
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("completion", "").strip()
        
    except Exception as e:
        st.error(f"Error editando texto: {str(e)}")
        return text

# Inicializar session state
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

if "text_history" not in st.session_state:
    st.session_state.text_history = []

if "user_role" not in st.session_state:
    st.session_state.user_role = "diseñador"

if "projects" not in st.session_state:
    st.session_state.projects = {}

# Sidebar para navegación y configuración
st.sidebar.title("🎨 Creative AI Studio")
st.sidebar.markdown("---")

# Selector de rol de usuario
user_role = st.sidebar.selectbox(
    "👤 Rol de Usuario:",
    ["diseñador", "redactor", "aprobador", "administrador"],
    key="user_role_selector"
)
st.session_state.user_role = user_role

# Mostrar permisos según el rol
permissions = {
    "diseñador": ["Generar imágenes", "Ver galería"],
    "redactor": ["Editar texto", "Ver historial"],
    "aprobador": ["Ver todo", "Aprobar contenido"],
    "administrador": ["Acceso completo", "Gestión de usuarios"]
}

st.sidebar.markdown(f"**Permisos actuales:**")
for perm in permissions[user_role]:
    st.sidebar.markdown(f"✅ {perm}")

st.sidebar.markdown("---")

# Navegación principal
page = st.sidebar.radio(
    "📍 Navegación:",
    ["🖼️ Generación de Imágenes", "✍️ Edición de Texto", "📁 Proyectos", "👥 Colaboración", "⚙️ Configuración"]
)

# Página principal
st.title("🎨 Creative AI Studio")
st.markdown("*Plataforma integral de creación de contenido con IA*")

# =================== PÁGINA: GENERACIÓN DE IMÁGENES ===================
if page == "🖼️ Generación de Imágenes":
    if user_role not in ["diseñador", "administrador"]:
        st.warning("⚠️ No tienes permisos para generar imágenes.")
    else:
        st.header("🖼️ Generador de Imágenes con IA")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input para descripción de imagen
            prompt = st.text_area(
                "📝 Describe la imagen que quieres generar:",
                placeholder="Ej: Un gato naranja saltando sobre un río cristalino en un bosque mágico",
                height=100
            )
            
            # Selector de estilo
            style = st.selectbox("🎨 Estilo de imagen:", STYLE_PRESETS)
            
            # Configuraciones avanzadas en un expander
            with st.expander("⚙️ Configuraciones Avanzadas"):
                col_a, col_b = st.columns(2)
                with col_a:
                    cfg_scale = st.slider("Precisión del prompt:", 1, 20, 10)
                    steps = st.slider("Pasos de generación:", 10, 100, 50)
                with col_b:
                    width = st.selectbox("Ancho:", [512, 768, 1024], index=1)
                    height = st.selectbox("Alto:", [512, 768, 1024], index=1)
            
            # Botón para generar
            if st.button("🎨 Generar Imagen", type="primary"):
                if prompt.strip():
                    with st.spinner("Generando imagen... ⏳"):
                        image = generate_image(prompt, style)
                        if image:
                            # Guardar en historial
                            image_data = {
                                "image": image,
                                "prompt": prompt,
                                "style": style,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "user": user_role
                            }
                            st.session_state.generated_images.append(image_data)
                            st.success("✅ ¡Imagen generada exitosamente!")
                else:
                    st.warning("⚠️ Por favor, escribe una descripción para la imagen.")
        
        with col2:
            st.markdown("### 🛡️ Políticas de Uso Ético")
            st.info("""
            **Pautas importantes:**
            - No generar contenido ofensivo o inapropiado
            - Respetar derechos de autor y marcas registradas
            - Usar para fines creativos y profesionales
            - Evitar contenido que pueda ser dañino
            """)
        
        # Mostrar última imagen generada
        if st.session_state.generated_images:
            st.markdown("---")
            st.subheader("🖼️ Última Imagen Generada")
            
            latest = st.session_state.generated_images[-1]
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(latest["image"], caption=f"Prompt: {latest['prompt']}")
            
            with col2:
                st.markdown(f"**Estilo:** {latest['style']}")
                st.markdown(f"**Creado:** {latest['timestamp']}")
                st.markdown(f"**Usuario:** {latest['user']}")
                
                # Botón de descarga
                img_buffer = io.BytesIO()
                latest["image"].save(img_buffer, format='PNG')
                st.download_button(
                    label="⬇️ Descargar",
                    data=img_buffer.getvalue(),
                    file_name=f"imagen_{latest['timestamp'].replace(':', '-')}.png",
                    mime="image/png"
                )
        
        # Galería de imágenes
        if st.session_state.generated_images:
            st.markdown("---")
            st.subheader("🖼️ Galería de Imágenes")
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_style = st.selectbox("Filtrar por estilo:", ["Todos"] + STYLE_PRESETS)
            with col2:
                filter_user = st.selectbox("Filtrar por usuario:", ["Todos", "diseñador", "redactor", "administrador"])
            
            # Mostrar imágenes en grid
            images_to_show = st.session_state.generated_images
            if filter_style != "Todos":
                images_to_show = [img for img in images_to_show if img["style"] == filter_style]
            if filter_user != "Todos":
                images_to_show = [img for img in images_to_show if img["user"] == filter_user]
            
            if images_to_show:
                cols = st.columns(3)
                for idx, img_data in enumerate(reversed(images_to_show)):
                    with cols[idx % 3]:
                        st.image(img_data["image"], caption=img_data["prompt"][:50] + "...")
                        st.caption(f"Estilo: {img_data['style']} | {img_data['timestamp']}")

# =================== PÁGINA: EDICIÓN DE TEXTO ===================
elif page == "✍️ Edición de Texto":
    if user_role not in ["redactor", "administrador"]:
        st.warning("⚠️ No tienes permisos para editar texto.")
    else:
        st.header("✍️ Editor de Texto con IA")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input de texto
            original_text = st.text_area(
                "📝 Texto a editar:",
                placeholder="Escribe o pega aquí el texto que quieres mejorar...",
                height=200
            )
            
            # Opciones de edición
            operation = st.selectbox(
                "🔧 Tipo de edición:",
                ["improve", "summarize", "expand", "correct", "creative"],
                format_func=lambda x: {
                    "improve": "Mejorar texto",
                    "summarize": "Resumir",
                    "expand": "Expandir",
                    "correct": "Corregir errores",
                    "creative": "Reescribir creativamente"
                }[x]
            )
            
            # Botón para procesar
            if st.button("✨ Procesar Texto", type="primary"):
                if original_text.strip():
                    with st.spinner("Procesando texto... ⏳"):
                        edited_text = edit_text_with_claude(original_text, operation)
                        
                        # Guardar en historial
                        text_entry = {
                            "original": original_text,
                            "edited": edited_text,
                            "operation": operation,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user": user_role
                        }
                        st.session_state.text_history.append(text_entry)
                        
                        st.success("✅ ¡Texto procesado exitosamente!")
                else:
                    st.warning("⚠️ Por favor, ingresa un texto para editar.")
        
        with col2:
            st.markdown("### 📋 Guías de Estilo")
            st.info("""
            **Mejores prácticas:**
            - Usa lenguaje claro y conciso
            - Mantén el tono apropiado
            - Verifica la precisión factual
            - Evita contenido sesgado
            """)
        
        # Mostrar resultado de la última edición
        if st.session_state.text_history:
            st.markdown("---")
            st.subheader("📝 Resultado de la Edición")
            
            latest = st.session_state.text_history[-1]
            
            # Mostrar antes y después
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Texto Original:**")
                st.text_area("", value=latest["original"], height=150, disabled=True)
            
            with col2:
                st.markdown("**✨ Texto Editado:**")
                edited_area = st.text_area("", value=latest["edited"], height=150, key="edited_text")
                
                # Botón para copiar
                if st.button("📋 Copiar al portapapeles"):
                    st.info("Usa Ctrl+A y Ctrl+C para copiar el texto editado")
            
            st.markdown(f"**Operación:** {latest['operation']} | **Fecha:** {latest['timestamp']} | **Usuario:** {latest['user']}")
        
        # Historial de ediciones
        if st.session_state.text_history:
            st.markdown("---")
            st.subheader("📚 Historial de Ediciones")
            
            for idx, entry in enumerate(reversed(st.session_state.text_history)):
                with st.expander(f"Edición {len(st.session_state.text_history) - idx} - {entry['operation']} ({entry['timestamp']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.text(entry["original"][:200] + "..." if len(entry["original"]) > 200 else entry["original"])
                    with col2:
                        st.markdown("**Editado:**")
                        st.text(entry["edited"][:200] + "..." if len(entry["edited"]) > 200 else entry["edited"])

# =================== PÁGINA: PROYECTOS ===================
elif page == "📁 Proyectos":
    st.header("📁 Gestión de Proyectos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Crear nuevo proyecto
        st.subheader("➕ Nuevo Proyecto")
        project_name = st.text_input("Nombre del proyecto:")
        project_desc = st.text_area("Descripción del proyecto:")
        
        if st.button("🚀 Crear Proyecto"):
            if project_name:
                st.session_state.projects[project_name] = {
                    "description": project_desc,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "creator": user_role,
                    "images": [],
                    "texts": [],
                    "comments": []
                }
                st.success(f"✅ Proyecto '{project_name}' creado exitosamente!")
            else:
                st.warning("⚠️ Por favor, ingresa un nombre para el proyecto.")
    
    with col2:
        st.markdown("### 💡 Consejos")
        st.info("""
        **Organización efectiva:**
        - Usa nombres descriptivos
        - Agrupa contenido relacionado
        - Documenta el progreso
        - Colabora con tu equipo
        """)
    
    # Mostrar proyectos existentes
    if st.session_state.projects:
        st.markdown("---")
        st.subheader("📂 Proyectos Existentes")
        
        for name, project in st.session_state.projects.items():
            with st.expander(f"📁 {name}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Descripción:** {project['description']}")
                    st.markdown(f"**Creado:** {project['created']} por {project['creator']}")
                    
                    # Mostrar estadísticas
                    st.markdown(f"📊 **Estadísticas:**")
                    st.markdown(f"- Imágenes: {len(project['images'])}")
                    st.markdown(f"- Textos: {len(project['texts'])}")
                    st.markdown(f"- Comentarios: {len(project['comments'])}")
                
                with col2:
                    # Agregar comentario
                    comment = st.text_input(f"Comentario para {name}:", key=f"comment_{name}")
                    if st.button(f"💬 Agregar", key=f"btn_{name}"):
                        if comment:
                            project['comments'].append({
                                "text": comment,
                                "user": user_role,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success("Comentario agregado!")
                
                # Mostrar comentarios
                if project['comments']:
                    st.markdown("**💬 Comentarios:**")
                    for comment in project['comments']:
                        st.markdown(f"- *{comment['text']}* - {comment['user']} ({comment['timestamp']})")

# =================== PÁGINA: COLABORACIÓN ===================
elif page == "👥 Colaboración":
    st.header("👥 Herramientas de Colaboración")
    
    # Simulación de usuarios activos
    active_users = ["Ana (diseñadora)", "Carlos (redactor)", "María (aprobadora)"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat de Equipo")
        
        # Mostrar mensajes simulados
        if "team_messages" not in st.session_state:
            st.session_state.team_messages = [
                {"user": "Ana", "message": "He subido las nuevas imágenes del proyecto", "time": "10:30"},
                {"user": "Carlos", "message": "Revisando el contenido de texto", "time": "10:45"},
                {"user": "María", "message": "Todo listo para aprobación", "time": "11:00"}
            ]
        
        # Mostrar chat
        for msg in st.session_state.team_messages:
            st.markdown(f"**{msg['user']}** ({msg['time']}): {msg['message']}")
        
        # Nuevo mensaje
        new_message = st.text_input("Escribe un mensaje:")
        if st.button("📤 Enviar") and new_message:
            st.session_state.team_messages.append({
                "user": user_role.capitalize(),
                "message": new_message,
                "time": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col2:
        st.subheader("👥 Usuarios Activos")
        for user in active_users:
            st.markdown(f"🟢 {user}")
        
        st.markdown("---")
        st.subheader("📋 Tareas Pendientes")
        tasks = [
            "Revisar imágenes del proyecto A",
            "Aprobar contenido de marketing",
            "Generar variaciones de texto"
        ]
        for task in tasks:
            st.checkbox(task)

# =================== PÁGINA: CONFIGURACIÓN ===================
elif page == "⚙️ Configuración":
    if user_role != "administrador":
        st.warning("⚠️ Solo los administradores pueden acceder a la configuración.")
    else:
        st.header("⚙️ Configuración del Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛡️ Seguridad y Privacidad")
            
            # Configuraciones de seguridad
            encrypt_data = st.checkbox("Cifrar datos almacenados", value=True)
            moderate_content = st.checkbox("Activar moderación de contenido", value=True)
            audit_log = st.checkbox("Registrar auditoría de actividades", value=True)
            
            st.markdown("---")
            st.subheader("🎨 Configuración de IA")
            
            # Límites y configuraciones
            max_images_per_user = st.slider("Máximo imágenes por usuario/día:", 1, 100, 20)
            max_text_length = st.slider("Máximo caracteres por texto:", 1000, 10000, 5000)
            
        with col2:
            st.subheader("👥 Gestión de Usuarios")
            
            # Simulación de usuarios
            users_data = [
                {"name": "Ana García", "role": "diseñador", "status": "Activo"},
                {"name": "Carlos López", "role": "redactor", "status": "Activo"},
                {"name": "María Rodríguez", "role": "aprobador", "status": "Inactivo"},
            ]
            
            for user in users_data:
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.write(user["name"])
                with col_b:
                    st.write(user["role"])
                with col_c:
                    color = "🟢" if user["status"] == "Activo" else "🔴"
                    st.write(f"{color} {user['status']}")
            
            st.markdown("---")
            st.subheader("📊 Estadísticas de Uso")
            
            # Métricas simuladas
            st.metric("Imágenes generadas hoy", "47", "12")
            st.metric("Textos editados hoy", "23", "5")
            st.metric("Usuarios activos", "8", "2")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🎨 Creative AI Studio | Desarrollado con Amazon Bedrock y Streamlit<br>
        <small>Uso ético y responsable de IA generativa</small>
    </div>
    """, 
    unsafe_allow_html=True
)