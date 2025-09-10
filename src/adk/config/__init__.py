"""
Configuration management for ADK
"""
import os
from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration settings for Agent Development Kit"""
    
    # Google Cloud Configuration
    google_cloud_project: str = Field(default="", env="GOOGLE_CLOUD_PROJECT")
    google_application_credentials: Optional[str] = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    vertex_ai_location: str = Field(default="us-central1", env="VERTEX_AI_LOCATION")
    
    # Dialogflow Configuration
    dialogflow_project_id: Optional[str] = Field(default=None, env="DIALOGFLOW_PROJECT_ID")
    dialogflow_language_code: str = Field(default="en-US", env="DIALOGFLOW_LANGUAGE_CODE")
    
    # OpenAI Configuration (optional)
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # Agent Configuration
    agent_name: str = Field(default="playground-agent", env="AGENT_NAME")
    agent_description: str = Field(default="A playground agent for experimentation", env="AGENT_DESCRIPTION")
    
    # Server Configuration
    host: str = Field(default="localhost", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Storage Configuration
    storage_bucket: Optional[str] = Field(default=None, env="STORAGE_BUCKET")
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    def __init__(self, **kwargs):
        # Load from environment variables if not provided
        from dotenv import load_dotenv
        load_dotenv()
        
        # Override with environment variables
        env_values = {}
        for field_name, field_info in self.model_fields.items():
            env_var = getattr(field_info, 'env', None) or field_name.upper()
            if isinstance(env_var, str) and env_var in os.environ:
                env_values[field_name] = os.environ[env_var]
        
        # Merge kwargs with env values
        final_values = {**env_values, **kwargs}
        super().__init__(**final_values)


def get_config() -> Config:
    """Get configuration instance"""
    return Config()


def validate_google_cloud_setup() -> bool:
    """Validate that Google Cloud is properly configured"""
    config = get_config()
    
    if not config.google_cloud_project:
        print("❌ GOOGLE_CLOUD_PROJECT is not set")
        return False
    
    if config.google_application_credentials:
        if not os.path.exists(config.google_application_credentials):
            print(f"❌ Credentials file not found: {config.google_application_credentials}")
            return False
    else:
        print("⚠️  GOOGLE_APPLICATION_CREDENTIALS not set, using default authentication")
    
    print("✅ Google Cloud configuration appears valid")
    return True