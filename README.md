# 🏥 ALDIMI-Assist | Intelligent Comprehensive Support Assistant

> Project for the **1ASI0404 – Artificial Intelligence** course (UPC, 2026-10 term).
> AI solution for Divina Misericordia Shelter (ALDIMI), developed as part of the **ALDIMI Core AI** ecosystem.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Milestone%201-yellow)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

---

## 📑 Table of Contents

1. [About the Project](#-about-the-project)
2. [SDG Alignment](#-sdg-alignment)
3. [Architecture](#-architecture)
4. [Technology Stack](#-technology-stack)
5. [Repository Structure](#-repository-structure)
6. [Team and Roles](#-team-and-roles)
7. [Work Methodology](#-work-methodology)
8. [Milestones and Progress](#-milestones-and-progress)
9. [How to Run the Project](#-how-to-run-the-project)
10. [Git Conventions](#-git-conventions)
11. [Deliverables](#-deliverables)

---

## 🎯 About the Project

Since 2004, ALDIMI has been a nonprofit organization providing comprehensive, free care to children and adolescents with cancer who live in extreme poverty. As part of its **ALDIMI 2.0** expansion (increasing its capacity from 50 to 100 families), its current manual processes are becoming unsustainable.

**ALDIMI-Assist** is an intelligent assistant designed to automate:

- 📄 **Document processing** through Computer Vision (OCR and classification of national ID cards, prescriptions, and receipts).
- 💬 **Conversational support** through NLP (a chatbot based on organizational guidelines and care guides).
- 🚨 **Early psychosocial risk detection** through sentiment analysis.
- 🔌 **Integration** with predictive Machine Learning models through a REST API.

---

## 🌍 SDG Alignment

| SDG | Target | Project Contribution |
|-----|--------|----------------------|
| **SDG 3 – Good Health and Well-being** | 3.4 (mental health and well-being) | Reduces medical transcription errors and identifies early psychosocial warning signs. |
| **SDG 10 – Reduced Inequalities** | 10.2 (social inclusion) | Provides accessible conversational interfaces for people with limited digital literacy. |

---

## 🏗 Architecture

```text
┌─────────────────┐      ┌──────────────────┐      ┌───────────────────┐
│   GUI Frontend  │ ───► │   API (FastAPI)  │ ───► │   AI Models       │
│  (React/Vue)    │ ◄─── │   /docs (Swagger)│ ◄─── │  (Vision + NLP)   │
└─────────────────┘      └──────────────────┘      └───────────────────┘
                                  │
                                  ▼
                   ┌─────────────────────────────────┐
                   │  PostgreSQL (profiles)          │
                   │  MongoDB (conversation logs)    │
                   └─────────────────────────────────┘
                                  │
                                  ▼
                   ┌─────────────────────────────────┐
                   │  ML Course (1ACC0057)            │
                   │  Predictive Dashboard            │
                   └─────────────────────────────────┘
```

> Detailed diagram available in [`/docs/arquitectura.md`](./docs/arquitectura.md).

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| **Main Language** | Python 3.9+ |
| **Computer Vision** | OpenCV, Tesseract OCR / EasyOCR, PyTorch |
| **NLP** | spaCy, NLTK, sentence-transformers, LangChain |
| **Backend / API** | FastAPI |
| **Database** | PostgreSQL (structured data) + MongoDB (logs) |
| **Frontend** | React / Streamlit (to be decided in Milestone 2) |
| **SCRUM Management** | Jira / Trello |
| **Version Control** | Git + GitHub |

---

## 📂 Repository Structure

> Follows the mandatory structure defined in Section 12 of the course assignment.

```text
aldimi-assist-ia/
│
├── README.md                       ← This file
├── .gitignore
├── requirements.txt                ← Python dependencies
│
├── codigo/                         ← Source code (required structure)
│   ├── frontend/                   ← Graphical user interface (GUI)
│   │   └── README.md
│   ├── backend/                    ← REST API built with FastAPI
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── tests/
│   │   └── README.md
│   └── ia_models/                  ← Computer Vision and NLP models
│       ├── vision/
│       │   ├── ocr/
│       │   └── classifier/
│       ├── nlp/
│       │   ├── chatbot/
│       │   ├── ontology/
│       │   └── sentiment/
│       └── README.md
│
├── datos/                          ← Datasets (anonymized)
│   ├── raw/                        ← Raw data
│   ├── processed/                  ← Processed data
│   ├── synthetic/                  ← Synthetically generated datasets
│   └── README.md                   ← Documents each dataset and its license
│
├── docs/                           ← Documentation
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
└── notebooks/                      ← Jupyter / Colab (experimentation)
    ├── 01_eda_dataset.ipynb
    ├── 02_ocr_baseline.ipynb
    └── 03_classifier_training.ipynb
```

> ⚠️ **Important:** For submission, compress only `/codigo`, `/datos`, and `/docs` using the format `TP_1ASI404_NRC_GRUPO_##.zip` or `TF_1ASI404_NRC_GRUPO_##.zip`.

---

## 👥 Team and Roles

Team composition follows Section 9 of the course assignment (4–5 members with SCRUM roles):

| Member | Role | Main Responsibility | Contact |
|--------|------|---------------------|---------|
| [Name 1] | **Scrum Master** | Methodology coordination and liaison with the Machine Learning team. | @username |
| [Name 2] | **AI Engineer (NLP)** | Chatbot, semantic search, ontology, and sentiment analysis. | @username |
| [Name 3] | **AI Engineer (Vision)** | OCR, document classification, and image preprocessing. | @username |
| [Name 4] | **Fullstack / Integration Developer** | GUI, REST API, database connectivity, and integration with the ML course. | @username |
| [Name 5] | **Product Owner / QA** *(optional)* | Backlog management, prioritization, and functional testing with volunteers. | @username |

> All team members participate in code reviews and daily stand-ups. Each role represents a primary area of responsibility, not an exclusive one.

---

## 🔄 Work Methodology

### CRISP-DM (AI Model Lifecycle)

1. ✅ Business Understanding *(Milestone 1)*
2. 🟡 Data Understanding *(Milestone 1, in progress)*
3. 🔲 Data Preparation *(Milestone 2)*
4. 🔲 Modeling *(Milestones 2–3)*
5. 🔲 Evaluation *(Milestone 3)*
6. 🔲 Deployment *(Milestone 4)*

### SCRUM (Development Management)

- **Sprint duration:** 2 weeks
- **Ceremonies:**
  - Sprint Planning (Monday, at the start of the sprint)
  - Daily Stand-up (15 minutes, Monday / Wednesday / Friday)
  - Sprint Review (Friday, at the end of the sprint)
  - Retrospective (Friday, at the end of the sprint)
- **Board:** [Jira/Trello board link](#)

### Definition of Done (DoD)

A user story is considered "Done" when:

- ✔ The code passes unit tests.
- ✔ It is documented (docstring + module README).
- ✔ It has been reviewed by at least one teammate (approved PR).
- ✔ It meets the user story and its acceptance criteria.
- ✔ It has been merged into `develop`.

---

## 📊 Milestones and Progress

| Milestone | Week | Status | Deliverable |
|-----------|------|--------|-------------|
| **Milestone 1** – Knowledge Analysis and Modeling | 6 | 🟡 In progress | Technical report + ontology + architecture + backlog |
| **Milestone 2** – Midterm Project: Functional Prototype | 7 | 🔲 Pending | Baseline OCR + FAQ chatbot + initial GUI |
| **Milestone 3** – Integration and Refinement | 12 | 🔲 Pending | Classifier + sentiment analysis + API |
| **Milestone 4** – Final Project: Ecosystem | 15 | 🔲 Pending | Complete software + ML integration + demo |

---

## 🚀 How to Run the Project

### Prerequisites

- Python 3.9 or later (for local development without Docker)
- Git
- Docker and Docker Compose (recommended for running the full stack)
- Tesseract OCR ([installation instructions](https://github.com/tesseract-ocr/tesseract)) — only if using OCR outside the container
- PostgreSQL — included in Docker Compose; optional if running backends locally

### Quick Start with Docker Compose

From the repository root:

```bash
docker compose up --build
```

| URL | Description |
|-----|-------------|
| http://localhost:4200 | Web portal (Angular) |
| http://localhost:8000/docs | Central API (Swagger) |

Development login (seed migration 002): `admin@aldimi.local` / `AdminDev123!`

See [src/context/ecosystem/services-map.md](src/context/ecosystem/services-map.md) for details about ports, proxy, and environment variables.

### Clone and Install (Local Development Without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/[username]/aldimi-assist-ia.git
cd aldimi-assist-ia

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate            # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the Backend

```bash
cd codigo/backend
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Swagger documentation: `http://localhost:8000/docs`

---

## 🌿 Git Conventions

### Branches

- `main` → stable version; receives merges from `develop` for releases only.
- `develop` → integration branch for sprint work.
- `feature/<name>` → new features. Example: `feature/ocr-dni`
- `fix/<name>` → bug fixes.
- `docs/<name>` → documentation-only changes.

### Commits (Conventional Commits)

```text
feat: add OCR for Peruvian national ID cards
fix: correct date extraction from prescriptions
docs: update README with installation instructions
test: add tests for the classifier
refactor: reorganize the NLP module
```

### Pull Requests

- Use a clear, descriptive title.
- Describe the changes and include screenshots when applicable.
- At least one reviewer must approve before merging.
- Do not merge directly into `main`.

---

## 📦 Deliverables

### Milestone 2 — Midterm Project (Week 7)

File: `TP_1ASI404_NRC_GRUPO_##.zip`

Contents:

- `/codigo` → functional prototype (OCR + basic chatbot + GUI)
- `/datos` → initial anonymized dataset
- `/docs` → midterm report in PDF format

### Milestone 4 — Final Project (Week 15)

File: `TF_1ASI404_NRC_GRUPO_##.zip`

Contents:

- `/codigo` → complete integrated system
- `/datos` → final anonymized dataset
- `/docs` → final report + user manual + video pitch

---

## 📜 License and Ethical Considerations

This project is developed for academic purposes as part of the **1ASI0404 – Artificial Intelligence** course at Universidad Peruana de Ciencias Aplicadas (UPC).

**Ethical commitments:**

- ✔ Compliance with **Law No. 29733** (Peru's Personal Data Protection Law).
- ✔ Mandatory anonymization of any real data obtained from ALDIMI.
- ✔ Preference for synthetic datasets during model training.
- ✔ Special care when handling data belonging to minors (no storage of identifiable images).
- ✔ Transparency regarding the use of AI models and disclosure of their limitations.

---

## 📞 Contact

**Course:** 1ASI0404 – Artificial Intelligence  
**Section / NRC:** [to be completed]  
**Instructor:** [instructor's name to be completed]  
**University:** Universidad Peruana de Ciencias Aplicadas (UPC)

For internal technical questions, use the team's Slack/Discord channel.

---

<div align="center">

**Made with 💙 by the ALDIMI-Assist team | UPC 2026-10**

*"Technology serving those who need it most."*

</div>
