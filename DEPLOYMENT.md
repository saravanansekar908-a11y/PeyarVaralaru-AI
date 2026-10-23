# 🚀 Deploying PeyarVaralaru AI on Render

This guide outlines how to deploy the full **PeyarVaralaru AI** application (FastAPI Backend + React Vite Frontend) to **Render** and obtain your public live links.

---

## ⚡ Method 1: 1-Click Render Blueprint (Recommended)

Render Blueprints automatically deploy both the **Python FastAPI Backend** and the **React Vite Static Site** from the repository's [`render.yaml`](./render.yaml).

### Steps:
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** in the top right and select **Blueprint**.
3. Connect your GitHub repository:
   ```text
   https://github.com/saravanansekar908-a11y/PeyarVaralaru-AI
   ```
4. Render will automatically detect [`render.yaml`](./render.yaml) and configure two services:
   - **`peyarvaralaru-web`** (Static Site — Frontend):
     - Build Command: `npm install && npm run build`
     - Publish Directory: `dist`
     - Auto-routes SPA rewrites (`/* -> /index.html`)
     - Assigned URL: `https://peyarvaralaru-web.onrender.com`
   - **`peyarvaralaru-api`** (Web Service — Backend):
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Assigned URL: `https://peyarvaralaru-api.onrender.com`
5. Under Environment Variables for `peyarvaralaru-api`, add your `GEMINI_API_KEY` (optional, for AI features).
6. Click **Apply**.
7. Once deployed, access your live application at:
   - **Frontend App**: `https://peyarvaralaru-web.onrender.com`
   - **Backend API Docs**: `https://peyarvaralaru-api.onrender.com/docs`
   - **API Health Check**: `https://peyarvaralaru-api.onrender.com/api/health`

---

## 🛠️ Method 2: Manual Service Creation

If you prefer deploying services individually:

### 1. Deploy the Backend (Web Service)
1. In Render Dashboard, click **New +** → **Web Service**.
2. Select your repository `saravanansekar908-a11y/PeyarVaralaru-AI`.
3. Configure settings:
   - **Name**: `peyarvaralaru-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `PYTHON_VERSION`: `3.11.9`
   - `GEMINI_API_KEY`: *(your Google Gemini API key)*
5. Click **Create Web Service**.
6. Copy the assigned URL (e.g. `https://peyarvaralaru-api.onrender.com`).

### 2. Deploy the Frontend (Static Site)
1. In Render Dashboard, click **New +** → **Static Site**.
2. Select your repository `saravanansekar908-a11y/PeyarVaralaru-AI`.
3. Configure settings:
   - **Name**: `peyarvaralaru-web`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   - `VITE_API_URL`: `https://peyarvaralaru-api.onrender.com` *(your backend URL)*
5. Under **Redirects/Rewrites**:
   - Add Rewrite Rule: `/*` → `/index.html` (Action: **Rewrite**)
6. Click **Create Static Site**.
7. Visit `https://peyarvaralaru-web.onrender.com`.

---

## 📦 Method 3: All-in-One Single Web Service (Unified)

If you wish to host both frontend and backend under a single Render free web service:
1. In Render Dashboard, click **New +** → **Web Service**.
2. Leave **Root Directory** blank (repository root).
3. Set **Build Command**:
   ```bash
   chmod +x ./render-build.sh && ./render-build.sh
   ```
4. Set **Start Command**:
   ```bash
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. The FastAPI backend automatically detects `frontend/dist` and serves both the API and the React Single Page Application on the same origin.
