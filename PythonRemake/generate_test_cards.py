"""
Test script to generate sample SVG cards and save them for development testing
"""

import asyncio
import os
from pathlib import Path

# Add the parent directory to the path so we can import our modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_handlers import StatsAPIHandler, TopLanguagesAPIHandler

async def generate_test_cards():
    """Generate test cards and save them as SVG files"""
    
    # Test data URLs (matching your original examples)
    test_urls = {
        'stats_card': 'username=adbreeker&show_icons=true&count_private=true&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=1c1917&show_icons=true',
        'top_langs_card': 'username=adbreeker&show_icons=true&count_private=true&theme=dark&title_color=0891b2&hide=tcl,html,css,powershell,scss,shaderlab'
    }
    
    # Create handlers
    stats_handler = StatsAPIHandler()
    langs_handler = TopLanguagesAPIHandler()
    
    # Create Tests directory
    tests_dir = Path(__file__).parent / 'Tests'
    tests_dir.mkdir(exist_ok=True)
    
    print("Generating test cards...")
    
    try:
        # Generate stats card
        print("Generating stats card...")
        svg_content, headers = await stats_handler.handle_request(test_urls['stats_card'])
        
        stats_file = tests_dir / 'stats_card_test.svg'
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Stats card saved to: {stats_file}")
        
        # Generate top languages card
        print("Generating top languages card...")
        svg_content, headers = await langs_handler.handle_request(test_urls['top_langs_card'])
        
        langs_file = tests_dir / 'top_langs_card_test.svg'
        with open(langs_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Top languages card saved to: {langs_file}")
        
        # Generate additional theme examples
        themes = ['default', 'dark', 'radical', 'merko', 'gruvbox', 'tokyonight']
        
        print("\nGenerating theme examples...")
        for theme in themes:
            # Stats card with theme
            theme_query = f'username=adbreeker&show_icons=true&theme={theme}'
            svg_content, _ = await stats_handler.handle_request(theme_query)
            
            theme_file = tests_dir / f'stats_card_{theme}_theme.svg'
            with open(theme_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✓ Stats card ({theme} theme) saved to: {theme_file}")
            
            # Top languages card with theme
            theme_query = f'username=adbreeker&theme={theme}&layout=compact'
            svg_content, _ = await langs_handler.handle_request(theme_query)
            
            theme_file = tests_dir / f'top_langs_{theme}_theme.svg'
            with open(theme_file, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"✓ Top languages card ({theme} theme) saved to: {theme_file}")
        
        print(f"\n🎉 All test cards generated successfully in: {tests_dir}")
        print("\nGenerated files:")
        for svg_file in sorted(tests_dir.glob('*.svg')):
            print(f"  - {svg_file.name}")
            
    except Exception as e:
        print(f"❌ Error generating test cards: {str(e)}")
        print("Make sure you have set the PAT_1 environment variable with a valid GitHub token")

if __name__ == '__main__':
    # Check if GitHub token is set
    if not os.getenv('PAT_1'):
        print("❌ Error: PAT_1 environment variable not set!")
        print("Please set your GitHub Personal Access Token:")
        print("export PAT_1=your_github_token_here")
        exit(1)
    
    asyncio.run(generate_test_cards())
