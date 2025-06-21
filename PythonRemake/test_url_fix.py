#!/usr/bin/env python3
"""
Test the specific URL that was not working
"""

import asyncio
from api_handlers import TopLanguagesAPIHandler

async def test_url():
    """Test the exact URL parameters"""
    query_string = "username=adbreeker&show_icons=true&count_private=true&theme=dark&title_color=0891b2&hide=tcl,html,css,powershell,scss,shaderlab"
    
    print(f"Testing query: {query_string}")
    
    handler = TopLanguagesAPIHandler()
    try:
        svg_content, headers = await handler.handle_request(query_string)
        
        # Save the result
        with open('Tests/test_adbreeker_fixed.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print("✅ Success! Generated SVG")
        print(f"SVG length: {len(svg_content)} characters")
        print(f"Content-Type: {headers.get('Content-Type')}")
        print("✅ Saved to Tests/test_adbreeker_fixed.svg")
        
        # Show a preview of the SVG
        print("\nSVG Preview (first 200 chars):")
        print(svg_content[:200] + "...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_url())
