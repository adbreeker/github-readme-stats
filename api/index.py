"""
Vercel Serverless Function Entry Point
Handles GitHub Stats API requests for deployment on Vercel
"""

from flask import Flask, request, Response
import asyncio
import os
import sys

# Add the parent directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import handlers after setting up the path
try:
    from api_handlers import StatsAPIHandler, TopLanguagesAPIHandler
    
    # Initialize handlers
    stats_handler = StatsAPIHandler()
    langs_handler = TopLanguagesAPIHandler()
    HANDLERS_LOADED = True
except Exception as e:
    print(f"Error loading handlers: {e}")
    HANDLERS_LOADED = False

# Create Flask app
app = Flask(__name__)

def run_async(coro):
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a new loop
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create a new one
        return asyncio.run(coro)

def create_error_svg(width, height, title, message):
    """Create an error SVG"""
    return f'''
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .error-title {{ font: 600 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e74c3c; }}
            .error-text {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #586069; }}
        </style>
        <rect width="{width}" height="{height}" fill="#fffefe" stroke="#e4e2e2" stroke-width="1" rx="4"/>
        <text x="25" y="35" class="error-title">{title}</text>
        <text x="25" y="60" class="error-text">{message}</text>
    </svg>
    '''

@app.route('/')
def index():
    """Root endpoint with basic info"""
    status = "✅ Ready" if HANDLERS_LOADED else "❌ Error loading handlers"
    return f'''
    <html>
    <head>
        <title>GitHub Stats API - Python on Vercel</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
            .status {{ padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .ready {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            code {{ background: #f1f1f1; padding: 2px 4px; border-radius: 3px; }}
            .example {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>🐍 GitHub Stats API - Python</h1>
        <div class="status {'ready' if HANDLERS_LOADED else 'error'}">
            <strong>Status:</strong> {status}
        </div>
        
        <h2>📊 Available Endpoints</h2>
        <ul>
            <li><strong>/api</strong> - GitHub user statistics card</li>
            <li><strong>/api/top-langs</strong> - Top programming languages card</li>
        </ul>
        
        <h2>🎨 Example Usage</h2>        <div class="example">
            <h3>Stats Card</h3>
            <code>/api?username=adbreeker&show_icons=true&theme=dark</code>
            <br><br>
            <img src="/api?username=adbreeker&show_icons=true&theme=dark" alt="Stats Card Example" style="max-width: 100%;">
            <br><br>
            <p><em>Replace 'adbreeker' with any GitHub username to see their stats</em></p>
        </div>
        
        <div class="example">
            <h3>Top Languages</h3>
            <code>/api/top-langs?username=adbreeker&layout=compact&theme=dark</code>
            <br><br>
            <img src="/api/top-langs?username=adbreeker&layout=compact&theme=dark" alt="Languages Card Example" style="max-width: 100%;">
            <br><br>
            <p><em>Replace 'adbreeker' with any GitHub username to see their top languages</em></p>
        </div>
        
        <h2>🔧 Configuration</h2>
        <p>Environment variables required:</p>
        <ul>
            <li><code>PAT_1</code> - GitHub Personal Access Token</li>
            <li><code>CACHE_SECONDS</code> - Cache duration (optional)</li>
        </ul>
        
        <h2>🚀 Deployment</h2>
        <p>This is a Python remake of the popular GitHub README Stats, deployed on Vercel with pixel-perfect SVG output matching the original.</p>
        
        <h2>📚 Resources</h2>
        <ul>
            <li><a href="https://github.com/anuraghazra/github-readme-stats">Original JavaScript Version</a></li>
            <li><a href="https://vercel.com">Vercel Deployment Platform</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api')
def stats_api():
    """GitHub stats API endpoint"""
    if not HANDLERS_LOADED:
        return Response(
            create_error_svg(495, 120, "Service Unavailable", "Handlers not loaded"),
            content_type='image/svg+xml'
        )
    
    try:
        svg_content, headers = run_async(
            stats_handler.handle_request(request.query_string.decode())
        )
        return Response(svg_content, content_type=headers['Content-Type'], headers=headers)
    except Exception as e:
        return Response(
            create_error_svg(495, 120, "Internal Server Error", str(e)[:100]),
            content_type='image/svg+xml'
        )

@app.route('/api/top-langs')
@app.route('/api/top-langs/')  # Add support for trailing slash
def top_langs_api():
    """Top languages API endpoint"""
    if not HANDLERS_LOADED:
        return Response(
            create_error_svg(300, 120, "Service Unavailable", "Handlers not loaded"),
            content_type='image/svg+xml'
        )
    
    try:
        svg_content, headers = run_async(
            langs_handler.handle_request(request.query_string.decode())
        )
        return Response(svg_content, content_type=headers['Content-Type'], headers=headers)
    except Exception as e:
        return Response(
            create_error_svg(300, 120, "Internal Server Error", str(e)[:100]),
            content_type='image/svg+xml'
        )

# Health check endpoint
@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        "status": "healthy" if HANDLERS_LOADED else "unhealthy",
        "handlers_loaded": HANDLERS_LOADED,
        "python_version": sys.version,
        "environment": "vercel"
    }

# Export the app for Vercel
# Note: Vercel will automatically detect this as the main handler
if __name__ == '__main__':
    app.run(debug=True)
