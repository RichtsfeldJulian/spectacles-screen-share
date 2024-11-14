# spectacles-screen-share

conda create -n screenshare python=3.10
pip install -r requirements.txt


# For development (default)
set FLASK_ENV=development  # Windows

# For production
set FLASK_ENV=production  # Windows


# Login to Azure
az login

# Create a resource group
az group create --name screen-capture-rg --location eastus

# Create an App Service plan (Free tier - F1)
az appservice plan create \
  --name screen-capture-plan \
  --resource-group screen-capture-rg \
  --sku F1 \
  --is-linux

# Create a web app
az webapp create \
  --resource-group screen-capture-rg \
  --plan screen-capture-plan \
  --name screen-capture-server \
  --runtime "PYTHON:3.11" \
  --deployment-local-git

# Enable WebSocket support
az webapp config set \
  --resource-group screen-capture-rg \
  --name screen-capture-server \
  --web-sockets-enabled true

# Set startup command
az webapp config set \
  --resource-group screen-capture-rg \
  --name screen-capture-server \
  --startup-file "startup.txt"


  # Initialize git repository if not already done
git init

# Add Azure as remote
git remote add azure <deployment-url-from-azure>

# Add and commit files
git add .
git commit -m "Initial commit"

# Push to Azure
git push azure main

https://None@screen-capture-server.scm.azurewebsites.net/screen-capture-server.git