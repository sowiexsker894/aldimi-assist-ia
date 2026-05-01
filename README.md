# 🏥 ALDIMI-Assist | Asistente Inteligente de Soporte Integral

> Proyecto del curso **1ASI0404 – Inteligencia Artificial** (UPC, ciclo 2026-10)
> Solución de IA para el Albergue Divina Misericordia (ALDIMI), enmarcada en el ecosistema **ALDIMI Core AI**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Hito%201-yellow)
![License](https://img.shields.io/badge/License-Académico-lightgrey)

---

## 📑 Tabla de contenidos

1. [Sobre el proyecto](#-sobre-el-proyecto)
2. [Alineación con los ODS](#-alineación-con-los-ods)
3. [Arquitectura](#-arquitectura)
4. [Stack tecnológico](#-stack-tecnológico)
5. [Estructura del repositorio](#-estructura-del-repositorio)
6. [Equipo y roles](#-equipo-y-roles)
7. [Metodología de trabajo](#-metodología-de-trabajo)
8. [Hitos y avance](#-hitos-y-avance)
9. [Cómo correr el proyecto](#-cómo-correr-el-proyecto)
10. [Convenciones de Git](#-convenciones-de-git)
11. [Entregables](#-entregables)

---

## 🎯 Sobre el proyecto

ALDIMI es una organización sin fines de lucro que desde 2004 brinda atención integral y gratuita a niños y adolescentes con cáncer en situación de extrema pobreza. En el marco de su expansión **ALDIMI 2.0** (de 50 a 100 familias atendidas), los procesos manuales actuales se vuelven insostenibles.

**ALDIMI-Assist** es un asistente inteligente que automatiza:

- 📄 **Carga documental** mediante Visión Artificial (OCR + clasificación de DNI, recetas y boletas).
- 💬 **Soporte conversacional** mediante NLP (chatbot sobre reglamento y guías de cuidado).
- 🚨 **Detección temprana de riesgos psicosociales** mediante análisis de sentimiento.
- 🔌 **Integración** con modelos predictivos del curso de Machine Learning vía API REST.

---

## 🌍 Alineación con los ODS

| ODS | Meta | Aporte del proyecto |
|-----|------|---------------------|
| **ODS 3 – Salud y Bienestar** | 3.4 (salud mental y bienestar) | Reduce errores de transcripción médica y detecta alertas psicosociales tempranas. |
| **ODS 10 – Reducción de Desigualdades** | 10.2 (inclusión social) | Interfaces conversacionales accesibles para personas con baja alfabetización digital. |

---

## 🏗 Arquitectura

```
┌─────────────────┐      ┌──────────────────┐      ┌───────────────────┐
│   GUI Frontend  │ ───► │   API (FastAPI)  │ ───► │  Modelos de IA    │
│  (React/Vue)    │ ◄─── │   /docs (Swagger)│ ◄─── │  (Vision + NLP)   │
└─────────────────┘      └──────────────────┘      └───────────────────┘
                                  │
                                  ▼
                  ┌─────────────────────────────────┐
                  │  PostgreSQL (perfiles)          │
                  │  MongoDB (logs conversacionales)│
                  └─────────────────────────────────┘
                                  │
                                  ▼
                  ┌─────────────────────────────────┐
                  │  Curso ML (1ACC0057)            │
                  │  Dashboard predictivo           │
                  └─────────────────────────────────┘
```

> Diagrama detallado disponible en [`/docs/arquitectura.md`](./docs/arquitectura.md).

---

## 🛠 Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| **Lenguaje principal** | Python 3.9+ |
| **Visión Artificial** | OpenCV, Tesseract OCR / EasyOCR, PyTorch |
| **NLP** | spaCy, NLTK, sentence-transformers, LangChain |
| **Backend / API** | FastAPI |
| **Base de datos** | PostgreSQL (estructurado) + MongoDB (logs) |
| **Frontend** | React / Streamlit (a definir en Hito 2) |
| **Gestión SCRUM** | Jira / Trello |
| **Control de versiones** | Git + GitHub |

---

## 📂 Estructura del repositorio

> Sigue la estructura obligatoria definida en la Sección 12 del enunciado del curso.

```
aldimi-assist-ia/
│
├── README.md                       ← Este archivo
├── .gitignore
├── requirements.txt                ← Dependencias Python
│
├── codigo/                         ← Código fuente (estructura obligatoria)
│   ├── frontend/                   ← Interfaz gráfica (GUI)
│   │   └── README.md
│   ├── backend/                    ← API REST con FastAPI
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── tests/
│   │   └── README.md
│   └── ia_models/                  ← Modelos de Visión y NLP
│       ├── vision/
│       │   ├── ocr/
│       │   └── classifier/
│       ├── nlp/
│       │   ├── chatbot/
│       │   ├── ontology/
│       │   └── sentiment/
│       └── README.md
│
├── datos/                          ← Datasets (anonimizados)
│   ├── raw/                        ← Datos crudos
│   ├── processed/                  ← Datos procesados
│   ├── synthetic/                  ← Datasets generados sintéticamente
│   └── README.md                   ← Documenta cada dataset y su licencia
│
├── docs/                           ← Documentación
│   ├── informe_hito1.pdf
│   ├── informe_hito2.pdf
│   ├── informe_final.pdf
│   ├── manual_usuario.pdf
│   ├── arquitectura.md
│   ├── ontologia.md
│   ├── api_reference.md
│   └── diagramas/
│       ├── as-is.png
│       ├── to-be.png
│       └── arquitectura.png
│
└── notebooks/                      ← Jupyter / Colab (experimentación)
    ├── 01_eda_dataset.ipynb
    ├── 02_ocr_baseline.ipynb
    └── 03_classifier_training.ipynb
```

> ⚠️ **Importante:** Al momento de la entrega, comprimir solo `/codigo`, `/datos` y `/docs` con el formato `TP_1ASI404_NRC_GRUPO_##.zip` o `TF_1ASI404_NRC_GRUPO_##.zip`.

---

## 👥 Equipo y roles

Conformación según la Sección 9 del enunciado (4–5 integrantes con roles SCRUM):

| Integrante | Rol | Responsabilidad principal | Contacto |
|------------|-----|---------------------------|----------|
| [Nombre 1] | **Scrum Master** | Coordinación metodológica y enlace con equipo de Machine Learning. | @usuario |
| [Nombre 2] | **AI Engineer (NLP)** | Chatbot, búsqueda semántica, ontología, análisis de sentimiento. | @usuario |
| [Nombre 3] | **AI Engineer (Vision)** | OCR, clasificación de documentos, preprocesamiento de imágenes. | @usuario |
| [Nombre 4] | **Fullstack / Integration Developer** | GUI, API REST, conexión con BD, integración con curso ML. | @usuario |
| [Nombre 5] | **Product Owner / QA** *(opcional)* | Backlog, priorización, pruebas funcionales con voluntarios. | @usuario |

> Todos los integrantes participan en code reviews y daily stand-ups. La especialización es del rol principal, no excluyente.

---

## 🔄 Metodología de trabajo

### CRISP-DM (ciclo de vida del modelo de IA)

1. ✅ Business Understanding *(Hito 1)*
2. 🟡 Data Understanding *(Hito 1, en curso)*
3. 🔲 Data Preparation *(Hito 2)*
4. 🔲 Modeling *(Hito 2–3)*
5. 🔲 Evaluation *(Hito 3)*
6. 🔲 Deployment *(Hito 4)*

### SCRUM (gestión del desarrollo)

- **Duración del Sprint:** 2 semanas
- **Ceremonias:**
  - Sprint Planning (lunes, inicio de sprint)
  - Daily Stand-up (15 min, lunes / miércoles / viernes)
  - Sprint Review (viernes, fin de sprint)
  - Retrospective (viernes, fin de sprint)
- **Tablero:** [Enlace al tablero Jira/Trello](#)

### Definition of Done (DoD)

Una historia de usuario está "Done" cuando:
- ✔ El código pasa las pruebas unitarias.
- ✔ Está documentado (docstring + README del módulo).
- ✔ Fue revisado por al menos un compañero (PR aprobado).
- ✔ Cumple con la historia de usuario y los criterios de aceptación.
- ✔ Está mergeado a `develop`.

---

## 📊 Hitos y avance

| Hito | Semana | Estado | Entregable |
|------|--------|--------|------------|
| **Hito 1** – Análisis y Modelado del Conocimiento | 6 | 🟡 En curso | Informe técnico + ontología + arquitectura + backlog |
| **Hito 2** – Trabajo Parcial: Prototipo Funcional | 7 | 🔲 Pendiente | OCR base + Chatbot FAQ + GUI inicial |
| **Hito 3** – Integración y Refinamiento | 12 | 🔲 Pendiente | Clasificador + análisis de sentimiento + API |
| **Hito 4** – Trabajo Final: Ecosistema | 15 | 🔲 Pendiente | Software completo + integración con ML + demo |

---

## 🚀 Cómo correr el proyecto

### Requisitos previos

- Python 3.9 o superior
- Git
- Tesseract OCR ([instalar aquí](https://github.com/tesseract-ocr/tesseract))
- PostgreSQL (opcional para local)

### Clonar e instalar

```bash
# 1. Clonar el repositorio
git clone https://github.com/[usuario]/aldimi-assist-ia.git
cd aldimi-assist-ia

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate            # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Levantar el backend

```bash
cd codigo/backend
uvicorn app.main:app --reload
```

API disponible en: `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

---

## 🌿 Convenciones de Git

### Ramas

- `main` → versión estable, solo recibe merges desde `develop` para entregas.
- `develop` → integración del trabajo del sprint.
- `feature/<nombre>` → nuevas funcionalidades. Ej: `feature/ocr-dni`
- `fix/<nombre>` → corrección de bugs.
- `docs/<nombre>` → cambios solo de documentación.

### Commits (Conventional Commits)

```
feat: agrega OCR para DNI peruano
fix: corrige extracción de fecha en recetas
docs: actualiza README con instrucciones de instalación
test: agrega tests para clasificador
refactor: reorganiza módulo de NLP
```

### Pull Requests

- Título claro y descriptivo.
- Descripción del cambio + screenshots si aplica.
- Mínimo 1 reviewer aprobando antes de merge.
- No mergear sobre `main` directamente.

---

## 📦 Entregables

### Hito 2 — Trabajo Parcial (Semana 7)

Archivo: `TP_1ASI404_NRC_GRUPO_##.zip`

Contenido:
- `/codigo` → prototipo funcional (OCR + chatbot básico + GUI)
- `/datos` → dataset inicial anonimizado
- `/docs` → informe parcial en PDF

### Hito 4 — Trabajo Final (Semana 15)

Archivo: `TF_1ASI404_NRC_GRUPO_##.zip`

Contenido:
- `/codigo` → sistema completo integrado
- `/datos` → dataset final anonimizado
- `/docs` → informe final + manual de usuario + video pitch

---

## 📜 Licencia y consideraciones éticas

Este proyecto se desarrolla con fines académicos para el curso **1ASI0404 – Inteligencia Artificial** de la Universidad Peruana de Ciencias Aplicadas (UPC).

**Compromisos éticos:**

- ✔ Cumplimiento de la **Ley N° 29733** (Protección de Datos Personales del Perú).
- ✔ Anonimización obligatoria de cualquier dato real proveniente de ALDIMI.
- ✔ Uso preferente de datasets sintéticos para entrenamiento.
- ✔ Especial cuidado con datos de menores de edad (no almacenamiento de imágenes identificables).
- ✔ Transparencia en el uso de modelos de IA y limitaciones declaradas.

---

## 📞 Contacto

**Curso:** 1ASI0404 – Inteligencia Artificial
**Sección / NRC:** [completar]
**Profesor a cargo:** [completar nombre]
**Universidad:** Universidad Peruana de Ciencias Aplicadas (UPC)

Para dudas técnicas internas del equipo, usar el canal de Slack/Discord del grupo.

---

<div align="center">

**Hecho con 💙 por el equipo ALDIMI-Assist | UPC 2026-10**

*"Tecnología al servicio de quienes más lo necesitan."*

</div>
