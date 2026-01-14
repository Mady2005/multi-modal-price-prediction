# Design Document: Render Deployment for Smart Pricing AI

## Overview

This design outlines the deployment architecture for the Smart Pricing AI system on Render. The system will be deployed as three separate web services (FastAPI backend, Streamlit frontend, Streamlit dashboard) and one PostgreSQL database, all communicating through environment variables and internal networking.

The deployment follows a microservices architecture where each component is independently deployable and scalable. Services communicate via HTTP APIs and database connections using environment-based configuration.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Render Cloud                         │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │   Streamlit      │─────▶│   FastAPI        │            │
│  │   Frontend       │      │   Backend        │            │
│  │  (frontend.py)   │      │   (app.py)       │            │
│  │  Port: 8501      │      │   Port: 8000     │            │
│  └──────────────────┘      └──────────────────┘            │
│                                     │                        │
│  ┌──────────────────┐              │                        │
│  │   Streamlit      │              │                        │
│  │   Dashboard      │              │                        │
│  │ (dashboard.py)   │              │                        │
│  │  Port: 8501      │              │                        │
│  └────────┬─────────┘              │                        │
│           │                         │                        │
│           │         ┌───────────────▼──────────┐            │
│           └────────▶│   PostgreSQL Database    │            │
│                     │   (Managed Service)      │            │
│                     └──────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Service Communication

1. **Frontend → Backend**: HTTP POST requests to `/predict` endpoint
2. **Dashboard → Database**: PostgreSQL connection via SQLAlchemy
3. **Environment Variables**: Used for service discovery and configuration

### Deployment Strategy

Each service will be deployed independently with:
- Automatic deployments from Git repository
- Environment-specific configuration via environment variables
- Health checks and automatic restarts
- Build and start commands tailored to each service type

## Components and Interfaces

### Component 1: FastAPI Backend Service

**Purpose**: Serve ML model predictions via REST API

**Configuration**:
- **Service Type**: Web Service
- **Runtime**: Python 3.9+
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 8000`
- **Port**: 8000
- **Health Check**: GET `/` or `/docs`

**Files Required**:
- `app.py` - Main FastAPI application
- `feature_engineering.py` - Feature processing utilities
- `model.pkl` - Trained ML model
- `vectorizer.pkl` - TF-IDF vectorizer
- `requirements.txt` - Python dependencies

**Environment Variables**:
- None required (model artifacts loaded from local filesystem)

**API Endpoints**:
- `POST /predict` - Accepts `{"catalog_content": "string"}`, returns `{"predicted_price": float, "currency": "USD", "status": "success"}`

### Component 2: Streamlit Frontend Service

**Purpose**: Provide user interface for price predictions

**Configuration**:
- **Service Type**: Web Service
- **Runtime**: Python 3.9+
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0`
- **Port**: 8501

**Files Required**:
- `frontend.py` - Streamlit application
- `requirements.txt` - Python dependencies (must include `streamlit` and `requests`)

**Environment Variables**:
- `API_URL` - URL of the FastAPI backend service (e.g., `https://smart-pricing-api.onrender.com/predict`)

**Code Modifications Required**:
```python
# Current code (frontend.py line 7):
API_URL = "http://127.0.0.1:8000/predict"

# Updated code:
import os
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
```

### Component 3: Streamlit Dashboard Service

**Purpose**: Provide analytics and insights dashboard

**Configuration**:
- **Service Type**: Web Service
- **Runtime**: Python 3.9+
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0`
- **Port**: 8501

**Files Required**:
- `dashboard.py` - Streamlit dashboard application
- `requirements.txt` - Python dependencies (must include `streamlit`, `plotly`, `sqlalchemy`)

**Environment Variables**:
- `DATABASE_URL` - PostgreSQL connection string (provided by Render database service)

**Code Modifications Required**:
```python
# Current code (dashboard.py line 6):
DB_CONNECTION_URL = "postgresql://user:password@localhost:5432/pricing_data"

# Updated code:
import os
DB_CONNECTION_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/pricing_data")
```

### Component 4: PostgreSQL Database

**Purpose**: Store product data for analytics

**Configuration**:
- **Service Type**: PostgreSQL (Managed Database)
- **Version**: PostgreSQL 15
- **Database Name**: `pricing_data`
- **Plan**: Free tier (sufficient for development/testing)

**Connection Details**:
- Render provides internal and external connection strings
- Use internal connection string for services within Render
- Connection string format: `postgresql://user:password@host:port/database`

**Schema Setup**:
- Table: `products_cleaned`
- Columns: Based on ETL pipeline output (price, brand, etc.)
- Note: Schema creation should be handled by ETL pipeline or migration scripts

## Data Models

### API Request Model (FastAPI)

```python
class ProductInput(BaseModel):
    catalog_content: str  # Product description text
```

### API Response Model (FastAPI)

```python
{
    "predicted_price": float,  # Predicted price in USD
    "currency": str,           # Currency code (e.g., "USD")
    "status": str              # Status message (e.g., "success")
}
```

### Database Schema (PostgreSQL)

```sql
-- Table: products_cleaned
-- Note: Actual schema depends on ETL pipeline
CREATE TABLE products_cleaned (
    id SERIAL PRIMARY KEY,
    catalog_content TEXT,
    price DECIMAL(10, 2),
    brand VARCHAR(255),
    is_bulk INTEGER,
    item_quantity INTEGER,
    -- Additional columns from feature engineering
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Environment Configuration Model

```python
# Service configuration via environment variables
{
    "API_URL": "https://smart-pricing-api.onrender.com/predict",  # Frontend
    "DATABASE_URL": "postgresql://user:pass@host:5432/db"         # Dashboard
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Service Accessibility
*For any* deployed service on Render, when the service is healthy, it should respond to HTTP requests on its designated port within 30 seconds.
**Validates: Requirements 1.1, 2.1, 3.1**

### Property 2: Environment Variable Resolution
*For any* service that requires environment variables, when the service starts, it should successfully read and use the configured environment variables or fall back to default values for local development.
**Validates: Requirements 5.2, 5.3, 10.3**

### Property 3: API Communication
*For any* valid product description submitted through the frontend, when the frontend sends a request to the backend API, the request should reach the correct API endpoint and return a response.
**Validates: Requirements 2.2, 10.1**

### Property 4: Database Connectivity
*For any* dashboard service instance, when it attempts to connect to the PostgreSQL database using the DATABASE_URL environment variable, the connection should succeed or fail with a clear error message.
**Validates: Requirements 3.2, 4.3, 10.2**

### Property 5: Model Artifact Loading
*For any* FastAPI service deployment, when the service starts, it should successfully load both model.pkl and vectorizer.pkl from the application directory or fail with a descriptive error.
**Validates: Requirements 1.2, 6.1, 6.2, 6.4**

### Property 6: Dependency Installation
*For any* service deployment, when the build command executes, all dependencies listed in requirements.txt should install successfully without errors.
**Validates: Requirements 7.1, 7.2, 7.4**

### Property 7: Service Restart Resilience
*For any* service that crashes or becomes unhealthy, when Render detects the failure, the service should automatically restart and return to a healthy state.
**Validates: Requirements 8.5, 9.5**

### Property 8: Port Binding
*For any* service with a start command, when the service starts, it should bind to 0.0.0.0 (all interfaces) on the specified port to accept external connections.
**Validates: Requirements 1.4, 2.5, 8.4**

## Error Handling

### Service Startup Errors

**Model Artifact Missing**:
- **Detection**: FastAPI service fails to load model.pkl or vectorizer.pkl
- **Response**: Service logs error message and exits with non-zero status code
- **User Impact**: Deployment fails, Render shows error in logs
- **Resolution**: Ensure model files are committed to repository or uploaded separately

**Database Connection Failure**:
- **Detection**: Dashboard cannot connect to PostgreSQL using DATABASE_URL
- **Response**: Display user-friendly error message in Streamlit UI
- **User Impact**: Dashboard loads but shows connection error
- **Resolution**: Verify DATABASE_URL environment variable is set correctly

**Missing Environment Variables**:
- **Detection**: Service attempts to read undefined environment variable
- **Response**: Fall back to default localhost values (for local dev) or log warning
- **User Impact**: Service may work locally but fail in production
- **Resolution**: Set required environment variables in Render dashboard

### Runtime Errors

**API Request Failure**:
- **Detection**: Frontend receives non-200 status code from backend
- **Response**: Display error message with status code and details
- **User Impact**: User sees error message instead of prediction
- **Resolution**: Check backend logs, verify API_URL is correct

**Prediction Error**:
- **Detection**: Backend encounters exception during prediction
- **Response**: Return HTTP 500 with error details in JSON
- **User Impact**: User sees error message
- **Resolution**: Check input format, verify model compatibility

**Database Query Error**:
- **Detection**: Dashboard SQL query fails
- **Response**: Display error message in Streamlit UI
- **User Impact**: Dashboard shows error instead of data
- **Resolution**: Verify database schema matches query expectations

### Deployment Errors

**Build Failure**:
- **Detection**: pip install fails during build
- **Response**: Deployment stops, error shown in Render logs
- **User Impact**: Service not deployed
- **Resolution**: Check requirements.txt for invalid packages, verify Python version

**Port Binding Failure**:
- **Detection**: Service cannot bind to specified port
- **Response**: Service fails to start
- **User Impact**: Service shows as unhealthy
- **Resolution**: Verify start command uses correct port, check for port conflicts

## Testing Strategy

### Manual Testing Approach

Since this is a deployment configuration project, testing will primarily be manual verification of each deployment step. The testing strategy focuses on validating that services are correctly configured and can communicate with each other.

### Unit Tests

**Configuration Validation Tests**:
- Test that environment variables are correctly read with fallback values
- Test that service URLs are properly formatted
- Test that database connection strings are valid format

**Example Test Cases**:
```python
# Test environment variable fallback
def test_api_url_fallback():
    # When API_URL is not set
    os.environ.pop('API_URL', None)
    # Then should use localhost default
    assert get_api_url() == "http://127.0.0.1:8000/predict"

# Test database URL parsing
def test_database_url_format():
    # For any valid PostgreSQL URL
    url = "postgresql://user:pass@host:5432/db"
    # Should parse without errors
    assert parse_database_url(url) is not None
```

### Integration Tests

**Service Communication Tests**:
- Verify frontend can reach backend API
- Verify dashboard can connect to database
- Verify API returns valid predictions

**Deployment Verification Tests**:
- Check that all services are running and healthy
- Verify environment variables are set correctly
- Test end-to-end flow: frontend → backend → response

**Example Test Cases**:
```python
# Test API endpoint accessibility
def test_api_health():
    # For any deployed API service
    response = requests.get(f"{API_URL}/docs")
    # Should return 200 OK
    assert response.status_code == 200

# Test database connectivity
def test_database_connection():
    # For any configured database URL
    engine = create_engine(DATABASE_URL)
    # Should connect without errors
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        assert result.fetchone()[0] == 1
```

### Deployment Validation Checklist

After each service deployment, verify:

1. **FastAPI Backend**:
   - [ ] Service shows as "Live" in Render dashboard
   - [ ] Can access `/docs` endpoint (FastAPI auto-generated docs)
   - [ ] POST request to `/predict` returns valid JSON response
   - [ ] Model artifacts loaded successfully (check logs)

2. **Streamlit Frontend**:
   - [ ] Service shows as "Live" in Render dashboard
   - [ ] Can access web interface in browser
   - [ ] Form accepts input and submits without errors
   - [ ] Receives response from backend API

3. **Streamlit Dashboard**:
   - [ ] Service shows as "Live" in Render dashboard
   - [ ] Can access dashboard in browser
   - [ ] Successfully connects to database
   - [ ] Displays data and charts correctly

4. **PostgreSQL Database**:
   - [ ] Database shows as "Available" in Render dashboard
   - [ ] Can connect using provided connection string
   - [ ] Tables exist and contain data (if ETL has run)

### Testing Configuration Changes

When updating environment variables or service configuration:

1. Make change in Render dashboard
2. Wait for automatic redeployment
3. Verify service restarts successfully
4. Test affected functionality
5. Check logs for any errors

### Performance Testing

Basic performance validation:
- API response time should be < 2 seconds for predictions
- Dashboard should load within 5 seconds
- Frontend should be responsive and load within 3 seconds

Note: Formal load testing is not required for initial deployment but should be considered for production scaling.

## Deployment Steps Summary

### Phase 1: Prepare Repository
1. Update code to use environment variables
2. Verify all required files are in repository
3. Ensure requirements.txt includes all dependencies
4. Commit and push changes to Git

### Phase 2: Create Render Account and Services
1. Sign up for Render account
2. Connect Git repository to Render
3. Create PostgreSQL database service
4. Note database connection string

### Phase 3: Deploy Backend Service
1. Create new Web Service for FastAPI
2. Configure build and start commands
3. Deploy and verify model artifacts load
4. Test `/predict` endpoint

### Phase 4: Deploy Frontend Service
1. Create new Web Service for Streamlit frontend
2. Set API_URL environment variable (backend URL)
3. Configure build and start commands
4. Deploy and test prediction flow

### Phase 5: Deploy Dashboard Service
1. Create new Web Service for Streamlit dashboard
2. Set DATABASE_URL environment variable
3. Configure build and start commands
4. Deploy and verify database connection

### Phase 6: Verification and Testing
1. Test all services individually
2. Test end-to-end flows
3. Verify error handling
4. Check logs for any warnings

## Additional Considerations

### Cost Optimization
- Use Render free tier for all services (sufficient for development)
- Free tier limitations: 750 hours/month, services sleep after 15 minutes of inactivity
- Consider upgrading to paid tier for production use (no sleep, better performance)

### Security
- Use Render's internal networking for service-to-service communication
- Store sensitive credentials in environment variables, not code
- Use HTTPS for all external connections (Render provides this automatically)
- Restrict database access to Render services only

### Monitoring
- Use Render's built-in logging and metrics
- Set up health checks for automatic restart on failure
- Monitor service logs for errors and warnings
- Consider adding application-level logging for debugging

### Scaling Considerations
- Each service can be scaled independently
- Database can be upgraded to larger instance for more storage/performance
- Consider adding caching layer (Redis) for high-traffic scenarios
- Use Render's auto-scaling features for production workloads

### Maintenance
- Keep dependencies updated in requirements.txt
- Regularly review logs for errors
- Test deployments in staging environment before production
- Document any custom configuration or workarounds
