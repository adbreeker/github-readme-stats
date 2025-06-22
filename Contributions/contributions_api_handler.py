"""
GitHub Contributions API Handler
API endpoint handler for generating GitHub contributions SVG
"""

import asyncio
from typing import Dict
from urllib.parse import parse_qs, unquote

from github_contributions import generate_contributions_svg

class ContributionsAPIHandler:
    """Handler for GitHub contributions API endpoint"""
    
    def _parse_query_params(self, query_string: str) -> Dict[str, str]:
        """Parse URL query parameters"""
        if not query_string:
            return {}
        
        parsed = parse_qs(query_string, keep_blank_values=True)
        # Convert lists to single values
        result = {}
        for key, values in parsed.items():
            if values:
                result[key] = unquote(values[0])
            else:
                result[key] = ""
        
        return result
    
    async def handle_request(self, query_string: str = "") -> Dict[str, any]:
        """Handle contributions API request"""
        try:
            # Parse query parameters
            params = self._parse_query_params(query_string)
            
            # Extract parameters
            username = params.get('username', '').strip()
            theme = params.get('theme', 'light').lower()
            
            # Validate required parameters
            if not username:
                return {
                    'status': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': {'error': 'Missing required parameter: username'}
                }
            
            # Validate theme
            if theme not in ['light', 'dark']:
                theme = 'light'
            
            # Generate SVG
            svg_content = await generate_contributions_svg(username, theme)
            
            # Return successful response
            return {
                'status': 200,
                'headers': {
                    'Content-Type': 'image/svg+xml',
                    'Cache-Control': 'public, max-age=14400',  # 4 hours cache
                },
                'body': svg_content
            }
            
        except Exception as e:
            # Return error response
            error_svg = f'''<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="100" fill="#f6f8fa" stroke="#d1d5da"/>
                <text x="200" y="40" text-anchor="middle" fill="#d73a49" 
                      font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                      font-size="14">Error generating contributions</text>
                <text x="200" y="60" text-anchor="middle" fill="#586069" 
                      font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" 
                      font-size="12">{str(e)[:50]}...</text>
            </svg>'''
            
            return {
                'status': 500,
                'headers': {'Content-Type': 'image/svg+xml'},
                'body': error_svg
            }

# Vercel handler function
async def handler(request):
    """Vercel handler for contributions endpoint"""
    contributions_handler = ContributionsAPIHandler()
    query_string = request.get('query', '')
    
    response = await contributions_handler.handle_request(query_string)
    
    return {
        'statusCode': response['status'],
        'headers': response['headers'],
        'body': response['body']
    }
