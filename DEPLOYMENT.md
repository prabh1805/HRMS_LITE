# Deployment Guide - Render.com

This guide will help you deploy HRMSLite to Render.com with PostgreSQL database, backend API, and frontend.

## Prerequisites

1. A [Render.com](https://render.com) account (free tier available)
2. Your GitHub repository: https://github.com/prabh1805/HRMS_LITE.git
3. Git installed locally

## Deployment Steps

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `hrms-lite-db`
   - **Database**: `hrms_lite`
   - **User**: `hrms_user` (auto-generated)
   - **Region**: Oregon (or closest to you)
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for database to be created (takes 1-2 minutes)
6. **Important**: Copy the **Internal Database URL** (starts with `postgres://`)

### Step 2: Deploy Backend API

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `prabh1805/HRMS_LITE`
3. Configure:
   - **Name**: `hrms-lite-api`
   - **Region**: Oregon (same as database)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   DATABASE_URL = <paste Internal Database URL from Step 1>
   DEBUG = false
   APP_NAME = HRMSLite
   VERSION = 0.1.0
   CORS_ORIGINS = https://hrms-lite-frontend.onrender.com
   ```
   
   **Note**: Update `CORS_ORIGINS` with your actual frontend URL after Step 3

5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes for first deploy)
7. Once deployed, copy your backend URL (e.g., `https://hrms-lite-api.onrender.com`)

### Step 3: Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository: `prabh1805/HRMS_LITE`
3. Configure:
   - **Name**: `hrms-lite-frontend`
   - **Region**: Oregon
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Plan**: Free

4. **Environment Variables**:
   ```
   VITE_API_BASE_URL = <paste backend URL from Step 2>/api
   ```
   Example: `https://hrms-lite-api.onrender.com/api`

5. Click **"Create Static Site"**
6. Wait for deployment (3-5 minutes)
7. Once deployed, you'll get your frontend URL (e.g., `https://hrms-lite-frontend.onrender.com`)

### Step 4: Update CORS Settings

1. Go back to your **Backend Service** (`hrms-lite-api`)
2. Click **"Environment"** in the left sidebar
3. Update the `CORS_ORIGINS` variable with your frontend URL:
   ```
   CORS_ORIGINS = https://hrms-lite-frontend.onrender.com
   ```
4. Click **"Save Changes"**
5. Backend will automatically redeploy

### Step 5: Seed Database (Optional)

To populate your database with sample data:

1. Go to your **Backend Service** dashboard
2. Click **"Shell"** in the left sidebar
3. Run the seed script:
   ```bash
   python seed_data.py
   ```
4. This will create 100 employees with 30 days of attendance data

### Step 6: Test Your Application

1. Open your frontend URL: `https://hrms-lite-frontend.onrender.com`
2. Navigate through:
   - Dashboard (should show stats)
   - Employees (add/edit/delete employees)
   - Attendance (mark attendance)

## Important Notes

### Free Tier Limitations

- **Database**: 
  - 1 GB storage
  - Expires after 90 days (backup your data!)
  - Limited connections

- **Backend**:
  - Spins down after 15 minutes of inactivity
  - First request after spin-down takes 30-60 seconds
  - 750 hours/month free

- **Frontend**:
  - 100 GB bandwidth/month
  - Always active (no spin-down)

### Custom Domain (Optional)

1. Go to your service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Add your domain and follow DNS instructions

### Monitoring

- **Logs**: Each service has a "Logs" tab for debugging
- **Metrics**: View CPU, memory, and bandwidth usage
- **Events**: See deployment history and status

## Troubleshooting

### Backend won't start

**Check logs for:**
- Database connection errors → Verify DATABASE_URL
- Migration errors → Check Alembic configuration
- Port binding errors → Ensure using `$PORT` variable

**Solution:**
```bash
# In Shell tab of backend service
alembic upgrade head
```

### Frontend can't connect to backend

**Check:**
1. VITE_API_BASE_URL is correct (includes `/api`)
2. CORS_ORIGINS in backend includes frontend URL
3. Backend is running (check status)

**Solution:**
- Redeploy frontend after updating env vars
- Check browser console for CORS errors

### Database connection timeout

**Render free tier databases sleep after inactivity**

**Solution:**
- First request will be slow (30-60s)
- Consider upgrading to paid tier for production

### Build failures

**Common issues:**
- Missing dependencies → Check requirements.txt / package.json
- Python version mismatch → Render uses Python 3.7 by default
- Node version issues → Add `.node-version` file

**Solution:**
```bash
# Add to backend/.python-version
3.13.0

# Add to frontend/.node-version  
18
```

## Updating Your Deployment

### Automatic Deploys

Render automatically deploys when you push to `main` branch:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Deploy

1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Rollback

1. Go to **"Events"** tab
2. Find previous successful deploy
3. Click **"Rollback to this version"**

## Environment Variables Reference

### Backend
```env
DATABASE_URL=postgres://user:pass@host:5432/dbname
DEBUG=false
APP_NAME=HRMSLite
VERSION=0.1.0
CORS_ORIGINS=https://your-frontend.onrender.com
```

### Frontend
```env
VITE_API_BASE_URL=https://your-backend.onrender.com/api
```

## Cost Optimization

### Free Tier Strategy
- Use free tier for development/demo
- Backend spins down when inactive (acceptable for demos)
- Database expires in 90 days (backup regularly)

### Paid Tier Benefits ($7-25/month)
- No spin-down (always responsive)
- More resources (CPU/RAM)
- Persistent database
- Better for production use

## Backup Strategy

### Database Backup

1. Go to database dashboard
2. Click **"Backups"** tab
3. Click **"Create Backup"**
4. Download backup file

### Automated Backups (Paid tier only)
- Daily automatic backups
- Point-in-time recovery
- 7-day retention

## Security Checklist

- [ ] Change default SECRET_KEY in production
- [ ] Set DEBUG=false
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (automatic on Render)
- [ ] Restrict CORS_ORIGINS to your domain only
- [ ] Regular database backups
- [ ] Monitor logs for suspicious activity

## Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. ✅ Set up monitoring/alerts
3. ✅ Configure custom domain (optional)
4. ✅ Set up regular database backups
5. ✅ Add authentication (future enhancement)
6. ✅ Implement analytics (future enhancement)

---

**Deployed URLs:**
- Frontend: `https://hrms-lite-frontend.onrender.com`
- Backend API: `https://hrms-lite-api.onrender.com`
- API Docs: `https://hrms-lite-api.onrender.com/docs`
