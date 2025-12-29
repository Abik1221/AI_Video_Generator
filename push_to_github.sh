#!/bin/bash

# Script to push Render configuration to GitHub

cd /home/nahomkeneni/upwork_projects/chebude_dande

echo "Setting up git configuration..."

# Configure git (replace with your actual name and email)
git config user.email "you@example.com"
git config user.name "Your Name"

echo "Adding all changes..."
git add .

echo "Checking git status..."
git status

echo "Committing changes..."
git commit -m "Configure for Render deployment with auto-deploy
- Updated CORS settings for production
- Added Render deployment configuration
- Removed conflicting deployment workflows
- Configured automatic deployment on push"

echo "Adding remote origin..."
git remote add origin https://github.com/Abik1221/AI_Video_Generator.git

echo "Pushing to main branch..."
git push -u origin main

echo "Deployment configuration pushed successfully!"
echo "Your Render deployment should now work with the proper configuration."