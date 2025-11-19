# Deployment Guide

This guide covers deploying the AI Interview Assistant to production.

## Overview

The AI Interview Assistant consists of:
- **Frontend**: React + TypeScript (Static Site)
- **Backend**: Python FastAPI (API Server)
- **Database**: ChromaDB (File-based Vector DB)
- **External API**: Groq API (LLM)

## Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) [RECOMMENDED - FREE]

**Pros:**
- ✅ Free tier available
- ✅ Easy setup
- ✅ Auto-deploys from Git
- ✅ HTTPS included

**Cons:**
- ⚠️ Backend sleeps after 15 mins inactivity (free tier)
- ⚠️ Cold start delay (~30 seconds)

#### Step 1: Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-interview-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `PYTHON_VERSION`: 3.10.0
6. Click "Create Web Service"
7. Copy the deployed URL (e.g., `https://ai-interview-backend.onrender.com`)

#### Step 2: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL`: Your Render backend URL (from Step 1)
6. Click "Deploy"
7. Your app will be live at `https://your-project.vercel.app`

---

### Option 2: Railway [RECOMMENDED - EASY]

**Pros:**
- ✅ Deploy both frontend & backend together
- ✅ Free tier: $5 credit/month
- ✅ No cold starts
- ✅ Easy setup

**Cons:**
- ⚠️ Limited free tier

#### Steps:

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your repository
4. Railway will detect both frontend and backend automatically
5. Add Environment Variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `VITE_API_URL`: Will be auto-generated
6. Click "Deploy"
7. Railway will provide URLs for both services

---

### Option 3: DigitalOcean App Platform

**Pros:**
- ✅ Good performance
- ✅ No cold starts
- ✅ Professional hosting

**Cons:**
- ⚠️ Costs $5-12/month
- ⚠️ More complex setup

#### Steps:

1. Create a DigitalOcean account
2. Go to "Apps" → "Create App"
3. Connect GitHub repository
4. Configure Components:
   - **Backend**: Python, `uvicorn api.main:app --host 0.0.0.0 --port 8080`
   - **Frontend**: Static Site, build: `npm run build`, output: `dist`
5. Add environment variables
6. Deploy

---

### Option 4: Self-Hosted VPS (Advanced)

**Pros:**
- ✅ Full control
- ✅ Best performance
- ✅ No vendor lock-in

**Cons:**
- ⚠️ Requires server management skills
- ⚠️ Manual setup and maintenance

#### Requirements:
- Ubuntu 22.04 or similar
- At least 1GB RAM
- Domain name (optional)

#### Quick Setup Script:

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python
sudo apt install python3.10 python3-pip python3-venv -y

# 3. Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 4. Clone repository
git clone https://github.com/jimthereal/ai-interview-assistant.git
cd ai-interview-assistant

# 5. Setup backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Setup frontend
cd frontend
npm install
npm run build
cd ..

# 7. Install Nginx
sudo apt install nginx -y

# 8. Configure Nginx (see nginx.conf below)
sudo nano /etc/nginx/sites-available/ai-interview

# 9. Install SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com

# 10. Setup systemd service (see systemd.service below)
sudo nano /etc/systemd/system/ai-interview.service
sudo systemctl enable ai-interview
sudo systemctl start ai-interview
```

**Nginx Configuration** (`/etc/nginx/sites-available/ai-interview`):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /path/to/ai-interview-assistant/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Systemd Service** (`/etc/systemd/system/ai-interview.service`):
```ini
[Unit]
Description=AI Interview Assistant Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ai-interview-assistant
Environment="PATH=/path/to/ai-interview-assistant/venv/bin"
Environment="GROQ_API_KEY=your_key_here"
ExecStart=/path/to/ai-interview-assistant/venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Environment Variables

**Required for all deployments:**

```env
# Groq API Key (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here

# Frontend Environment (for production build)
VITE_API_URL=https://your-backend-url.com

# Optional: Groq Model Selection
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Pre-Deployment Checklist

- [ ] Test application locally (both frontend and backend running)
- [ ] Verify all features work (Job Analysis, Practice, Progress, Explainer)
- [ ] Check .env.example has all required variables
- [ ] Test with production-like data
- [ ] Verify Groq API key is valid
- [ ] Update CORS settings in backend for production domain
- [ ] Build frontend locally to check for errors: `cd frontend && npm run build`
- [ ] Test backend API endpoints work

---

## CORS Configuration

Update `api/main.py` to allow your production frontend domain:

```python
# Development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Production (add your deployed frontend URL)
origins = [
    "http://localhost:5173",
    "https://your-app.vercel.app",  # Add your frontend URL
    "https://yourdomain.com",
]
```

---

## Database Considerations

**ChromaDB** is file-based and stores data in `data/chroma_db/`:
- ✅ No external database needed
- ✅ Easy deployment
- ⚠️ Data persists in the deployment filesystem
- ⚠️ On free tiers, data may be lost on restart

**Solutions:**
1. **Keep it simple**: Re-initialize DB on each deploy (fast, 150 questions)
2. **Use volume storage**: Mount persistent volume (Render, Railway support this)
3. **Migrate to PostgreSQL + pgvector**: For production-grade persistence

---

## Monitoring & Logs

**Render:**
- View logs in Dashboard → Logs tab
- Check deployment status

**Vercel:**
- View deployment logs in project dashboard
- Monitor function invocations

**Railway:**
- Real-time logs in project view
- Metrics dashboard

**Self-Hosted:**
- View logs: `sudo journalctl -u ai-interview -f`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

---

## Cost Estimates

| Platform | Cost | Pros | Best For |
|----------|------|------|----------|
| **Vercel + Render** | FREE (with limits) | Easy, auto-deploy | Personal projects, MVPs |
| **Railway** | $5-10/month | Simple, reliable | Small projects |
| **DigitalOcean** | $12-24/month | Professional, scalable | Production apps |
| **AWS/GCP/Azure** | $10-50/month | Enterprise-grade | Large scale |
| **VPS (DigitalOcean Droplet)** | $6/month | Full control | Tech-savvy users |

**Note:** Groq API is FREE with generous limits.

---

## Scaling Considerations

**When you have more users:**

1. **Add Redis for caching**:
   - Cache LLM responses
   - Reduce API calls

2. **Use PostgreSQL + pgvector**:
   - More robust than ChromaDB
   - Better for production

3. **Add rate limiting**:
   - Prevent API abuse
   - Protect Groq API quota

4. **Use CDN**:
   - Serve frontend assets faster
   - Reduce server load

5. **Implement user authentication**:
   - Track users individually
   - Personalized experiences

---

## Troubleshooting

**Backend not starting:**
- Check Python version (3.10+)
- Verify all dependencies installed
- Check environment variables set
- Review logs for errors

**Frontend can't connect to backend:**
- Verify `VITE_API_URL` is correct
- Check CORS configuration
- Ensure backend is running
- Check network firewall rules

**ChromaDB errors:**
- Ensure `data/` directory exists
- Check write permissions
- Verify enough disk space

**Groq API errors:**
- Check API key is valid
- Verify not hitting rate limits
- Check internet connectivity

---

## Security Best Practices

1. **Never commit `.env` file**:
   - Already in `.gitignore`
   - Use environment variables in platform

2. **Use HTTPS only**:
   - All major platforms provide this
   - Required for production

3. **Implement rate limiting**:
   - Protect your Groq API quota
   - Prevent abuse

4. **Keep dependencies updated**:
   - Run `pip list --outdated`
   - Update regularly

5. **Add authentication** (future):
   - Implement user login
   - Secure sensitive operations

---

## GitHub Repository Setup

**For clean deployments:**

1. Ensure `.gitignore` includes:
```
.env
node_modules/
__pycache__/
*.pyc
.venv/
venv/
dist/
data/chroma_db/
```

2. Create production branch:
```bash
git checkout -b production
git push origin production
```

3. Deploy from production branch

---

## Support

**Issues during deployment?**
1. Check platform-specific documentation
2. Review logs carefully
3. Test locally first
4. Check GitHub Issues

---

**Last Updated**: November 2025
