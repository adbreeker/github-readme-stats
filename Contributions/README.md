# GitHub Contributions SVG Generator

This module generates SVG representations of GitHub contributions graphs that match the exact appearance of the contributions calendar on GitHub profile pages.

## ✨ Features

- **🎯 Exact GitHub styling**: Uses the same colors, fonts, and layout as GitHub's contributions graph
- **🌓 Theme support**: Both light and dark themes with authentic GitHub colors
- **📅 Perfect calendar logic**: Shows contributions for exactly 53 weeks starting from Sunday
- **⏰ Current date awareness**: Properly positions today's square based on the current date
- **📊 Responsive grid**: 53 weeks × 7 days grid matching GitHub's exact layout
- **💬 Tooltips**: Hover information showing date and contribution count
- **🏷️ Legend**: Visual legend showing contribution intensity levels
- **⚠️ Error handling**: Graceful error handling with informative SVG messages

## 🎨 Colors

### Light Theme
- **Empty**: `#ebedf0` (no contributions)
- **Level 1**: `#9be9a8` (1-2 contributions)
- **Level 2**: `#40c463` (3-5 contributions)
- **Level 3**: `#30a14e` (6-8 contributions)  
- **Level 4**: `#216e39` (9+ contributions)

### Dark Theme
- **Empty**: `#161b22` (no contributions)
- **Level 1**: `#0e4429` (1-2 contributions)
- **Level 2**: `#006d32` (3-5 contributions)
- **Level 3**: `#26a641` (6-8 contributions)
- **Level 4**: `#39d353` (9+ contributions)

## 🚀 Setup

1. **Install dependencies**:
   ```bash
   pip install aiohttp python-dotenv
   ```

2. **Set up GitHub token**:
   - Create a GitHub Personal Access Token at [github.com/settings/tokens](https://github.com/settings/tokens)
   - No special permissions needed for public profiles
   - Set the `GITHUB_TOKEN` environment variable:
     ```powershell
     # Windows PowerShell
     $env:GITHUB_TOKEN="your_token_here"
     ```
   - Or create a `.env` file:
     ```
     GITHUB_TOKEN=your_token_here
     ```

## 💻 Usage

### Command Line
```bash
# Generate light theme (default)
python github_contributions.py username

# Generate dark theme
python github_contributions.py username dark
```

### Programmatic Usage
```python
import asyncio
from github_contributions import generate_contributions_svg

async def main():
    # Generate SVG content
    svg_content = await generate_contributions_svg("username", "light")
    
    # Save to file
    with open("contributions.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

asyncio.run(main())
```

## 📅 Calendar Logic

The contributions calendar follows GitHub's exact logic:

1. **📍 Week starts on Sunday**: GitHub's calendar always starts weeks on Sunday
2. **📊 53 weeks displayed**: Shows exactly 53 weeks (371 days) ending with the current week
3. **⭐ Current date positioning**: 
   - If today is **Sunday**: One square in the last column
   - If today is **Saturday**: Seven squares in the last column
4. **🕐 Past year coverage**: Always shows contributions for the past ~371 days

### Current Date Examples (June 22, 2025 - Sunday)
Since today is Sunday, the contributions graph will show:
- 52 complete weeks of squares (7 squares each)
- 1 square in the final week (today's square in the top-right position)

## 📁 Files

- `github_contributions.py` - Main contributions generator
- `test_contributions.py` - Interactive test script
- `demo_calendar_logic.py` - Demonstrates calendar positioning logic
- `README.md` - This documentation

## 🧪 Testing

Run the interactive test script:
```bash
python test_contributions.py
```

Or test the calendar logic:
```bash
python demo_calendar_logic.py
```

The test will:
- Check for GitHub token
- Ask for a username (defaults to 'octocat')
- Generate both light and dark theme SVGs
- Show statistics about the generated files

## 📊 Example Output

The generated SVG includes:
- **Username and total contributions** count at the top
- **Month labels** (Jan, Feb, Mar, etc.) across the top
- **Weekday labels** (Mon, Wed, Fri) on the left side
- **53×7 grid** of contribution squares with accurate colors
- **Interactive tooltips** with exact dates and contribution counts
- **Legend** at the bottom showing contribution intensity levels

## 🔧 Error Handling

The generator handles various error conditions gracefully:
- ❌ Missing GitHub token → Clear setup instructions
- ❌ Invalid usernames → Informative error SVG
- ❌ API rate limits → Helpful error message
- ❌ Network errors → Fallback error display
- ❌ Invalid themes → Defaults to light theme

All errors result in valid SVG files with clear error messages rather than crashes.

## 🎯 Accuracy

This generator creates pixel-perfect replicas of GitHub's contributions graph:
- ✅ Exact color values from GitHub's CSS
- ✅ Same fonts (system font stack)
- ✅ Identical spacing and dimensions
- ✅ Proper week start (Sunday) logic
- ✅ Accurate current date positioning
- ✅ Same tooltip format and content
