#!/usr/bin/env python3
"""
Setup script for ADK environment
"""
import os
import sys
import subprocess
from pathlib import Path


def run_command(command: str, description: str = "") -> bool:
    """Run a command and return success status"""
    if description:
        print(f"📋 {description}")
    
    print(f"   Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   ✅ Success")
        return True
    else:
        print(f"   ❌ Failed: {result.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major != 3 or version.minor < 8:
        print(f"   ❌ Python {version.major}.{version.minor} is not supported")
        print("   💡 Please use Python 3.8 or higher")
        return False
    else:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True


def create_virtual_environment():
    """Create a virtual environment"""
    if os.path.exists("venv"):
        print("📦 Virtual environment already exists")
        return True
    
    return run_command(
        "python -m venv venv",
        "Creating virtual environment"
    )


def activate_venv_and_install():
    """Install dependencies in virtual environment"""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -e .", "Installing ADK package"),
        (f"{pip_cmd} install -e .[dev,ai,jupyter]", "Installing optional dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def create_env_file():
    """Create .env file from template"""
    if os.path.exists(".env"):
        print("📄 .env file already exists")
        return True
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your configuration")
        return True
    else:
        print("❌ .env.example not found")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Google Cloud configuration:")
    print("   - Set GOOGLE_CLOUD_PROJECT to your project ID")
    print("   - Set GOOGLE_APPLICATION_CREDENTIALS path (optional)")
    
    print("\n2. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n3. Test the setup:")
    print("   python examples/basic_agent_example.py")
    
    print("\n4. Start the API server:")
    print("   python examples/server.py")
    
    print("\n5. Open Jupyter notebook for experimentation:")
    print("   jupyter notebook")
    
    print("\n📚 Documentation:")
    print("   - Check README.md for detailed instructions")
    print("   - Browse examples/ directory for sample code")
    print("   - Visit Google Cloud Console to set up authentication")


def main():
    """Main setup function"""
    print("🚀 Setting up Agent Development Kit (ADK) environment")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not activate_venv_and_install():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("⚠️  Could not create .env file")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()