# GitHub Stats API - Python Implementation

This is a Python remake of the GitHub README Stats service that generates SVG cards for GitHub user statistics and top programming languages.

## Features

- **Stats Card**: Displays GitHub user statistics (stars, commits, PRs, issues, contributions)
- **Top Languages Card**: Shows the most used programming languages
- **Multiple Themes**: Support for various color themes (dark, radical, merko, etc.)
- **Customizable**: Colors, layouts, and display options can be customized
- **Token Rotation**: Automatic GitHub API token rotation for rate limiting
- **Caching**: Configurable cache headers for performance

## Installation

### Requirements

```bash
pip install aiohttp flask python-dotenv
```

### Environment Variables

You need a GitHub Personal Access Token to access the GitHub API.

#### 1. Create a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "GitHub Stats API"
4. Select scopes: `public_repo` (or `repo` if you want private repo access)
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)

#### 2. Create Environment File

Create a `.env` file in the PythonRemake directory:

```env
# GitHub Personal Access Token (required)
PAT_1=ghp_your_github_token_here

# Cache duration in seconds (optional, default: 14400 = 4 hours)
CACHE_SECONDS=14400

# Flask configuration (optional)
FLASK_ENV=development
PORT=5000
```

**⚠️ Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Running the Server

```bash
cd PythonRemake
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Stats Card
```
GET /api?username=USERNAME&[options]
```

**Example:**
```
/api?username=adbreeker&show_icons=true&count_private=true&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=1c1917
```

#### Top Languages Card
```
GET /api/top-langs/?username=USERNAME&[options]
```

**Example:**
```
/api/top-langs/?username=adbreeker&show_icons=true&count_private=true&theme=dark&title_color=0891b2&hide=tcl,html,css,powershell,scss,shaderlab
```

### Parameters

#### Common Parameters
- `username` - GitHub username (required)
- `theme` - Theme name (default, dark, radical, merko, gruvbox, tokyonight)
- `title_color` - Title color (hex without #)
- `text_color` - Text color (hex without #)
- `icon_color` - Icon color (hex without #)
- `bg_color` - Background color (hex without #)
- `border_color` - Border color (hex without #)
- `hide_border` - Hide border (true/false)
- `hide_title` - Hide title (true/false)
- `card_width` - Card width in pixels
- `border_radius` - Border radius in pixels

#### Stats Card Parameters
- `show_icons` - Show icons (true/false)
- `hide` - Comma-separated list of stats to hide (stars,commits,prs,issues,contribs)
- `custom_title` - Custom card title

#### Top Languages Card Parameters
- `layout` - Layout style (normal, compact)
- `hide` - Comma-separated list of languages to hide
- `hide_progress` - Hide progress bars (true/false)

## Testing

### Generate Test Cards

```bash
cd PythonRemake
python generate_test_cards.py
```

This will generate sample SVG cards in the `Tests/` directory for visual testing.

## File Structure

- `github_stats.py` - Core GitHub API interaction and data models
- `svg_renderer.py` - SVG card generation and rendering
- `api_handlers.py` - API request handlers for stats and languages
- `app.py` - Flask web server
- `generate_test_cards.py` - Test card generation script
- `Tests/` - Generated test SVG files

## Differences from JavaScript Version

1. **Language**: Python instead of JavaScript/Node.js
2. **Framework**: Flask instead of Vercel serverless functions
3. **Async**: Uses aiohttp for async HTTP requests
4. **Simplified**: Some advanced features simplified for core functionality
5. **Standalone**: Can run as a standalone server

## Deployment

### Local Development
```bash
cd PythonRemake
export PAT_1=your_github_token
python app.py
```

### Production
For production deployment, you can use:
- **Heroku**: Deploy as a Flask app
- **Docker**: Containerize the application
- **VPS**: Run with gunicorn/uwsgi

### Docker Example
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## API Compatibility

The API is designed to be compatible with the original JavaScript version:

- Same URL structure
- Same query parameters
- Same SVG output format
- Same error handling

You can use the same markdown syntax in your GitHub README:

```markdown
![GitHub Stats](http://localhost:5000/api?username=yourusername&show_icons=true&theme=dark)
![Top Languages](http://localhost:5000/api/top-langs/?username=yourusername&layout=compact&theme=dark)
```
