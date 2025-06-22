"""
Test script for GitHub Contributions SVG Generator
"""

import asyncio
import os
from datetime import datetime
from github_contributions import generate_contributions_svg

async def test_contributions():
    """Test the contributions generator"""
    
    print("🔍 Testing GitHub Contributions SVG Generator...")
    print(f"📅 Current date: {datetime.now().strftime('%A, %B %d, %Y')}")
      # Check if GitHub token is available
    token = os.getenv('PAT_1')
    if not token:
        print("❌ No GitHub token found")
        print("\n📝 Setup instructions:")
        print("1. Create a GitHub Personal Access Token at https://github.com/settings/tokens")
        print("2. No special permissions needed for public profiles")
        print("3. Set environment variable: GITHUB_TOKEN=your_token_here")
        print("4. Or create a .env file with: PAT_1=your_token_here")
        return
    else:
        token_name = "GITHUB_TOKEN" if os.getenv('GITHUB_TOKEN') else "PAT_1"
        print(f"✅ Found GitHub token: {token_name}")
        print(f"🔑 Token starts with: {token[:10]}...")
    
    # Get username from user input or use default
    username = 'adbreeker'
    
    print(f"\n👤 Testing with username: {username}")
    
    # Test both themes
    themes = ["light", "dark"]
    
    for theme in themes:
        print(f"\n🎨 Generating {theme} theme...")
        try:
            svg_content = await generate_contributions_svg(username, theme)
            filename = f"{username}_contributions_{theme}.svg"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            print(f"✅ {theme.title()} theme SVG saved as {filename}")
            
            # Show some stats about the generated SVG
            lines = svg_content.count('\n')
            squares = svg_content.count('<rect') - 1  # -1 for background rect
            print(f"   📊 Generated {lines} lines, {squares} contribution squares")
            
        except Exception as e:
            print(f"❌ {theme.title()} theme failed: {str(e)}")
    
    print(f"\n🎉 Test completed!")
    print(f"\n💡 Usage examples:")
    print(f"   python github_contributions.py {username}")
    print(f"   python github_contributions.py {username} dark")

if __name__ == "__main__":
    asyncio.run(test_contributions())
