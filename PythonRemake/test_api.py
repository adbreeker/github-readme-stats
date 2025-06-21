"""
Test the API with real GitHub token
"""

import asyncio
from api_handlers import StatsAPIHandler

async def test_api():
    handler = StatsAPIHandler()
    try:
        # Test with a simple request
        svg, headers = await handler.handle_request('username=octocat')
        print('✅ API request successful!')
        print(f'Content-Type: {headers.get("Content-Type")}')
        print(f'SVG length: {len(svg)} characters')
        print('First 200 characters of SVG:')
        print(svg[:200] + '...')
        
        # Save the test result
        with open('Tests/octocat_stats.svg', 'w', encoding='utf-8') as f:
            f.write(svg)
        print('✅ Saved test result to Tests/octocat_stats.svg')
        
    except Exception as e:
        print(f'❌ API request failed: {e}')

if __name__ == "__main__":
    asyncio.run(test_api())
