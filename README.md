# ServiceHubAI - Enterprise AI Service Desk Platform

ServiceHubAI is a complete, enterprise-grade multi-tenant SaaS Service Desk platform built using Streamlit, Supabase, and Google Gemini. It offers ticketing, departments, SLA management, interactive analytics, and an integrated RAG (Retrieval-Augmented Generation) Knowledge Base chatbot.

---

## Features

- **Multi-Tenant Isolation**: Organizations register separately and can never see each other's tickets, users, settings, or documents.
- **Role-Based Access Control (RBAC)**: Supports **Super Admin**, **Organization Admin**, **Department Manager**, **Service Desk Agent**, and **Employee**.
- **AI-Powered Copilot**:
  - Automatically summarizes tickets.
  - Predicts ticket categories and priorities.
  - Suggests department routing and resolutions.
  - Finds duplicate or similar past resolved tickets.
- **Enterprise RAG Chatbot**:
  - Upload documents (PDF, DOCX, TXT, CSV, XLSX, PPTX).
  - Parse, chunk, embed (via Gemini Embeddings), and store chunks inside pgvector on Supabase.
  - Conversations retrieve only organization-specific documents with citation confidence.
- **SLA Engine**: Track ticket deadlines with priority-specific resolution SLAs.
- **Interactive Analytics**: Dynamic Plotly visualizers detailing ticket volumes, category distributions, SLA performance, agent productivity, and AI utilization.

---

## Technical Stack

- **Frontend/UI**: Streamlit, `streamlit-option-menu`, `streamlit-aggrid`, Custom HSL Dark Mode CSS
- **Database & Storage**: Supabase PostgreSQL with `pgvector`, Supabase Authentication, Supabase Storage
- **AI & Embeddings**: Google Gemini 2.5 Flash (`gemini-2.5-flash`), Gemini Embeddings (`text-embedding-004`)

---

## Installation & Setup

### 1. Database Setup (Supabase)
1. Create a new project on [Supabase](https://supabase.com/).
2. Enable the `vector` extension in your database settings (enabled automatically by the schema).
3. Open the **SQL Editor** in Supabase and run the content of [schema.sql](file:///d:/3YR/demo/ServiceHubAI/schema.sql) to set up all tables, indexes, constraints, and similarity search functions.

### 2. Storage Setup (Supabase)
Create two public buckets in Supabase Storage:
- `attachments`: For ticket attachments and screenshots.
- `knowledge-base`: For organization document files.

### 3. Local Configuration
1. Clone this repository to your workspace.
2. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```
3. Enter your values:
   - `SUPABASE_URL`: Your project URL.
   - `SUPABASE_ANON_KEY`: Your project's API key.
   - `SUPABASE_SERVICE_ROLE_KEY`: Service role secret (used securely for admin actions, e.g., inviting users).
   - `GEMINI_API_KEY`: Google Gemini API key.

### 4. Install Dependencies
Ensure you have Python 3.10+ installed. Install libraries via:
```bash
pip install -r requirements.txt
```

### 5. Running the Application
Run the Streamlit application:
```bash
streamlit run app.py
```

---

## Deployment (Streamlit Community Cloud)

When deploying to [Streamlit Community Cloud](https://share.streamlit.io/):
1. Push your repository to GitHub.
2. Configure **Secrets** in Streamlit Cloud Dashboard under Settings:
   - Paste the contents of your `.env` file into the Streamlit Secrets box using TOML format:
     ```toml
     SUPABASE_URL = "https://your-project.supabase.co"
     SUPABASE_ANON_KEY = "your-supabase-anon-key"
     SUPABASE_SERVICE_ROLE_KEY = "your-supabase-service-role-key"
     GEMINI_API_KEY = "your-google-gemini-api-key"
     ```
3. Deploy!
