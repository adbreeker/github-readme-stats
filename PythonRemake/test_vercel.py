#!/usr/bin/env python3
"""
Test Vercel deployment setup
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from api.index import app
        print("✅ Vercel entry point imports successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_endpoints():
    """Test if endpoints respond correctly"""
    try:
        from api.index import app
        
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Root endpoint works")
            
            # Test health endpoint
            response = client.get('/health')
            assert response.status_code == 200
            print("✅ Health endpoint works")
            
            # Test stats endpoint (should work even without PAT for error handling)
            response = client.get('/api?username=octocat')
            assert response.status_code == 200
            assert 'image/svg+xml' in response.content_type
            print("✅ Stats API endpoint responds with SVG")
            
            # Test languages endpoint
            response = client.get('/api/top-langs?username=octocat')
            assert response.status_code == 200
            assert 'image/svg+xml' in response.content_type
            print("✅ Languages API endpoint responds with SVG")
            
        return True
    except Exception as e:
        print(f"❌ Endpoint test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Vercel deployment setup...\n")
    
    success = True
    success &= test_imports()
    success &= test_endpoints()
    
    if success:
        print("\n🎉 All tests passed! Ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Set up PAT_1 environment variable in Vercel")
        print("2. Deploy with: vercel --prod")
        print("3. Test your deployment at: https://your-app.vercel.app")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
