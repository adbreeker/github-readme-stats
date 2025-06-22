"""
GitHub Contributions SVG Generator
Creates an SVG representation of GitHub contributions graph exactly like on GitHub
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import calendar
import os
from dotenv import load_dotenv
from chars_patterns import generate_text_pattern

# Load environment variables
load_dotenv()

# GitHub API endpoint for contributions
GITHUB_API_URL = "https://api.github.com/graphql"

# Exact GitHub colors for contributions
GITHUB_COLORS = {
    "light": {
        "bg": "#ebedf0",  # Empty/no contributions
        "level1": "#9be9a8",  # 1-2 contributions
        "level2": "#40c463",  # 3-5 contributions  
        "level3": "#30a14e",  # 6-8 contributions
        "level4": "#216e39",  # 9+ contributions
        "text": "#656d76",
        "border": "#d1d9e0"
    },
    "dark": {
        "bg": "#161b22",  # Empty/no contributions
        "level1": "#0e4429",  # 1-2 contributions
        "level2": "#006d32",  # 3-5 contributions
        "level3": "#26a641",  # 6-8 contributions
        "level4": "#39d353",  # 9+ contributions
        "text": "#7d8590",
        "border": "#21262d"
    }
}

# GraphQL query for contributions
CONTRIBUTIONS_QUERY = """
query userInfo($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        colors
        totalContributions
        weeks {
          contributionDays {
            color
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}
"""

class GitHubContributionsAPI:
    """GitHub API client for fetching contributions data"""
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN') or os.getenv('PAT_1')
        if not self.token:
            raise ValueError("GITHUB_TOKEN or PAT_1 environment variable is required")
    
    async def fetch_contributions(self, username: str) -> Dict:
        """Fetch contributions data from GitHub API"""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }
        
        variables = {'login': username}
        payload = {
            'query': CONTRIBUTIONS_QUERY,
            'variables': variables
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(GITHUB_API_URL, 
                                   headers=headers, 
                                   json=payload) as response:
                if response.status != 200:
                    raise Exception(f"GitHub API error: {response.status}")
                
                data = await response.json()
                
                if 'errors' in data:
                    raise Exception(f"GraphQL errors: {data['errors']}")
                
                return data['data']['user']['contributionsCollection']['contributionCalendar']

def get_contributions_year_range() -> Tuple[datetime, datetime]:
    """Get the start and end dates for the contributions calendar
    GitHub shows exactly 53 weeks ending with today (not padded to end of week)"""
    today = datetime.now(timezone.utc).date()
    
    # Calculate current Sunday (GitHub weeks start on Sunday)
    # weekday(): Monday=0, Sunday=6, so we need to adjust
    days_since_sunday = (today.weekday() + 1) % 7
    current_sunday = today - timedelta(days=days_since_sunday)
    
    # Start date is 52 weeks (364 days) before current Sunday
    # This gives us exactly 53 weeks (52 full weeks + current partial week)
    start_date = current_sunday - timedelta(weeks=52)
    
    # End date is today (not padded to end of week)
    return datetime.combine(start_date, datetime.min.time(), timezone.utc), \
           datetime.combine(today, datetime.max.time(), timezone.utc)

def generate_contributions_grid(contributions_data: Dict, theme: str = "light") -> Tuple[List[List[Dict]], int, int]:
    """Generate contributions grid - 52 full weeks + current partial week"""
    colors = GITHUB_COLORS[theme]
    
    # Get the date range and calculate actual weeks needed
    start_date, end_date = get_contributions_year_range()
    today = datetime.now(timezone.utc).date()
    
    # Calculate how many days are in the current (partial) week
    days_since_sunday = (today.weekday() + 1) % 7
    current_week_days = days_since_sunday + 1  # +1 because we include today
    
    # Create grid: 52 full weeks + 1 partial week
    total_weeks = 53
    grid = []
    
    # Add 52 full weeks
    for week in range(52):
        grid.append([{"count": 0, "color": colors["bg"], "date": ""} for _ in range(7)])
    
    # Add partial current week (only the days that have passed)
    current_week = []
    for day in range(current_week_days):
        current_week.append({"count": 0, "color": colors["bg"], "date": ""})
    grid.append(current_week)
    
    total_contributions = contributions_data.get('totalContributions', 0)
    weeks = contributions_data.get('weeks', [])    # Process GitHub's weeks data
    for week_data in weeks:
        days = week_data.get('contributionDays', [])
        
        for day in days:
            date_str = day.get('date', '')
            if not date_str:
                continue
                
            # Parse the date
            try:
                # GitHub returns dates in YYYY-MM-DD format, convert to timezone-aware datetime
                if 'T' in date_str:
                    day_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    # If it's just a date string (YYYY-MM-DD), parse it and add timezone
                    day_date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except:
                continue
            
            # Check if this date falls within our display range
            if not (start_date <= day_date <= end_date):
                continue
            
            # Calculate which week this belongs to (from our start date)
            days_from_start = (day_date.date() - start_date.date()).days
            week_idx = days_from_start // 7
            weekday = day.get('weekday', 0)  # 0 = Sunday, 6 = Saturday
            
            # Check bounds - for the last week, only include days that exist
            if week_idx < len(grid) and weekday < len(grid[week_idx]):
                count = day.get('contributionCount', 0)
                
                # Determine color based on contribution count
                if count == 0:
                    color = colors["bg"]
                elif count <= 2:
                    color = colors["level1"] 
                elif count <= 5:
                    color = colors["level2"]
                elif count <= 8:
                    color = colors["level3"]
                else:
                    color = colors["level4"]
                
                grid[week_idx][weekday] = {
                    "count": count,
                    "color": color,
                    "date": date_str[:10]  # YYYY-MM-DD format
                }
    
    return grid, total_contributions, current_week_days

def create_contributions_svg(username: str, contributions_data: Dict, theme: str = "light", text: str = "ADBREEKER", line_color: str = "#ff8c00", line_alpha: float = 0.7) -> str:
    """Create SVG representation of GitHub contributions"""
    colors = GITHUB_COLORS[theme]
    grid, total_contributions, current_week_days = generate_contributions_grid(contributions_data, theme)
    
    # SVG dimensions - calculate based on actual grid structure
    square_size = 11
    square_margin = 2
    padding = 10
      # Calculate total dimensions based on actual grid
    # 52 full weeks + partial current week
    grid_width = 52 * (square_size + square_margin) + (square_size + square_margin) - square_margin
    grid_height = 7 * (square_size + square_margin) - square_margin
    total_width = grid_width + (padding * 2)
    total_height = grid_height + (padding * 2)
      # Animation parameters
    animation_duration = "8s"  # Extended duration for smooth sequence
    middle_column = len(grid) // 2  # Middle of the grid
    line_height = grid_height + 2 * (square_size + square_margin)  # One square taller on each side
    line_width = square_size    # Generate custom text pattern for animation
    text_patterns = generate_text_pattern(text)
    # Calculate total width needed for all letters
    total_text_width = max(text_patterns.keys()) + 4 if text_patterns else 0
    text_start_column = max(0, middle_column - total_text_width // 2)  # Center the text
    text_start_row = 1  # Start from row 1 (0-6, so 1-5 will be the text area)
      # Start building SVG with animation
    svg_parts = [
        f'<svg width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">',
        f'<defs>',
        f'<style>',
        f'.contrib-square {{ stroke-width: 1; stroke: rgba(27,31,35,0.06); rx: 2; ry: 2; }}',
        f'.eating-line {{ fill: {line_color}; }}',  # Customizable line color
        f'</style>',
        f'</defs>',
    ]# Add contribution squares with animation
    for week_idx, week in enumerate(grid):
        for day_idx, day_data in enumerate(week):
            x = padding + week_idx * (square_size + square_margin)
            y = padding + day_idx * (square_size + square_margin)
            
            # Format the tooltip text
            if day_data["date"]:
                # Parse date and format it nicely
                try:
                    date_obj = datetime.fromisoformat(day_data["date"]).date()
                    formatted_date = date_obj.strftime("%b %d, %Y")
                except:
                    formatted_date = day_data["date"]
                
                count_text = "No contributions" if day_data["count"] == 0 else f"{day_data['count']} contribution{'s' if day_data['count'] != 1 else ''}"
                tooltip_text = f"{count_text} on {formatted_date}"
            else:
                tooltip_text = "No data"
              # Check if this square should be part of ADBREEKER text
            is_text_square = False
            text_square_active = False
            
            # Check if we're in the text area (5 rows starting from text_start_row)
            if (day_idx >= text_start_row and day_idx < text_start_row + 5 and
                week_idx >= text_start_column):
                
                # Calculate which letter and position within the letter
                relative_col = week_idx - text_start_column
                relative_row = day_idx - text_start_row
                  # Find which letter this column belongs to
                for letter_start_col, letter_pattern in text_patterns.items():
                    if (relative_col >= letter_start_col and 
                        relative_col < letter_start_col + 4):  # Each letter is 4 cols wide
                        
                        letter_col = relative_col - letter_start_col
                        is_text_square = True
                        text_square_active = letter_pattern[relative_row][letter_col] == 1
                        break
            
            # Create the square with eating animation effect
            square_id = f"square-{week_idx}-{day_idx}"
            original_color = day_data["color"]
            empty_color = colors["bg"]
            text_color = colors["level3"]  # Use level 3 color for text
            
            svg_parts.append(
                f'<rect id="{square_id}" x="{x}" y="{y}" width="{square_size}" height="{square_size}" '
                f'fill="{original_color}" class="contrib-square">'
                f'<title>{tooltip_text}</title>'
            )              # Add eating animation - for contribution squares and text squares
            has_contribution = day_data["count"] > 0
            
            if has_contribution or is_text_square:
                # Animation sequence:
                # 0-25%: Lines come in, eat original squares (contributions only)
                # 25-50%: Lines go out, write ADBREEKER text (text squares appear)
                # 50-75%: Lines come back in, eat ADBREEKER text (text squares disappear)
                # 75-100%: Lines go out, restore original squares (contributions only)
                
                # Calculate timing based on column position
                total_columns = len(grid)
                
                if week_idx <= middle_column:
                    # Left line territory (columns 0 to middle_column inclusive)
                    if middle_column > 0:
                        eat_progress = week_idx / middle_column
                    else:
                        eat_progress = 0
                    # Ensure eat_time is never 0 to avoid keyframe issues
                    eat_time = max(0.1, eat_progress * 24.5)  # 0.1-24.5%
                    restore_time = 75 + (1 - eat_progress) * 24.5  # 75.5-99.5%
                else:
                    # Right line territory (columns after middle_column)
                    columns_from_right = total_columns - 1 - week_idx
                    max_columns_right = total_columns - middle_column - 1
                    if max_columns_right > 0:
                        eat_progress = columns_from_right / max_columns_right
                    else:
                        eat_progress = 0
                    # Ensure eat_time is never 0 to avoid keyframe issues
                    eat_time = max(0.1, eat_progress * 24.5)  # 0.1-24.5%
                    restore_time = 75 + (1 - eat_progress) * 24.5  # 75.5-99.5%                # Different animation sequences for different square types
                if is_text_square and text_square_active:
                    # Text squares: get written by lines during phase 2 (25-50%)
                    # Calculate when this square gets written based on distance from center
                    distance_from_center = abs(week_idx - middle_column)
                    max_distance = middle_column if week_idx <= middle_column else (len(grid) - 1 - middle_column)
                    
                    if max_distance > 0:
                        write_progress = distance_from_center / max_distance
                    else:
                        write_progress = 0
                    
                    # Text appears as lines move out during phase 2 (25-50%)
                    write_time = 25 + write_progress * 25  # 25-50%
                    
                    keyframes = [
                        0,                # Start: empty
                        25,               # Phase 1 end: still empty
                        write_time,       # Just before writing
                        write_time + 0.5, # Just after writing (text appears)
                        50,               # Phase 2 end: text visible
                        eat_time + 50,    # Just before eating in phase 3
                        eat_time + 50.5,  # Just after eating (empty)
                        100               # End: empty
                    ]
                    
                    colors_sequence = [
                        empty_color,      # Start: empty
                        empty_color,      # Phase 1 end: still empty
                        empty_color,      # Just before writing
                        text_color,       # Text appears (written by line)
                        text_color,       # Text visible through phase 2
                        text_color,       # Just before eating
                        empty_color,      # Just after eating
                        empty_color       # End: empty
                    ]
                elif has_contribution:
                    # Regular contribution squares: normal eating and restoring
                    keyframes = [
                        0,                # Start: original color
                        eat_time,         # Just before eating
                        eat_time + 0.5,   # Just after eating (empty)
                        75,               # Stay empty until restore phase
                        restore_time,     # Just before restoring
                        restore_time + 0.5, # Just after restoring (original)
                        100               # End: original color
                    ]
                    
                    colors_sequence = [
                        original_color,  # Start
                        original_color,  # Just before eating
                        empty_color,     # Just after eating
                        empty_color,     # Stay empty through phases 2 and 3
                        empty_color,     # Just before restoring
                        original_color,  # Just after restoring
                        original_color   # End
                    ]
                else:
                    # Empty text squares (spaces): stay empty throughout
                    keyframes = [0, 100]
                    colors_sequence = [empty_color, empty_color]                
                # Convert to keyTimes format (0-1) and apply animation
                key_times = [t/100 for t in keyframes]
                key_times_str = ';'.join([f'{t:.3f}' for t in key_times])
                colors_str = ';'.join(colors_sequence)
                
                svg_parts.append(
                    f'<animate attributeName="fill" '
                    f'values="{colors_str}" '
                    f'dur="{animation_duration}" '
                    f'keyTimes="{key_times_str}" '
                    f'repeatCount="indefinite"/>'
                )
            
            svg_parts.append('</rect>')
    
    # Add the eating lines (visual indicators) - smooth movement
    line_start_y = padding - (square_size + square_margin)
      # Left eating line
    left_line_start_x = padding - line_width
    left_line_end_x = padding + middle_column * (square_size + square_margin)
    
    svg_parts.append(
        f'<rect class="eating-line" x="{left_line_start_x}" y="{line_start_y}" '
        f'width="{line_width}" height="{line_height}" rx="2" opacity="{line_alpha}">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0,0;{left_line_end_x - left_line_start_x},0;0,0;{left_line_end_x - left_line_start_x},0;0,0" '
        f'dur="{animation_duration}" '
        f'keyTimes="0;0.25;0.5;0.75;1" '
        f'repeatCount="indefinite"/>'
        f'</rect>'
    )
      # Right eating line  
    right_line_start_x = padding + len(grid) * (square_size + square_margin)
    right_line_end_x = padding + middle_column * (square_size + square_margin)
    
    svg_parts.append(
        f'<rect class="eating-line" x="{right_line_start_x}" y="{line_start_y}" '
        f'width="{line_width}" height="{line_height}" rx="2" opacity="{line_alpha}">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0,0;{right_line_end_x - right_line_start_x},0;0,0;{right_line_end_x - right_line_start_x},0;0,0" '
        f'dur="{animation_duration}" '
        f'keyTimes="0;0.25;0.5;0.75;1" '
        f'repeatCount="indefinite"/>'
        f'</rect>'
    )
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)

async def generate_contributions_svg(username: str, theme: str = "light", text: str = "ADBREEKER", line_color: str = "#ff8c00", line_alpha: float = 0.7) -> str:
    """Main function to generate contributions SVG"""
    try:
        api = GitHubContributionsAPI()
        contributions_data = await api.fetch_contributions(username)
        return create_contributions_svg(username, contributions_data, theme, text, line_color, line_alpha)
    except ValueError as e:
        # Token-related errors
        return f'''<svg width="500" height="100" xmlns="http://www.w3.org/2000/svg">
            <rect width="500" height="100" fill="#f6f8fa" stroke="#d1d5da"/>
            <text x="250" y="35" text-anchor="middle" fill="#d73a49" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="14" font-weight="600">GitHub Token Error</text>
            <text x="250" y="55" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="12">Set GITHUB_TOKEN or PAT_1 environment variable</text>
            <text x="250" y="75" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="11">Create token at github.com/settings/tokens</text>
        </svg>'''
    except Exception as e:
        # Other errors with more details
        error_msg = str(e)
        if "offset-naive and offset-aware" in error_msg:
            error_msg = "Date/time processing error"
        elif "GraphQL" in error_msg:
            error_msg = "GitHub API error - check username"
        elif "404" in error_msg or "Not Found" in error_msg:
            error_msg = f"User '{username}' not found"
        else:
            error_msg = error_msg[:60] + "..." if len(error_msg) > 60 else error_msg
            
        return f'''<svg width="500" height="100" xmlns="http://www.w3.org/2000/svg">
            <rect width="500" height="100" fill="#f6f8fa" stroke="#d1d5da"/>
            <text x="250" y="35" text-anchor="middle" fill="#d73a49" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="14" font-weight="600">Error generating contributions</text>
            <text x="250" y="55" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="12">{error_msg}</text>
            <text x="250" y="75" text-anchor="middle" fill="#586069" 
                  font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                  font-size="11">Check username and token</text>
        </svg>'''

# CLI usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python github_contributions.py <username> [theme] [text] [line_color] [line_alpha]")
        print("Theme options: light (default), dark")
        print("Text: custom text to animate (default: ADBREEKER)")
        print("Line color: hex color for eating lines (default: #ff8c00)")
        print("Line alpha: transparency 0.0-1.0 (default: 0.7)")
        print("Examples:")
        print("  python github_contributions.py adbreeker")
        print("  python github_contributions.py adbreeker dark")
        print("  python github_contributions.py adbreeker light \"HELLO WORLD\"")
        print("  python github_contributions.py adbreeker dark \"2025\" \"#00ff00\" 0.8")
        sys.exit(1)
    
    username = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else "light"
    text = sys.argv[3] if len(sys.argv) > 3 else "ADBREEKER"
    line_color = sys.argv[4] if len(sys.argv) > 4 else "#ff8c00"
    line_alpha = float(sys.argv[5]) if len(sys.argv) > 5 else 0.7
    
    if theme not in ["light", "dark"]:
        print("Invalid theme. Use 'light' or 'dark'")
        sys.exit(1)
    
    if not (0.0 <= line_alpha <= 1.0):
        print("Invalid line alpha. Use a value between 0.0 and 1.0")
        sys.exit(1)
    
    # Validate hex color format
    if not line_color.startswith('#') or len(line_color) not in [4, 7]:
        print("Invalid line color. Use hex format like #ff8c00 or #f80")
        sys.exit(1)
    
    async def main():
        svg_content = await generate_contributions_svg(username, theme, text, line_color, line_alpha)
        # Create filename with text info
        safe_text = "".join(c for c in text if c.isalnum())[:10]  # Safe filename
        filename = f"{username}_contributions_{theme}_{safe_text}.svg"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"Contributions SVG saved as {filename}")
        print(f"Animated text: '{text}'")
        print(f"Line color: {line_color}, Alpha: {line_alpha}")
    
    asyncio.run(main())
