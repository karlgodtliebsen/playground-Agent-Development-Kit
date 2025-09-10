"""
Utility functions for ADK
"""
import structlog
import sys
import logging
from typing import Any, Dict


def setup_logging(level: str = "INFO", format_type: str = "json") -> None:
    """Setup structured logging"""
    
    # Map level strings to logging constants
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    log_level = level_map.get(level.upper(), logging.INFO)
    
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
    ]
    
    if format_type == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.WriteLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def validate_environment() -> Dict[str, Any]:
    """Validate the environment setup"""
    from ..config import validate_google_cloud_setup
    
    results = {
        "google_cloud": validate_google_cloud_setup(),
        "python_version": sys.version,
    }
    
    # Check optional dependencies
    optional_deps = {}
    
    try:
        import google.cloud.aiplatform
        optional_deps["vertex_ai"] = True
    except ImportError:
        optional_deps["vertex_ai"] = False
    
    try:
        import google.cloud.dialogflow
        optional_deps["dialogflow"] = True
    except ImportError:
        optional_deps["dialogflow"] = False
    
    try:
        import openai
        optional_deps["openai"] = True
    except ImportError:
        optional_deps["openai"] = False
    
    try:
        import langchain
        optional_deps["langchain"] = True
    except ImportError:
        optional_deps["langchain"] = False
    
    results["dependencies"] = optional_deps
    
    return results


def print_environment_status() -> None:
    """Print environment validation results"""
    results = validate_environment()
    
    print("🔍 Environment Validation Results:")
    print(f"  Google Cloud: {'✅' if results['google_cloud'] else '❌'}")
    print(f"  Python: {results['python_version']}")
    
    print("\n📦 Dependencies:")
    for dep, available in results["dependencies"].items():
        status = "✅" if available else "❌"
        print(f"  {dep}: {status}")
    
    if not all(results["dependencies"].values()):
        print("\n💡 To install missing dependencies:")
        print("  pip install -e .[ai,dev]")


def create_sample_env_file() -> None:
    """Create a sample .env file with placeholder values"""
    import os
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        return
    
    import shutil
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from .env.example")
        print("📝 Please edit .env file with your actual configuration values")
    else:
        print("❌ .env.example file not found")