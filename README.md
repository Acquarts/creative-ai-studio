# Creative AI Studio

**Plataforma integral de IA Generativa para creación y edición de contenido empresarial**

## Descripción del Proyecto

Creative AI Studio es una aplicación web desarrollada como parte del Master de IA del Instituto Europeo de Posgrado. La plataforma integra múltiples modelos de inteligencia artificial generativa para crear una solución completa destinada a equipos de marketing, diseño y creación de contenido.

El proyecto resuelve la necesidad empresarial de generar contenido visual y textual de alta calidad de manera eficiente, incorporando flujos de trabajo colaborativos y políticas de uso ético de la IA.

## Objetivos del Proyecto

### Objetivo Principal
Desarrollar una plataforma que permita a diferentes roles de usuario (diseñadores, redactores, aprobadores) colaborar en la creación de contenido utilizando IA generativa de última generación.

### Objetivos Específicos
- Implementar generación de imágenes con control granular de estilos y parámetros
- Proporcionar herramientas de edición de texto inteligente para múltiples propósitos
- Establecer un sistema de roles y permisos para diferentes tipos de usuarios
- Crear flujos de trabajo colaborativos con gestión de proyectos
- Incorporar medidas de seguridad y uso ético de la IA
- Demostrar la integración práctica de servicios de AWS para IA

## Arquitectura Técnica

### Tecnologías Utilizadas

**Frontend y Interface**
- **Streamlit**: Framework principal para la interfaz web
- **Python**: Lenguaje de programación base
- **PIL (Pillow)**: Procesamiento de imágenes
- **JSON**: Manejo de datos estructurados

**Backend y IA**
- **Amazon Bedrock**: Plataforma de IA como servicio
- **Stable Diffusion XL**: Modelo de generación de imágenes
- **Claude v2 (Anthropic)**: Modelo de procesamiento de lenguaje natural
- **boto3**: SDK de AWS para Python

**Infraestructura y Deploy**
- **AWS**: Servicios de nube para IA
- **Streamlit Cloud**: Plataforma de deploy
- **GitHub**: Control de versiones y CI/CD

### Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   AWS Bedrock   │
│   (Streamlit)   │◄──►│   (Python +      │◄──►│                 │
│                 │    │    boto3)        │    │ • Stable Diff.  │
│ • UI Components │    │                  │    │ • Claude v2     │
│ • Session State │    │ • Authentication │    │ • Model APIs    │
│ • Role Mgmt     │    │ • API Calls      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Funcionalidades Principales

### 1. Generación de Imágenes Inteligente

**Características:**
- Conversión de texto a imagen usando Stable Diffusion XL
- 18 estilos predefinidos (anime, fotográfico, digital art, etc.)
- Parámetros configurables:
  - Precisión del prompt (cfg_scale): 1-20
  - Pasos de generación: 10-100
  - Dimensiones: 512x512, 768x768, 1024x1024
- Generación determinística o aleatoria mediante control de seed

**Flujo de Trabajo:**
1. Usuario ingresa descripción textual
2. Selecciona estilo artístico deseado
3. Ajusta parámetros avanzados (opcional)
4. Sistema envía request a Amazon Bedrock
5. Stable Diffusion procesa y genera imagen
6. Imagen se muestra y almacena en galería personal

**Gestión de Resultados:**
- Historial completo de imágenes generadas
- Metadatos: prompt original, estilo, timestamp, usuario
- Sistema de descarga en formato PNG
- Galería filtrable por estilo y usuario
- Previsualización en grid de 3 columnas

### 2. Edición de Contenido Textual

**Capacidades del Sistema:**
- **Mejora de texto**: Optimización de claridad y profesionalismo
- **Resumen inteligente**: Condensación manteniendo puntos clave
- **Expansión de contenido**: Adición de detalles y ejemplos relevantes
- **Corrección gramatical**: Detección y corrección de errores
- **Reescritura creativa**: Transformación estilística del contenido

**Proceso de Edición:**
1. Usuario ingresa texto original
2. Selecciona tipo de operación deseada
3. Claude v2 procesa el contenido según la instrucción
4. Sistema presenta comparación lado a lado (antes/después)
5. Resultado se almacena en historial de ediciones

**Control de Versiones:**
- Historial completo de todas las ediciones
- Comparación visual entre versiones
- Metadatos de cada operación
- Reversión a versiones anteriores
- Trazabilidad por usuario y timestamp

### 3. Sistema de Roles y Permisos

**Arquitectura de Usuarios:**

**Diseñador**
- Generación ilimitada de imágenes
- Acceso a galería completa
- Configuración de parámetros avanzados
- Sin acceso a edición de texto

**Redactor**
- Edición y mejora de contenido textual
- Acceso completo al historial de ediciones
- Herramientas de corrección y reescritura
- Sin acceso a generación de imágenes

**Aprobador**
- Visualización de todo el contenido
- Capacidad de aprobar o rechazar
- Acceso de solo lectura a herramientas de creación
- Gestión de flujos de aprobación

**Administrador**
- Acceso completo a todas las funcionalidades
- Gestión de usuarios y permisos
- Configuración de políticas de seguridad
- Monitoreo y auditoría del sistema

### 4. Colaboración y Gestión de Proyectos

**Sistema de Proyectos:**
- Creación de proyectos con descripción y metadatos
- Asignación de contenido (imágenes/textos) a proyectos específicos
- Seguimiento de progreso y estadísticas
- Gestión de contributors por proyecto

**Herramientas Colaborativas:**
- Chat de equipo en tiempo real
- Sistema de comentarios por proyecto
- Notificaciones de actividad
- Lista de usuarios activos
- Gestión de tareas pendientes

**Flujo de Trabajo Típico:**
1. Administrador crea proyecto nuevo
2. Asigna roles específicos a miembros del equipo
3. Diseñadores generan assets visuales
4. Redactores crean y refinan contenido textual
5. Aprobadores revisan y validan el contenido
6. Proyecto se marca como completado

### 5. Seguridad y Uso Ético

**Políticas de Contenido:**
- Filtros automáticos para contenido inapropiado
- Directrices de uso ético claramente definidas
- Respeto a derechos de autor y marcas registradas
- Prevención de contenido dañino o sesgado

**Medidas de Seguridad:**
- Cifrado de datos almacenados
- Auditoría completa de actividades
- Control de acceso granular
- Protección de credenciales AWS
- Registro de todas las operaciones

**Configuraciones de Administración:**
- Límites por usuario (imágenes/día)
- Restricciones de longitud de texto
- Configuración de parámetros por defecto
- Gestión de políticas de retención

## Casos de Uso Empresariales

### Agencia de Marketing Digital
**Escenario**: Creación de campaña publicitaria multiplataforma
- Diseñadores generan variaciones visuales para diferentes canales
- Redactores adaptan copy para distintas audiencias
- Aprobadores validan coherencia de marca
- Colaboración fluida entre equipos remotos

### Departamento de Contenido Corporativo
**Escenario**: Producción de materiales educativos
- Generación de ilustraciones explicativas
- Adaptación de textos técnicos para diferentes niveles
- Versionado y control de cambios
- Aprobación por expertos técnicos

### Startup de E-commerce
**Escenario**: Creación de contenido para catálogo
- Generación masiva de imágenes de producto
- Optimización de descripciones SEO
- A/B testing de variaciones
- Escalabilidad sin contratación adicional

## Flujo de Datos del Sistema

```
1. Autenticación Usuario → 2. Selección de Rol → 3. Acceso a Funcionalidades

4a. Generación de Imagen:
   Input Text → Bedrock API → Stable Diffusion → Base64 → PIL → Display

4b. Edición de Texto:
   Input Text → Prompt Engineering → Claude API → Response → Comparison View

5. Almacenamiento en Session State → 6. Persistencia en Historial

7. Gestión de Proyectos → 8. Colaboración → 9. Aprobación
```

## Consideraciones Técnicas

### Optimizaciones Implementadas
- **Caching**: Uso de `@st.cache_resource` para cliente Bedrock
- **Session State**: Persistencia de datos durante la sesión
- **Lazy Loading**: Carga de componentes bajo demanda
- **Error Handling**: Manejo robusto de errores API
- **Responsive Design**: Adaptación a diferentes tamaños de pantalla

### Limitaciones Conocidas
- Dependencia de conectividad AWS
- Costos variables según uso de modelos
- Limitaciones de rate limiting de Bedrock
- Almacenamiento temporal (no persistente)
- Región específica requerida (us-east-1)

### Escalabilidad Futura
- Integración con bases de datos persistentes
- Implementación de cache distribuido
- Balanceado de carga para múltiples usuarios
- Integración con servicios de storage (S3)
- API REST para integraciones externas

## Métricas y Evaluación

### KPIs del Sistema
- Tiempo promedio de generación de imagen: ~10-15 segundos
- Precisión de edición de texto: Evaluación cualitativa por usuarios
- Satisfacción de usuario: Medición por encuestas post-uso
- Disponibilidad del sistema: >99% uptime objetivo

### Casos de Prueba
1. **Generación de Imagen**: "Un gato rojo saltando" → Verificar coherencia visual
2. **Edición de Texto**: Mejora de párrafo técnico → Evaluar claridad
3. **Colaboración**: Flujo completo diseñador → redactor → aprobador
4. **Seguridad**: Intento de generación de contenido inapropiado → Bloqueo efectivo

## Instalación y Configuración

### Requisitos del Sistema
- Python 3.9 o superior
- Cuenta AWS con acceso a Bedrock
- Credenciales IAM con permisos específicos
- Acceso a internet estable

### Configuración Mínima AWS
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### Variables de Entorno Requeridas
```
AWS_ACCESS_KEY_ID=<tu_access_key>
AWS_SECRET_ACCESS_KEY=<tu_secret_key>
AWS_DEFAULT_REGION=us-east-1
```

## Conclusiones del Proyecto

Creative AI Studio demuestra la viabilidad técnica y comercial de integrar múltiples servicios de IA generativa en una plataforma empresarial coherente. El proyecto aborda exitosamente los desafíos de:

- **Integración tecnológica** entre diferentes modelos de IA
- **Experiencia de usuario** intuitiva para usuarios no técnicos  
- **Colaboración empresarial** con roles y permisos granulares
- **Uso ético** mediante políticas y controles implementados
- **Escalabilidad técnica** usando arquitectura en la nube

La solución proporciona una base sólida para el desarrollo de aplicaciones empresariales de IA generativa, combinando potencia técnica con facilidad de uso y consideraciones éticas necesarias para adopción empresarial responsable.

## Información del Proyecto Académico

**Institución**: Instituto Europeo de Posgrado  
**Programa**: Master en Inteligencia Artificial  
**Asignatura**: Generative AI  
**Unidad**: 3 - Aplicaciones Prácticas de IA Generativa  
**Enfoque**: Desarrollo de solución empresarial completa

**Objetivos Académicos Cumplidos**:
- Implementación práctica de modelos de IA generativa
- Integración de servicios cloud para IA (AWS Bedrock)
- Desarrollo de interfaces de usuario para IA
- Consideraciones éticas en sistemas de IA
- Gestión de proyectos tecnológicos
- Deploy y operación de aplicaciones de IA
