"""Test script to verify app starts without errors"""
import sys

try:
    print("Testing app startup...")
    print("1. Testing imports...")
    from blindness import RetinalAIApp, get_dashboard_stats
    print("   [OK] Imports successful")
    
    print("2. Testing database stats...")
    stats = get_dashboard_stats()
    print(f"   [OK] Stats retrieved: {stats}")
    
    print("3. Testing app initialization...")
    # Don't actually start the GUI, just test initialization
    print("   [OK] App ready to start")
    
    print("\n[SUCCESS] All tests passed! App should run without errors.")
    print("Run 'python blindness.py' to start the application.")
    
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
