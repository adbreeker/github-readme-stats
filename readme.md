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

### For Local Development

```bash
cd PythonRemake
python app.py
```

The server will start on `http://localhost:5000`

### For Production (Vercel)

Once deployed on Vercel, your API will be available at:
```
https://your-app.vercel.app/
```

### API Endpoints

#### Stats Card
```
GET /api?username=USERNAME&[options]
```

**Local Example:**
```
http://localhost:5000/api?username=adbreeker&show_icons=true&count_private=true&title_color=0891b2&text_color=ffffff&icon_color=0891b2&bg_color=1c1917
```

**Production Example:**
```
https://your-app.vercel.app/api?username=adbreeker&show_icons=true&theme=dark
```

#### Top Languages Card
```
GET /api/top-langs/?username=USERNAME&[options]
```

### GitHub README Usage

Add these to your GitHub README:

```markdown
![GitHub Stats](https://your-app.vercel.app/api?username=yourusername&show_icons=true&theme=dark)
![Top Languages](https://your-app.vercel.app/api/top-langs/?username=yourusername&layout=compact&theme=dark)
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

## File Structure

- `api/index.py` - Vercel serverless function entry point
- `github_stats.py` - Core GitHub API interaction and data models
- `svg_renderer.py` - SVG card generation and rendering
- `api_handlers.py` - API request handlers for stats and languages
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration
- `.gitignore` - Git ignore rules

## Differences from JavaScript Version

1. **Language**: Python instead of JavaScript/Node.js
2. **Runtime**: Python serverless functions on Vercel
3. **Async**: Uses aiohttp for async HTTP requests
4. **Pixel-Perfect**: Matches original SVG output exactly
5. **Compatible**: Same API endpoints and parameters

## Deployment

### Deploy on Vercel (Recommended)

This project is optimized for deployment on Vercel as serverless functions.

#### Quick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/github-readme-stats-python)

#### Manual Deployment
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel --prod`
3. Set environment variables in Vercel dashboard:
   - `PAT_1` - Your GitHub Personal Access Token
   - `CACHE_SECONDS` - Cache duration (optional, default: 14400)

#### Environment Variables for Vercel
Set these in your Vercel project dashboard:
```
PAT_1=ghp_your_github_token_here
CACHE_SECONDS=14400
```

### Local Development
```bash
cd PythonRemake
export PAT_1=your_github_token
python app.py
```

### Other Deployment Options
For production deployment, you can also use:
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
