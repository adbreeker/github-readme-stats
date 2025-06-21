# GitHub Stats API - Python on Vercel

A pixel-perfect Python remake of the popular [GitHub README Stats](https://github.com/anuraghazra/github-readme-stats), deployed as serverless functions on Vercel.

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/github-readme-stats-python)

## 📋 Setup Instructions

### 1. Clone & Deploy
```bash
git clone <your-repo-url>
cd github-readme-stats-python/PythonRemake
vercel --prod
```

### 2. Environment Variables
Set these in your Vercel dashboard:
- `PAT_1` - Your GitHub Personal Access Token
- `CACHE_SECONDS` - Cache duration (optional, default: 14400)

### 3. Get Your GitHub PAT
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with these scopes:
   - `read:user`
   - `public_repo`
   - `read:org` (if you want to include private contributions)

## 🎨 Usage

Once deployed, your API will be available at:

### Stats Card
```
https://your-app.vercel.app/api?username=YOUR_USERNAME
```

### Top Languages Card
```
https://your-app.vercel.app/api/top-langs?username=YOUR_USERNAME
```

### Customization Options
Add these parameters to customize your cards:

**Colors & Themes:**
- `theme=dark` - Use dark theme
- `title_color=58A6FF` - Custom title color
- `text_color=C9D1D9` - Custom text color
- `icon_color=58A6FF` - Custom icon color
- `bg_color=0D1117` - Custom background color

**Stats Card Options:**
- `show_icons=true` - Show icons
- `count_private=true` - Include private repos
- `hide=issues,prs` - Hide specific stats
- `line_height=25` - Adjust line height
- `card_width=500` - Custom card width

**Languages Card Options:**
- `layout=compact` - Use compact layout
- `langs_count=8` - Number of languages to show
- `hide=html,css` - Hide specific languages

## 🎯 Features

- ✅ **Pixel-perfect** - Identical output to original JS version
- ✅ **All themes** - Support for all original themes
- ✅ **All parameters** - Complete feature parity
- ✅ **Fast deployment** - Serverless on Vercel
- ✅ **Auto-scaling** - Handles traffic spikes
- ✅ **Error handling** - Graceful fallbacks

## 📊 Example Cards

### Default Theme
![Stats Card](https://your-app.vercel.app/api?username=octocat&show_icons=true)

### Dark Theme
![Stats Card Dark](https://your-app.vercel.app/api?username=octocat&show_icons=true&theme=dark)

### Languages Compact
![Languages](https://your-app.vercel.app/api/top-langs?username=octocat&layout=compact&theme=dark)

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your PAT_1

# Run locally
python app.py
# Or test Vercel version
python api/index.py
```

## 📁 Project Structure

```
PythonRemake/
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── api/
│   └── index.py            # Vercel serverless entry point
├── app.py                  # Local Flask server
├── api_handlers.py         # API request handlers
├── svg_renderer.py         # SVG card generation
├── github_stats.py         # GitHub API integration
└── VERCEL_DEPLOYMENT.md    # Detailed deployment guide
```

## 🚨 Important Notes

### Rate Limits
- Without PAT: 60 requests/hour per IP
- With PAT: 5,000 requests/hour
- Consider implementing caching for high-traffic usage

### Vercel Limits (Hobby Tier)
- 10 second execution timeout
- 1024MB memory limit
- Cold start latency on first request

## 🆚 vs Original

This Python version provides:
- **Identical output** - Pixel-perfect SVG matching
- **Same features** - All parameters and themes supported
- **Better error handling** - Graceful fallbacks for edge cases
- **Vercel deployment** - Easy serverless hosting

## 📝 License

MIT License - Feel free to use this in your projects!

## 🤝 Contributing

Issues and PRs welcome! This project aims to maintain 100% compatibility with the original GitHub README Stats.

---

⭐ **Star this repo if you find it useful!** ⭐
