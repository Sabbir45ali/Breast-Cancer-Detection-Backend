# Breast Cancer Detection - Full API Documentation & Frontend Integration Guide

Here is the complete list of all your live APIs, followed by a prompt you can give to your frontend AI agent to wire them up.

---

## 🟢 1. The Core Backend API (Render)
**Base URL:** `https://breast-cancer-detection-backend.onrender.com`

This is your main database and user manager. Your frontend should **ONLY** talk to this server.

### Authentication Endpoints
* **User Signup:** `POST /api/user/signup/`
* **Org Signup:** `POST /api/org/signup/`
* **User Login:** `POST /api/user/login/`
* **Org Login:** `POST /api/org/login/`

### Profile Management
* **Get User Profile:** `GET /api/user/profile/` *(Requires Auth Token)*
* **Update User Profile:** `PUT /api/user/profile/update/` *(Requires Auth Token)*
* **Get Org Profile:** `GET /api/org/profile/` *(Requires Auth Token)*

### Prediction Endpoints (These Auto-Forward to Hugging Face)
* **Predict from Data:** `POST /api/prediction/org_predict_data/` *(Requires Auth Token)*
* **Predict from Image:** `POST /api/prediction/org_predict_image/` *(Requires Auth Token)*

---

## 🧠 2. The Machine Learning Engine (Hugging Face)
**Base URL:** `https://sabbir45ali-bcd-ml-api.hf.space`

This is your raw calculation engine. **Your frontend does not need to call these directly**, but here they are for reference (your Render server securely calls these for you):

* **Raw Data Predict:** `POST /predict/data` (Accepts JSON with `features` array)
* **Raw Image Predict:** `POST /predict/image` (Accepts `multipart/form-data` with `file`)

---

## 🚀 Prompt for your Frontend AI Agent

**Copy and paste everything below the line to your frontend AI assistant:**

---
I have successfully deployed my Breast Cancer Detection backend using a microservices architecture. My main Django Core API is live at `https://breast-cancer-detection-backend.onrender.com`.

I need you to update my React frontend to point to this new live server instead of localhost.

Here are the requirements:
1. Update the base URL in our API service files (or Axios/Fetch instances) to point to `https://breast-cancer-detection-backend.onrender.com`.
2. Ensure that auth tokens (like Firebase JWTs) are being passed correctly in the Authorization headers for protected routes (like `/api/user/profile/` and `/api/prediction/org_predict_data/`).
3. I am currently getting a `net::ERR_CONNECTION_RESET` and a `TypeError: Cannot read properties of null (reading 'name')` on my Profile page. This was because the backend connection dropped and the frontend didn't gracefully handle the `null` profile data. 
4. Please add optional chaining (e.g., `profile?.name`) or a loading/error state boundary around the `MainModalProfile` component so the app doesn't crash if the profile fetch fails or takes a moment to load.
5. All prediction requests from the frontend should go to the Render endpoints (`/api/prediction/org_predict_data/` and `/api/prediction/org_predict_image/`). The backend will handle the proxying to our Hugging Face ML service.

Please provide the updated React code for the API configuration and the Profile component error handling.
