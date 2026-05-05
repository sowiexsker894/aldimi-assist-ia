workspace "ALDIMI" "Proyecto IA - Ecosistema de Gestión Inteligente" {

    model {
        user = person "Operador ALDIMI" "Voluntario o administrador del albergue que gestiona pacientes y suministros."
        
        aldimi = softwareSystem "ALDIMI-Assist" "Sistema inteligente para la automatización de carga documental y soporte conversacional." {
            
            // Interfaces de Usuario
            webApp = container "SPA Application" "Interfaz administrativa para gestión de datos y reportes." "Angular" {
                tags "webapp"
            }
            
            // Núcleo del Sistema
            coreBackend = container "Core Backend" "Orquestador de lógica de negocio y comunicación entre módulos." "Python (FastAPI)" {
                description "Centraliza las peticiones de las apps, coordina los servicios de IA y gestiona la persistencia."
            }
            
            // Módulos de IA
            visionModule = container "Vision Module" "Servicio de Visión Artificial para OCR y clasificación." "Python (PyTorch/Tesseract)" {
                description "Extrae texto de DNI, recetas y boletas. Clasifica el tipo de documento automáticamente."
                tags "ia_service"
            }
            nlpModule = container "NLP Module" "Servicio de procesamiento de lenguaje natural." "Python (LangChain/Spacy)" {
                description "Chatbot de soporte basado en reglamentos y análisis de sentimiento de reportes psicosociales."
                tags "ia_service"
            }
            
            // Persistencia
            database = container "Database" "Almacena perfiles de niños, inventarios y datos procesados." "PostgreSQL" {
                tags "db"
            }
            logsDb = container "Knowledge & Logs DB" "Almacena historial de chats y base de conocimientos (Ontología)." "MongoDB" {
                tags "db"
            }
            
            // --- Relaciones ---
            user -> webApp "Usa para gestión administrativa"
            
            webApp -> coreBackend "Consume servicios mediante API REST"

            
            coreBackend -> visionModule "Envía imágenes para extracción de datos (OCR)"
            coreBackend -> nlpModule "Envía consultas y reportes para análisis"
            
            coreBackend -> database "Lee/Escribe datos maestros de ALDIMI"
            nlpModule -> logsDb "Consulta base de conocimientos y guarda historial"
            visionModule -> database "Persiste metadatos de documentos procesados"
        }
    }
    
    views {
        systemContext aldimi "Contexto_ALDIMI" {
            include *
            autolayout tb
        }

        container aldimi "Contenedores_ALDIMI" {
            include *
            autolayout tb
        }
        
        theme default
        styles {
            element "mobile" {
                shape MobileDeviceLandscape
            }
            element "webapp" {
                shape WebBrowser
            }
            element "ia_service" {
                shape Hexagon
                background yellow
                color #000000
            }
            element "db" {
                shape Cylinder
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}