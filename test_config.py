"""
Unit tests for environment variable configuration.
Tests API_URL and DATABASE_URL reading, fallback, and validation.

Requirements: 10.3, 10.4
"""
import os
import pytest
from config import get_api_url, get_database_url, validate_database_url, parse_database_url


class TestAPIURLConfiguration:
    """Test suite for API_URL environment variable handling."""
    
    def test_api_url_reads_from_environment(self):
        """Test that API_URL is read correctly from environment."""
        # Given: API_URL is set in environment
        test_url = "https://smart-pricing-api.onrender.com/predict"
        os.environ['API_URL'] = test_url
        
        try:
            # When: Getting the API URL
            result = get_api_url()
            
            # Then: Should return the environment variable value
            assert result == test_url
        finally:
            # Cleanup
            os.environ.pop('API_URL', None)
    
    def test_api_url_fallback_to_localhost(self):
        """Test fallback to localhost when environment variable is not set."""
        # Given: API_URL is not set in environment
        os.environ.pop('API_URL', None)
        
        # When: Getting the API URL
        result = get_api_url()
        
        # Then: Should return localhost default
        assert result == "http://127.0.0.1:8000/predict"
    
    def test_api_url_with_empty_string(self):
        """Test that empty string in environment uses the empty string (not fallback)."""
        # Given: API_URL is set to empty string
        os.environ['API_URL'] = ""
        
        try:
            # When: Getting the API URL
            result = get_api_url()
            
            # Then: Should return empty string (os.getenv behavior)
            assert result == ""
        finally:
            # Cleanup
            os.environ.pop('API_URL', None)
    
    def test_api_url_with_different_cloud_provider(self):
        """Test API_URL with different cloud provider URLs."""
        # Given: API_URL points to a different cloud provider
        test_url = "https://my-api.herokuapp.com/predict"
        os.environ['API_URL'] = test_url
        
        try:
            # When: Getting the API URL
            result = get_api_url()
            
            # Then: Should return the configured URL
            assert result == test_url
        finally:
            # Cleanup
            os.environ.pop('API_URL', None)


class TestDatabaseURLConfiguration:
    """Test suite for DATABASE_URL environment variable handling."""
    
    def test_database_url_reads_from_environment(self):
        """Test that DATABASE_URL is read correctly from environment."""
        # Given: DATABASE_URL is set in environment
        test_url = "postgresql://dbuser:dbpass@render-host:5432/pricing_db"
        os.environ['DATABASE_URL'] = test_url
        
        try:
            # When: Getting the database URL
            result = get_database_url()
            
            # Then: Should return the environment variable value
            assert result == test_url
        finally:
            # Cleanup
            os.environ.pop('DATABASE_URL', None)
    
    def test_database_url_fallback_to_localhost(self):
        """Test fallback to localhost when environment variable is not set."""
        # Given: DATABASE_URL is not set in environment
        os.environ.pop('DATABASE_URL', None)
        
        # When: Getting the database URL
        result = get_database_url()
        
        # Then: Should return localhost default
        assert result == "postgresql://user:password@localhost:5432/pricing_data"
    
    def test_database_url_with_render_format(self):
        """Test DATABASE_URL with Render's internal connection format."""
        # Given: DATABASE_URL in Render's format
        test_url = "postgresql://pricing_user:securepass123@dpg-abc123.oregon-postgres.render.com/pricing_data_xyz"
        os.environ['DATABASE_URL'] = test_url
        
        try:
            # When: Getting the database URL
            result = get_database_url()
            
            # Then: Should return the Render URL
            assert result == test_url
        finally:
            # Cleanup
            os.environ.pop('DATABASE_URL', None)


class TestDatabaseURLValidation:
    """Test suite for DATABASE_URL validation."""
    
    def test_validate_valid_postgresql_url(self):
        """Test validation accepts valid PostgreSQL URLs."""
        # Given: A valid PostgreSQL URL
        valid_url = "postgresql://user:pass@localhost:5432/dbname"
        
        # When: Validating the URL
        result = validate_database_url(valid_url)
        
        # Then: Should return True
        assert result is True
    
    def test_validate_valid_postgres_url(self):
        """Test validation accepts 'postgres' scheme (alternative to 'postgresql')."""
        # Given: A valid URL with 'postgres' scheme
        valid_url = "postgres://user:pass@localhost:5432/dbname"
        
        # When: Validating the URL
        result = validate_database_url(valid_url)
        
        # Then: Should return True
        assert result is True
    
    def test_validate_url_without_port(self):
        """Test validation accepts URLs without explicit port."""
        # Given: A valid URL without port (will use default)
        valid_url = "postgresql://user:pass@localhost/dbname"
        
        # When: Validating the URL
        result = validate_database_url(valid_url)
        
        # Then: Should return True
        assert result is True
    
    def test_validate_url_without_password(self):
        """Test validation accepts URLs without password."""
        # Given: A valid URL without password
        valid_url = "postgresql://user@localhost:5432/dbname"
        
        # When: Validating the URL
        result = validate_database_url(valid_url)
        
        # Then: Should return True
        assert result is True
    
    def test_validate_invalid_scheme(self):
        """Test validation rejects URLs with invalid scheme."""
        # Given: A URL with invalid scheme
        invalid_url = "mysql://user:pass@localhost:5432/dbname"
        
        # When: Validating the URL
        result = validate_database_url(invalid_url)
        
        # Then: Should return False
        assert result is False
    
    def test_validate_url_without_scheme(self):
        """Test validation rejects URLs without scheme."""
        # Given: A URL without scheme
        invalid_url = "user:pass@localhost:5432/dbname"
        
        # When: Validating the URL
        result = validate_database_url(invalid_url)
        
        # Then: Should return False
        assert result is False
    
    def test_validate_url_without_host(self):
        """Test validation rejects URLs without host."""
        # Given: A URL without host
        invalid_url = "postgresql:///dbname"
        
        # When: Validating the URL
        result = validate_database_url(invalid_url)
        
        # Then: Should return False
        assert result is False
    
    def test_validate_empty_string(self):
        """Test validation rejects empty string."""
        # Given: An empty string
        invalid_url = ""
        
        # When: Validating the URL
        result = validate_database_url(invalid_url)
        
        # Then: Should return False
        assert result is False


class TestDatabaseURLParsing:
    """Test suite for DATABASE_URL parsing."""
    
    def test_parse_complete_database_url(self):
        """Test parsing a complete database URL with all components."""
        # Given: A complete database URL
        url = "postgresql://myuser:mypass@dbhost:5433/mydb"
        
        # When: Parsing the URL
        result = parse_database_url(url)
        
        # Then: Should extract all components correctly
        assert result['scheme'] == 'postgresql'
        assert result['username'] == 'myuser'
        assert result['password'] == 'mypass'
        assert result['host'] == 'dbhost'
        assert result['port'] == 5433
        assert result['database'] == 'mydb'
    
    def test_parse_url_with_default_port(self):
        """Test parsing URL without explicit port uses default 5432."""
        # Given: A URL without explicit port
        url = "postgresql://user:pass@localhost/testdb"
        
        # When: Parsing the URL
        result = parse_database_url(url)
        
        # Then: Should use default port 5432
        assert result['port'] == 5432
    
    def test_parse_url_without_password(self):
        """Test parsing URL without password."""
        # Given: A URL without password
        url = "postgresql://user@localhost:5432/testdb"
        
        # When: Parsing the URL
        result = parse_database_url(url)
        
        # Then: Password should be None
        assert result['username'] == 'user'
        assert result['password'] is None
        assert result['database'] == 'testdb'
    
    def test_parse_render_database_url(self):
        """Test parsing a Render-style database URL."""
        # Given: A Render database URL
        url = "postgresql://pricing_user:abc123xyz@dpg-xyz123.oregon-postgres.render.com/pricing_data_abc"
        
        # When: Parsing the URL
        result = parse_database_url(url)
        
        # Then: Should parse correctly
        assert result['scheme'] == 'postgresql'
        assert result['username'] == 'pricing_user'
        assert result['password'] == 'abc123xyz'
        assert result['host'] == 'dpg-xyz123.oregon-postgres.render.com'
        assert result['database'] == 'pricing_data_abc'
    
    def test_parse_invalid_url_raises_error(self):
        """Test parsing invalid URL raises ValueError."""
        # Given: An invalid database URL
        invalid_url = "not-a-valid-url"
        
        # When/Then: Parsing should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            parse_database_url(invalid_url)
        
        assert "Invalid database URL format" in str(exc_info.value)
    
    def test_parse_url_with_special_characters_in_password(self):
        """Test parsing URL with special characters in password."""
        # Given: A URL with special characters in password (URL-encoded)
        url = "postgresql://user:p@ss%40word@localhost:5432/db"
        
        # When: Parsing the URL
        result = parse_database_url(url)
        
        # Then: Should parse the URL (password remains URL-encoded as returned by urlparse)
        assert result['username'] == 'user'
        # Note: urlparse doesn't automatically decode, so %40 stays as-is
        assert result['password'] == 'p@ss%40word'
        assert result['host'] == 'localhost'
