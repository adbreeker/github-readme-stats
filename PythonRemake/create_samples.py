"""
Simple test script to generate sample SVG cards without GitHub API
Creates mock data for immediate visual testing
"""

import os
import sys
from pathlib import Path

# Add the parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from github_stats import GitHubStats, THEMES
from svg_renderer import create_stats_card, create_top_languages_card

def create_mock_stats() -> GitHubStats:
    """Create mock GitHub stats for testing"""
    return GitHubStats(
        name="John Doe",
        total_stars=1250,
        total_commits=3420,
        total_issues=89,
        total_prs=156,
        total_prs_merged=134,
        total_reviews=45,
        contributed_to=23,
        rank=2,
        percentile=85.5
    )

def create_mock_languages() -> list:
    """Create mock language data for testing"""
    return [
        {"name": "JavaScript", "color": "#f1e05a", "size": 15420},
        {"name": "Python", "color": "#3572A5", "size": 12340},
        {"name": "TypeScript", "color": "#2b7489", "size": 8920},
        {"name": "HTML", "color": "#e34c26", "size": 5680},
        {"name": "CSS", "color": "#563d7c", "size": 3240},
        {"name": "Java", "color": "#b07219", "size": 2890},
        {"name": "C++", "color": "#f34b7d", "size": 1560},
        {"name": "Go", "color": "#00ADD8", "size": 980},
    ]

def generate_sample_cards():
    """Generate sample SVG cards for testing"""
    
    # Create Tests directory
    tests_dir = Path(__file__).parent / 'Tests'
    tests_dir.mkdir(exist_ok=True)
    
    print("Generating sample SVG cards...")
    
    # Create mock data
    stats = create_mock_stats()
    languages = create_mock_languages()
    
    # Test configurations matching your original URLs
    test_configs = [
        {
            'name': 'stats_card_original_style',
            'type': 'stats',
            'options': {
                'show_icons': True,
                'title_color': '0891b2',
                'text_color': 'ffffff',
                'icon_color': '0891b2',
                'bg_color': '1c1917',
                'width': 495
            }
        },
        {
            'name': 'top_langs_dark_theme',
            'type': 'languages',
            'options': {
                'theme': 'dark',
                'title_color': '0891b2',
                'hide': ['html', 'css'],
                'width': 300
            }
        }
    ]
    
    # Generate test configuration cards
    for config in test_configs:
        if config['type'] == 'stats':
            svg_content = create_stats_card(stats, config['options'])
        else:
            svg_content = create_top_languages_card(languages, config['options'])
        
        file_path = tests_dir / f"{config['name']}.svg"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Generated: {file_path}")
    
    # Generate theme examples
    print("\nGenerating theme examples...")
    
    for theme_name in THEMES.keys():
        # Stats card with theme
        options = {'theme': theme_name, 'show_icons': True, 'width': 495}
        svg_content = create_stats_card(stats, options)
        
        file_path = tests_dir / f'stats_{theme_name}_theme.svg'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Generated stats card ({theme_name}): {file_path}")
        
        # Languages card with theme
        options = {'theme': theme_name, 'layout': 'normal', 'width': 300}
        svg_content = create_top_languages_card(languages, options)
        
        file_path = tests_dir / f'languages_{theme_name}_theme.svg'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Generated languages card ({theme_name}): {file_path}")
    
    # Generate layout examples
    print("\nGenerating layout examples...")
    
    layouts = ['normal', 'compact']
    for layout in layouts:
        options = {'theme': 'dark', 'layout': layout, 'width': 350}
        svg_content = create_top_languages_card(languages, options)
        
        file_path = tests_dir / f'languages_{layout}_layout.svg'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✓ Generated languages card ({layout} layout): {file_path}")
    
    print(f"\n🎉 Sample cards generated successfully!")
    print(f"📁 Location: {tests_dir}")
    print("\nGenerated files:")
    for svg_file in sorted(tests_dir.glob('*.svg')):
        print(f"  - {svg_file.name}")
    
    print(f"\n💡 You can open these SVG files in a web browser to preview them.")

if __name__ == '__main__':
    generate_sample_cards()
