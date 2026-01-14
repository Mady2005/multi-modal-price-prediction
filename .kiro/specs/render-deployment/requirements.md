# Requirements Document

## Introduction

This document outlines the requirements for deploying the Smart Pricing AI system to Render, a cloud platform that supports web services, databases, and static sites. The system consists of a FastAPI backend API, a Streamlit frontend interface, an analytics dashboard, and requires a PostgreSQL database.

## Glossary

- **Render**: Cloud platform for deploying web services, databases, and static sites
- **FastAPI_Service**: The backend API service that serves ML model predictions
- **Streamlit_Frontend**: The user-facing web application for price predictions
- **Streamlit_Dashboard**: The analytics dashboard for viewing pricing insights
- **PostgreSQL_Database**: Managed database service on Render for storing product data
- **Web_Service**: A Render service type that runs web applications
- **Environment_Variables**: Configuration values stored securely in Render
- **Build_Command**: Command executed during deployment to prepare the application
- **Start_Command**: Command executed to run the application

## Requirements

### Requirement 1: Deploy FastAPI Backend Service

**User Story:** As a system administrator, I want to deploy the FastAPI backend to Render, so that the ML model API is accessible over the internet.

#### Acceptance Criteria

1. WHEN the FastAPI service is deployed THEN the system SHALL expose the /predict endpoint publicly
2. WHEN the service receives a POST request to /predict THEN the system SHALL load the model artifacts and return predictions
3. WHEN the service starts THEN the system SHALL install all Python dependencies from requirements.txt
4. THE FastAPI_Service SHALL run on port 8000 using uvicorn
5. WHEN model artifacts are missing THEN the system SHALL fail gracefully with a clear error message

### Requirement 2: Deploy Streamlit Frontend Service

**User Story:** As an end user, I want to access the pricing prediction interface through a web browser, so that I can get price predictions for products.

#### Acceptance Criteria

1. WHEN the Streamlit frontend is deployed THEN the system SHALL serve the web interface on the assigned Render URL
2. WHEN a user submits a product description THEN the system SHALL send a request to the FastAPI backend
3. THE Streamlit_Frontend SHALL connect to the FastAPI_Service using the correct environment variable for the API URL
4. WHEN the API returns a prediction THEN the system SHALL display the result in a user-friendly format
5. THE Streamlit_Frontend SHALL run using the streamlit run command

### Requirement 3: Deploy Analytics Dashboard Service

**User Story:** As a business analyst, I want to access the analytics dashboard, so that I can view pricing insights and trends.

#### Acceptance Criteria

1. WHEN the dashboard is deployed THEN the system SHALL serve the analytics interface on the assigned Render URL
2. WHEN the dashboard loads THEN the system SHALL connect to the PostgreSQL database
3. THE Streamlit_Dashboard SHALL use environment variables for database connection credentials
4. WHEN database connection fails THEN the system SHALL display a user-friendly error message
5. THE Streamlit_Dashboard SHALL cache data for 60 seconds to optimize performance

### Requirement 4: Provision PostgreSQL Database

**User Story:** As a system administrator, I want to provision a managed PostgreSQL database on Render, so that the application can store and retrieve product data.

#### Acceptance Criteria

1. WHEN the database is provisioned THEN the system SHALL create a PostgreSQL instance accessible to Render services
2. THE PostgreSQL_Database SHALL provide connection credentials including host, port, username, password, and database name
3. WHEN services connect to the database THEN the system SHALL use the internal connection string for security
4. THE PostgreSQL_Database SHALL persist data across service restarts
5. WHEN the database is created THEN the system SHALL be accessible from the dashboard service

### Requirement 5: Configure Environment Variables

**User Story:** As a developer, I want to configure environment variables for each service, so that services can communicate securely without hardcoded credentials.

#### Acceptance Criteria

1. WHEN the FastAPI service is configured THEN the system SHALL not require additional environment variables for basic operation
2. WHEN the frontend is configured THEN the system SHALL have an API_URL environment variable pointing to the FastAPI service
3. WHEN the dashboard is configured THEN the system SHALL have DATABASE_URL environment variable with PostgreSQL connection string
4. THE Environment_Variables SHALL be stored securely in Render's environment configuration
5. WHEN environment variables change THEN the system SHALL redeploy the affected services automatically

### Requirement 6: Handle Model Artifacts

**User Story:** As a developer, I want to ensure model artifacts (model.pkl, vectorizer.pkl) are available during deployment, so that the API can make predictions.

#### Acceptance Criteria

1. WHEN the FastAPI service deploys THEN the system SHALL include model.pkl and vectorizer.pkl in the deployment
2. THE FastAPI_Service SHALL load model artifacts from the application directory
3. WHEN model files are missing THEN the system SHALL log an error and fail to start
4. THE FastAPI_Service SHALL load artifacts once at startup for performance
5. WHEN artifacts are updated THEN the system SHALL require a service restart to load new versions

### Requirement 7: Configure Service Dependencies

**User Story:** As a system administrator, I want to ensure Python dependencies are installed correctly, so that all services run without import errors.

#### Acceptance Criteria

1. WHEN any service deploys THEN the system SHALL install dependencies from requirements.txt
2. THE Build_Command SHALL execute pip install -r requirements.txt
3. WHEN LightGBM is installed THEN the system SHALL include necessary system libraries (libgomp1)
4. WHEN dependency installation fails THEN the system SHALL halt deployment and display error logs
5. THE System SHALL use Python 3.9 or higher for compatibility

### Requirement 8: Configure Service Start Commands

**User Story:** As a developer, I want to specify the correct start commands for each service, so that they run properly on Render.

#### Acceptance Criteria

1. WHEN the FastAPI service starts THEN the system SHALL execute: uvicorn app:app --host 0.0.0.0 --port 8000
2. WHEN the frontend starts THEN the system SHALL execute: streamlit run frontend.py --server.port 8501
3. WHEN the dashboard starts THEN the system SHALL execute: streamlit run dashboard.py --server.port 8501
4. THE Start_Command SHALL bind to 0.0.0.0 to accept external connections
5. WHEN a service crashes THEN the system SHALL automatically restart it

### Requirement 9: Optimize Deployment Configuration

**User Story:** As a system administrator, I want to optimize deployment settings, so that services deploy quickly and run efficiently.

#### Acceptance Criteria

1. WHEN services deploy THEN the system SHALL use the free tier instance type for cost optimization
2. THE System SHALL enable auto-deploy from the main branch for continuous deployment
3. WHEN build caches are available THEN the system SHALL use them to speed up deployments
4. THE System SHALL set health check endpoints for service monitoring
5. WHEN a service is unhealthy THEN the system SHALL restart it automatically

### Requirement 10: Update Application Code for Cloud Deployment

**User Story:** As a developer, I want to update hardcoded localhost URLs, so that services can communicate in the cloud environment.

#### Acceptance Criteria

1. WHEN the frontend connects to the API THEN the system SHALL use the API_URL environment variable instead of localhost
2. WHEN the dashboard connects to the database THEN the system SHALL use the DATABASE_URL environment variable
3. THE Application SHALL fall back to localhost URLs for local development when environment variables are not set
4. WHEN environment variables are missing THEN the system SHALL log a warning
5. THE Application SHALL support both local and cloud configurations without code changes
