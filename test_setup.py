#!/usr/bin/env python3
"""
Test script to verify PetDunning setup
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")

    try:
        import streamlit
        print("  ✅ streamlit")
    except ImportError as e:
        print(f"  ❌ streamlit: {e}")
        return False

    try:
        import anthropic
        print("  ✅ anthropic")
    except ImportError as e:
        print(f"  ❌ anthropic: {e}")
        return False

    try:
        import langgraph
        print("  ✅ langgraph")
    except ImportError as e:
        print(f"  ❌ langgraph: {e}")
        return False

    try:
        import langchain
        print("  ✅ langchain")
    except ImportError as e:
        print(f"  ❌ langchain: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv")
    except ImportError as e:
        print(f"  ❌ python-dotenv: {e}")
        return False

    try:
        import pandas
        print("  ✅ pandas")
    except ImportError as e:
        print(f"  ❌ pandas: {e}")
        return False

    return True


def test_files():
    """Test required files exist"""
    print("\n📁 Testing file structure...")

    required_files = [
        'app.py',
        'graph.py',
        'state.py',
        'data/mock_db.json',
        'data/medical_risk_tiers.json',
        'agents/router.py',
        'agents/negotiator.py',
        'agents/extractor.py',
        'agents/tools.py',
        'utils/metrics.py',
        'utils/ui_components.py'
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - NOT FOUND")
            all_exist = False

    return all_exist


def test_env():
    """Test environment configuration"""
    print("\n⚙️  Testing environment...")

    if not os.path.exists('.env'):
        print("  ⚠️  .env file not found - you'll need to create one")
        print("     Copy .env.example to .env and add your ANTHROPIC_API_KEY")
        return False

    print("  ✅ .env file exists")

    with open('.env', 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY' in content:
            if 'sk-ant-' in content:
                print("  ✅ ANTHROPIC_API_KEY configured")
                return True
            else:
                print("  ⚠️  ANTHROPIC_API_KEY found but may be invalid")
                print("     Make sure it starts with 'sk-ant-'")
                return False
        else:
            print("  ❌ ANTHROPIC_API_KEY not found in .env")
            return False


def test_module_imports():
    """Test local module imports"""
    print("\n🔧 Testing local modules...")

    try:
        sys.path.insert(0, os.getcwd())

        import state
        print("  ✅ state module")

        import graph
        print("  ✅ graph module")

        from agents import router
        print("  ✅ agents.router")

        from agents import negotiator
        print("  ✅ agents.negotiator")

        from agents import extractor
        print("  ✅ agents.extractor")

        from agents import tools
        print("  ✅ agents.tools")

        from utils import metrics
        print("  ✅ utils.metrics")

        from utils import ui_components
        print("  ✅ utils.ui_components")

        return True
    except Exception as e:
        print(f"  ❌ Error importing modules: {e}")
        return False


def main():
    """Run all tests"""
    print("🐾 PetDunning Enterprise - Setup Test")
    print("=" * 50)
    print()

    results = {
        'imports': test_imports(),
        'files': test_files(),
        'env': test_env(),
        'modules': test_module_imports()
    }

    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()

    if all(results.values()):
        print("🎉 All tests passed! You're ready to run the app.")
        print("\nRun: ./run.sh")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nTry running: ./setup.sh")
        return 1


if __name__ == '__main__':
    sys.exit(main())
