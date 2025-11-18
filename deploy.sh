#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
REGION=${REGION:-us-central1}
REPO=verification-tool
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo "🚀 Deploying Content Verification Tool to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Project Number: $PROJECT_NUMBER"
echo "Region: $REGION"
echo "Service Account: $SERVICE_ACCOUNT"
echo ""

# Create Artifact Registry repository (only needed first time)
echo "📦 Setting up Artifact Registry..."
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION \
  --quiet 2>/dev/null || echo "Repository already exists"

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Grant secret access to Cloud Run service account
echo ""
echo "🔐 Granting secret access to service account..."
gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor" \
  --quiet 2>/dev/null || echo "Permission already granted"

# Build and push backend
echo ""
echo "🔨 Building backend image..."
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/backend:latest ./backend
echo "⬆️  Pushing backend image..."
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/backend:latest

# Build and push frontend
echo ""
echo "🔨 Building frontend image..."
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/frontend:latest ./frontend
echo "⬆️  Pushing frontend image..."
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/frontend:latest

# Deploy backend first
echo ""
echo "🚀 Deploying backend service..."
gcloud run deploy verification-backend \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/backend:latest \
  --region=$REGION \
  --platform=managed \
  --memory=2Gi \
  --cpu=2 \
  --timeout=300 \
  --max-instances=10 \
  --set-secrets=GEMINI_API_KEY=GEMINI_API_KEY:latest \
  --allow-unauthenticated \
  --quiet

# Get backend URL
BACKEND_URL=$(gcloud run services describe verification-backend \
  --region=$REGION --format='value(status.url)')

echo "✅ Backend deployed: $BACKEND_URL"

# Update backend CORS with wildcard for Cloud Run frontend
echo ""
echo "🔧 Updating backend CORS..."
gcloud run services update verification-backend \
  --region=$REGION \
  --set-env-vars=ALLOWED_ORIGINS=$BACKEND_URL,https://verification-frontend-*.run.app \
  --quiet

# Deploy frontend with backend URL
echo ""
echo "🚀 Deploying frontend service..."
gcloud run deploy verification-frontend \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/frontend:latest \
  --region=$REGION \
  --platform=managed \
  --memory=512Mi \
  --cpu=1 \
  --set-env-vars=BACKEND_URL=$BACKEND_URL \
  --allow-unauthenticated \
  --quiet

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe verification-frontend \
  --region=$REGION --format='value(status.url)')

echo ""
echo "✅ ========================================="
echo "✅ Deployment Complete!"
echo "✅ ========================================="
echo ""
echo "🌐 Frontend URL: $FRONTEND_URL"
echo "🔧 Backend URL:  $BACKEND_URL"
echo ""
echo "📝 Next steps:"
echo "   1. Visit the frontend URL to test"
echo "   2. Monitor logs: gcloud run services logs tail verification-frontend --region=$REGION"
echo "   3. Monitor backend: gcloud run services logs tail verification-backend --region=$REGION"
echo ""