# Deployment Guide for Render

This guide will help you deploy your EstateVision AI Property Video Generator to Render.

## Prerequisites

1. Sign up for a Render account at https://render.com
2. Have your API keys ready:
   - Google Gemini API Key
   - OpenAI API Key (if using)
3. Fork or connect your GitHub repository to Render

## Deployment Steps

### Automatic Deployment via GitHub Push

Your application is configured for automatic deployment when you push changes to your GitHub repository. The `render.yaml` files in your project root and in the client directory contain the `autoDeploy: true` setting, which will trigger a new deployment every time you push to your connected GitHub branch.

To set this up:
1. Connect your GitHub repository to Render
2. Select the branch you want to deploy from (typically main or master)
3. Render will automatically deploy your services and redeploy on every push

### 1. Deploy the Backend Service

1. Log into your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect to your GitHub repository
4. Choose the branch you want to deploy (typically main or master)
5. Fill in the following details:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Select your preferred region
6. Add the following environment variables:
   - `SECRET_KEY`: Generate a strong secret key
   - `GOOGLE_GEMINI_API_KEY`: Your Google Gemini API key
   - `OPENAI_API_KEY`: Your OpenAI API key (if applicable)
   - `DATABASE_URL`: Will be auto-generated if using Render's database
   - `CORS_ORIGINS`: Set to `["https://your-frontend-url.onrender.com"]` (update with your frontend URL after deployment)
7. Give your service a name (e.g., `estatevision-ai-backend`)
8. Click "Create Web Service"

### 2. Deploy the Frontend Service

1. In your Render dashboard, click "New +" and select "Static Site" (or "Web Service" if you prefer to build on Render)
2. Connect to your GitHub repository
3. Choose the branch you want to deploy
4. Fill in the following details:
   - **Environment**: Static
   - **Build Command**: 
     ```
     cd client/estatevision-ai---professional-property-video-generator &&
     npm install &&
     npm run build
     ```
   - **Publish Directory**: `client/estatevision-ai---professional-property-video-generator/dist`
5. Add the following environment variables:
   - `VITE_API_URL`: Set to your backend URL (e.g., `https://estatevision-ai-backend.onrender.com`)
   - `GEMINI_API_KEY`: Your Google Gemini API key (if needed client-side)
6. Give your service a name (e.g., `estatevision-ai-frontend`)
7. Click "Create Web Service"

### 3. Alternative: Using Render Blueprint (Recommended)

Instead of manually creating services, you can use the `render.yaml` file in the root of your project:

1. In your GitHub repository, make sure the `render.yaml` file exists in the root directory
2. In your Render dashboard, click "New +" and select "Blueprint Stack"
3. Connect to your GitHub repository
4. Render will automatically read the `render.yaml` file and create all necessary services
5. You'll be able to review and modify the configuration before deployment
6. Complete the setup by providing the required environment variables

## Post-Deployment Steps

1. After the backend is deployed, update the frontend's `VITE_API_URL` environment variable with the backend's URL
2. Redeploy the frontend to pick up the new backend URL
3. Test the application by visiting the frontend URL
4. Log in with the default admin credentials (if they were created during deployment)

## Environment Variables Reference

### Backend Service
- `SECRET_KEY`: Secret key for JWT tokens (generate a strong random key)
- `GOOGLE_GEMINI_API_KEY`: Your Google Gemini API key
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI TTS)
- `DATABASE_URL`: PostgreSQL connection string (auto-generated with Render database)
- `CORS_ORIGINS`: JSON array of allowed origins (e.g., `["https://your-frontend.onrender.com"]`)

### Frontend Service
- `VITE_API_URL`: The URL of your backend service (e.g., `https://estatevision-ai-backend.onrender.com`)
- `GEMINI_API_KEY`: Your Google Gemini API key (if needed client-side)

## Troubleshooting

1. **CORS errors**: Make sure your `CORS_ORIGINS` environment variable includes your frontend URL
2. **Database connection errors**: Verify that your `DATABASE_URL` is correctly set
3. **API key errors**: Ensure all required API keys are set as environment variables
4. **Build failures**: Check the build logs in Render dashboard for specific error messages

## Scaling

- For increased traffic, you can upgrade your Render services to higher tiers
- Consider using Render's PostgreSQL database for production use
- Monitor your application's performance in the Render dashboard

## Notes

- The application will automatically redeploy when you push changes to your connected GitHub branch
- For security, never commit API keys to your repository
- The application is configured to use SQLite for development but can use PostgreSQL in production