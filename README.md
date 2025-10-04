# Google Drive Image Import Service

**Working Site URL:**  
[http://43.204.107.183](http://43.204.107.183)

---

##  Overview
This project enables you to paste a **Google Drive folder URL**, automatically fetch all images from it, and store them in the backend for later retrieval.  

The system follows a **microservice-based architecture** with **separate frontend and backend services** for scalability and modularity.

---

##  Setup Instructions

### 🔹 Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/resilkv/google-drive-backend.git
   cd google-drive-backend


Environment Variables

Navigate into each service and create a .env file.

**Sample .env-example files are provided in respective folders**
    ```bash
    cd api_service
    create .env (refer .env-example)
    ```bash
    cd ../meta_service
    create .env (refer .env-example)
    ```bash
    cd ../frontend/google_image-frontend
    create .env (manual configuration)
---

Google Drive API Setup

Enable Google Drive API in Google Cloud Console.

Download the service account JSON file.

Save it as service-account.json in both api_service and meta_service.

## Run with Docker Compose


docker-compose build
docker-compose up -d

Frontend → http://localhost:3000

api_service → http://localhost:8001

meta_service → http://localhost:8000

# API Documentation
1. Upload Google Drive Folder URL
Endpoint:
POST /api/image-processing/

Request Body:


{
  "folder_url": "https://drive.google.com/drive/folders/<folder-id>"
}

Response:

{
  "status": "success",
  "imported_files": ["image1.jpg", "image2.png"]
}

# Architecture

Frontend (React)
Provides the UI to paste Google Drive folder URL and display images.

API Service (Django + DRF)
Handles incoming requests, communicates with Google Drive API, and stores image metadata.

Meta Service (Django + DRF)
Manages metadata and relationships of stored images.

Database (MySQL)
Stores image details and metadata.

Storage (Amazon S3)
Image files are stored securely in AWS S3.

# Scalability Notes
Microservice Architecture → Each service (Frontend, API, Meta) can scale independently.

Asynchronous Processing → Celery + Redis can handle large folder imports in the background.

Cloud Storage → Large image sets stored in S3 or Google Cloud Storage.

Future Improvements → Add load balancing (Nginx/HAProxy) and pagination for handling thousands of images.

# API Documentation URLs

api_service → http://43.204.107.183:8001/api/docs/

meta_service → http://43.204.107.183:8000/api/docs/

# Notes
Ensure .env files are configured correctly before starting services.

Google Drive folder must be shared with view access for the service account to fetch files.

