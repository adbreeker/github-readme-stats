"""
Simple test script to verify the API handlers work correctly
Tests both stats and top languages APIs with mock data
"""

import asyncio
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_handlers import StatsAPIHandler, TopLanguagesAPIHandler

async def test_apis():
    """Test both API handlers"""
    print("Testing GitHub Stats API handlers...")
    
    # Test without GitHub token (should show error)
    print("\n1. Testing without GitHub token (should show error):")
    
    try:
        stats_handler = StatsAPIHandler()
        langs_handler = TopLanguagesAPIHandler()
        print("✓ Handlers initialized successfully")
    except Exception as e:
        print(f"✗ Handler initialization failed: {e}")
        return
    
    # Test with mock query strings
    test_queries = {
        'stats': 'username=testuser&show_icons=true&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=1c1917',
        'langs': 'username=testuser&theme=dark&title_color=0891b2&hide=html,css'
    }
    
    print("\n2. Testing stats API handler:")
    try:
        svg_content, headers = await stats_handler.handle_request(test_queries['stats'])
        print(f"✓ Stats API returned {len(svg_content)} characters")
        print(f"✓ Content-Type: {headers.get('Content-Type')}")
        
        # Save test output
        with open('Tests/test_output_stats.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print("✓ Test output saved to Tests/test_output_stats.svg")
        
    except Exception as e:
        print(f"✗ Stats API failed: {e}")
    
    print("\n3. Testing top languages API handler:")
    try:
        svg_content, headers = await langs_handler.handle_request(test_queries['langs'])
        print(f"✓ Languages API returned {len(svg_content)} characters")
        print(f"✓ Content-Type: {headers.get('Content-Type')}")
        
        # Save test output
        with open('Tests/test_output_langs.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print("✓ Test output saved to Tests/test_output_langs.svg")
        
    except Exception as e:
        print(f"✗ Languages API failed: {e}")
    
    print("\n4. Flask app structure test:")
    try:
        from app import app
        print("✓ Flask app imports successfully")
        print(f"✓ App has {len(app.url_map.iter_rules())} routes:")
        for rule in app.url_map.iter_rules():
            print(f"  - {rule.methods} {rule.rule}")
    
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
    
    print("\n🎉 API testing completed!")
    print("\nTo test with real GitHub data:")
    print("1. Set environment variable: set PAT_1=your_github_token")
    print("2. Run: python app.py")
    print("3. Visit: http://localhost:5000/api?username=yourusername&show_icons=true")

if __name__ == '__main__':
    asyncio.run(test_apis())
