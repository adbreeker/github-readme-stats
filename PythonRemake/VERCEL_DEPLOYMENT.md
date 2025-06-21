# Deploying GitHub Stats API to Vercel

## Quick Setup

### 1. Prepare Your Repository
Make sure all files are in your repository:
- `vercel.json` - Vercel configuration
- `api/index.py` - Main serverless function
- `requirements.txt` - Python dependencies
- All your source files (`api_handlers.py`, `svg_renderer.py`, `github_stats.py`)

### 2. Environment Variables
In your Vercel dashboard, add these environment variables:
- `PAT_1` - Your GitHub Personal Access Token
- `CACHE_SECONDS` - Cache duration (optional, default: 14400)

### 3. Deploy Options

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option B: GitHub Integration
1. Connect your GitHub repository to Vercel
2. Push your code to GitHub
3. Vercel will automatically deploy

### 4. Usage After Deployment
Your API will be available at:
- `https://your-app.vercel.app/api?username=octocat`
- `https://your-app.vercel.app/api/top-langs?username=octocat`

## File Structure for Vercel
```
PythonRemake/
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── api/
│   └── index.py            # Main serverless function entry point
├── api_handlers.py         # Your API logic
├── svg_renderer.py         # SVG generation
├── github_stats.py         # GitHub API integration
└── .env                    # Local development only (not deployed)
```

## Important Notes

### Vercel Limitations
- **Cold starts**: First request may be slower
- **Execution time**: 10-second timeout for hobby tier
- **Memory**: Limited memory compared to dedicated servers

### GitHub API Rate Limits
- Without authentication: 60 requests/hour
- With PAT: 5000 requests/hour
- Consider implementing caching for production use

### Alternative Deployment Options
If Vercel doesn't work well, consider:
- **Heroku** - Better for Flask apps
- **Railway** - Modern alternative to Heroku  
- **Google Cloud Run** - Serverless containers
- **AWS Lambda** - With Zappa or Serverless framework

## Troubleshooting

### Common Issues
1. **Import errors**: Make sure all files are in the repository
2. **Environment variables**: Set PAT_1 in Vercel dashboard
3. **Path issues**: Use absolute imports where possible
4. **Async issues**: The handler uses `run_async()` helper

### Testing Locally
```bash
# Test the Vercel function locally
vercel dev

# Or run Flask normally
python app.py
```

## Production Optimizations

### Caching
Consider adding Redis or another caching layer for better performance:
```python
# Add to requirements.txt
redis==4.5.1

# Implement caching in api_handlers.py
import redis
cache = redis.from_url(os.environ.get('REDIS_URL'))
```

### Error Monitoring
Add error tracking:
```python
# Add to requirements.txt  
sentry-sdk==1.32.0

# Initialize in api/index.py
import sentry_sdk
sentry_sdk.init(dsn=os.environ.get('SENTRY_DSN'))
```
