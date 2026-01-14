# Implementation Plan: Render Deployment

## Overview

This plan guides the deployment of the Smart Pricing AI system to Render. Tasks are organized sequentially, starting with code preparation, then service deployment, and finally verification. Each task builds on previous steps to ensure a smooth deployment process.

## Tasks

- [x] 1. Prepare application code for cloud deployment
  - Update frontend.py to use API_URL environment variable instead of hardcoded localhost
  - Update dashboard.py to use DATABASE_URL environment variable instead of hardcoded localhost
  - Add fallback to localhost for local development when environment variables are not set
  - _Requirements: 10.1, 10.2, 10.3_

- [x] 1.1 Write unit tests for environment variable configuration

  - Test that API_URL is read correctly from environment
  - Test fallback to localhost when environment variable is not set
  - Test DATABASE_URL parsing and validation
  - _Requirements: 10.3, 10.4_

- [x] 2. Update requirements.txt for cloud deployment
  - Verify all dependencies are listed (fastapi, uvicorn, streamlit, requests, plotly, sqlalchemy, pandas, numpy, scikit-learn, lightgbm, joblib, pydantic)
  - Ensure psycopg2-binary is included for PostgreSQL connectivity
  - Pin versions for reproducible builds (optional but recommended)
  - _Requirements: 7.1, 7.2_

- [x] 3. Create Render account and connect repository
  - Sign up for Render account at https://render.com
  - Connect your Git repository (GitHub, GitLab, or Bitbucket)
  - Grant Render access to the repository containing the Smart Pricing AI code
  - _Requirements: 9.2_

- [x] 4. Deploy PostgreSQL database service
  - [ ] 4.1 Create PostgreSQL database in Render dashboard
    - Click "New +" and select "PostgreSQL"
    - Set database name to "pricing_data"
    - Select free tier plan
    - Click "Create Database"
    - _Requirements: 4.1, 4.2_

  - [ ] 4.2 Save database connection credentials
    - Copy the "Internal Database URL" from Render dashboard
    - Save it for use in dashboard service environment variables
    - Verify database shows as "Available" status
    - _Requirements: 4.2, 4.3_

- [ ] 5. Deploy FastAPI backend service
  - [ ] 5.1 Create web service for FastAPI backend
    - Click "New +" and select "Web Service"
    - Connect to your repository
    - Set name to "smart-pricing-api" (or your preferred name)
    - Set runtime to "Python 3"
    - Set build command to: `pip install -r requirements.txt`
    - Set start command to: `uvicorn app:app --host 0.0.0.0 --port 8000`
    - Select free tier instance type
    - Click "Create Web Service"
    - _Requirements: 1.1, 1.3, 1.4, 8.1_

  - [ ] 5.2 Verify backend deployment and model loading
    - Wait for deployment to complete (check logs)
    - Verify "Loading model artifacts..." appears in logs
    - Verify service shows as "Live" in Render dashboard
    - Access the service URL and append `/docs` to view FastAPI documentation
    - _Requirements: 1.2, 6.1, 6.4_

  - [ ]* 5.3 Test backend API endpoint
    - Send POST request to `/predict` endpoint with sample data
    - Verify response contains predicted_price, currency, and status fields
    - Test with various product descriptions
    - **Property 5: Model Artifact Loading**
    - **Validates: Requirements 1.2, 6.1, 6.2**

- [ ] 6. Checkpoint - Verify backend is working
  - Ensure backend service is "Live" and responding to requests
  - Verify model artifacts loaded successfully from logs
  - Test `/predict` endpoint returns valid predictions
  - Ask the user if questions arise

- [ ] 7. Deploy Streamlit frontend service
  - [ ] 7.1 Create web service for Streamlit frontend
    - Click "New +" and select "Web Service"
    - Connect to your repository
    - Set name to "smart-pricing-frontend" (or your preferred name)
    - Set runtime to "Python 3"
    - Set build command to: `pip install -r requirements.txt`
    - Set start command to: `streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0`
    - Select free tier instance type
    - _Requirements: 2.1, 2.5, 8.2_

  - [ ] 7.2 Configure frontend environment variables
    - In service settings, go to "Environment" section
    - Add environment variable: `API_URL`
    - Set value to your backend service URL + `/predict` (e.g., `https://smart-pricing-api.onrender.com/predict`)
    - Save changes (service will auto-redeploy)
    - _Requirements: 5.2, 5.3, 10.1_

  - [ ] 7.3 Verify frontend deployment
    - Wait for deployment to complete
    - Access the frontend URL in browser
    - Verify the web interface loads correctly
    - Check that form is displayed and accepts input
    - _Requirements: 2.1, 2.4_

  - [ ]* 7.4 Test end-to-end prediction flow
    - Submit a product description through the frontend
    - Verify request is sent to backend API
    - Verify prediction result is displayed
    - Test error handling with invalid input
    - **Property 3: API Communication**
    - **Validates: Requirements 2.2, 10.1**

- [ ] 8. Deploy Streamlit dashboard service
  - [ ] 8.1 Create web service for Streamlit dashboard
    - Click "New +" and select "Web Service"
    - Connect to your repository
    - Set name to "smart-pricing-dashboard" (or your preferred name)
    - Set runtime to "Python 3"
    - Set build command to: `pip install -r requirements.txt`
    - Set start command to: `streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0`
    - Select free tier instance type
    - _Requirements: 3.1, 3.5, 8.3_

  - [ ] 8.2 Configure dashboard environment variables
    - In service settings, go to "Environment" section
    - Add environment variable: `DATABASE_URL`
    - Set value to the Internal Database URL from step 4.2
    - Save changes (service will auto-redeploy)
    - _Requirements: 3.3, 5.3, 10.2_

  - [ ] 8.3 Verify dashboard deployment
    - Wait for deployment to complete
    - Access the dashboard URL in browser
    - Verify the dashboard interface loads
    - Check for database connection errors in the UI
    - _Requirements: 3.1, 3.2_

  - [ ]* 8.4 Test dashboard database connectivity
    - Verify dashboard connects to PostgreSQL database
    - Check that error message is displayed if connection fails
    - If connection succeeds, verify data loading (may be empty initially)
    - **Property 4: Database Connectivity**
    - **Validates: Requirements 3.2, 4.3, 10.2**

- [ ] 9. Checkpoint - Verify all services are deployed
  - Ensure all three services show as "Live" in Render dashboard
  - Verify database shows as "Available"
  - Test each service individually
  - Ask the user if questions arise

- [ ] 10. Populate database with sample data (optional)
  - [ ] 10.1 Run ETL pipeline to populate database
    - Update etl_pipeline.py to use DATABASE_URL environment variable
    - Run ETL pipeline locally or create a separate Render job
    - Verify data is inserted into products_cleaned table
    - _Requirements: 4.4_

  - [ ]* 10.2 Verify dashboard displays data
    - Refresh dashboard in browser
    - Verify KPIs are displayed (Total Products, Average Price, etc.)
    - Verify charts are rendered correctly
    - Check that raw data table shows records
    - _Requirements: 3.2, 3.4_

- [ ] 11. Configure service health checks and monitoring
  - [ ] 11.1 Set up health check endpoints
    - For FastAPI backend, use `/docs` or create a `/health` endpoint
    - For Streamlit services, use the default root path `/`
    - Configure health check path in Render service settings
    - _Requirements: 9.4_

  - [ ] 11.2 Enable auto-deploy from Git
    - In each service settings, enable "Auto-Deploy"
    - Set branch to "main" or your default branch
    - Verify that pushing to Git triggers automatic redeployment
    - _Requirements: 9.2_

- [ ]* 12. Perform comprehensive integration testing
  - Test frontend → backend communication with various inputs
  - Test dashboard → database queries and data display
  - Verify error handling for all services
  - Test service restart resilience by manually restarting services
  - **Property 1: Service Accessibility**
  - **Property 7: Service Restart Resilience**
  - **Validates: Requirements 1.1, 2.1, 3.1, 8.5, 9.5**

- [ ] 13. Document deployment configuration
  - Create a DEPLOYMENT.md file with service URLs
  - Document environment variables for each service
  - Include troubleshooting tips for common issues
  - Add instructions for updating services and rolling back changes
  - _Requirements: 9.4_

- [ ] 14. Final checkpoint - Deployment complete
  - All services are live and healthy
  - End-to-end flows are working correctly
  - Documentation is complete
  - Ask the user if they have any questions or need additional configuration

## Notes

- Tasks marked with `*` are optional and can be skipped for faster deployment
- Free tier services on Render sleep after 15 minutes of inactivity (first request may be slow)
- Each service can be updated independently by pushing changes to Git
- Environment variables can be updated in Render dashboard without code changes
- Database connection string should use the "Internal Database URL" for security
- Model artifacts (model.pkl, vectorizer.pkl) must be in the repository for backend to work
- If deployment fails, check the logs in Render dashboard for error messages

## Deployment URLs

After deployment, you will have three public URLs:
- **Backend API**: `https://smart-pricing-api.onrender.com`
- **Frontend**: `https://smart-pricing-frontend.onrender.com`
- **Dashboard**: `https://smart-pricing-dashboard.onrender.com`

(Replace with your actual service names)

## Troubleshooting

Common issues and solutions:
- **Service won't start**: Check logs for missing dependencies or syntax errors
- **Frontend can't reach backend**: Verify API_URL environment variable is set correctly
- **Dashboard can't connect to database**: Verify DATABASE_URL is set and database is available
- **Model artifacts not found**: Ensure model.pkl and vectorizer.pkl are committed to repository
- **Slow first request**: Free tier services sleep after inactivity; first request wakes them up
