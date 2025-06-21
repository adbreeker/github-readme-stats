"""
GitHub Stats API Implementation
Main API handlers for stats and top languages endpoints
"""

import asyncio
import json
from typing import Dict, List, Optional
from urllib.parse import parse_qs, unquote
import os

from github_stats import GitHubStatsAPI, GitHubStats, LanguageData, GitHubAPIError, STATS_QUERY, TOP_LANGS_QUERY
from svg_renderer import create_stats_card, create_top_languages_card

class StatsAPIHandler:
    """Handler for GitHub stats API endpoint"""
    
    def __init__(self):
        self.api = GitHubStatsAPI()
    
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
    
    def _parse_boolean(self, value: str) -> bool:
        """Parse boolean from string"""
        if not value:
            return False
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _parse_array(self, value: str) -> List[str]:
        """Parse comma-separated array from string"""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]
    
    async def _fetch_user_stats(self, username: str) -> GitHubStats:
        """Fetch user statistics from GitHub API"""
        variables = {'login': username}
        
        try:
            response = await self.api._make_graphql_request(STATS_QUERY, variables)
            user_data = response['data']['user']
            
            if not user_data:
                raise GitHubAPIError("User not found", "USER_NOT_FOUND")
            
            # Calculate total stars
            total_stars = sum(repo['stargazers']['totalCount'] for repo in user_data['repositories']['nodes'])
            
            # Calculate total issues
            total_issues = user_data['openIssues']['totalCount'] + user_data['closedIssues']['totalCount']
            
            # Create stats object
            stats = GitHubStats(
                name=user_data['name'] or user_data['login'],
                total_stars=total_stars,
                total_commits=user_data['contributionsCollection']['totalCommitContributions'],
                total_issues=total_issues,
                total_prs=user_data['pullRequests']['totalCount'],
                total_prs_merged=user_data['mergedPullRequests']['totalCount'],
                total_reviews=user_data['contributionsCollection']['totalPullRequestReviewContributions'],
                contributed_to=user_data['repositoriesContributedTo']['totalCount'],
            )
            
            # Calculate rank (simplified version)
            score = (stats.total_stars * 4 + 
                    stats.total_commits + 
                    stats.total_prs * 3 + 
                    stats.total_issues + 
                    stats.total_reviews * 2)
              # Simple rank calculation (this could be more sophisticated)
            if score > 1000:
                stats.rank = 1  # S+
                stats.rank_level = "S+"
            elif score > 500:
                stats.rank = 2  # S
                stats.rank_level = "S"
            elif score > 200:
                stats.rank = 3  # A+
                stats.rank_level = "A+"
            elif score > 100:
                stats.rank = 4  # A
                stats.rank_level = "A"
            else:
                stats.rank = 5  # B+
                stats.rank_level = "B+"
            
            stats.percentile = max(0, min(100, 100 - (stats.rank - 1) * 20))
            
            return stats
            
        except GitHubAPIError:
            raise
        except Exception as e:
            raise GitHubAPIError(f"Failed to fetch user stats: {str(e)}", "FETCH_ERROR")
    
    async def handle_request(self, query_string: str) -> tuple[str, Dict[str, str]]:
        """Handle stats API request"""
        params = self._parse_query_params(query_string)
        
        # Required parameter
        username = params.get('username')
        if not username:
            return self._create_error_svg("Missing required parameter: username"), {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'max-age=300'
            }
        
        # Parse options
        options = {
            'width': int(params.get('card_width', 495)),
            'title': params.get('custom_title'),
            'title_color': params.get('title_color'),
            'text_color': params.get('text_color'),
            'icon_color': params.get('icon_color'),
            'bg_color': params.get('bg_color'),
            'border_color': params.get('border_color'),
            'theme': params.get('theme', 'default'),
            'hide_border': self._parse_boolean(params.get('hide_border')),
            'hide_title': self._parse_boolean(params.get('hide_title')),
            'show_icons': self._parse_boolean(params.get('show_icons')),
            'hide': self._parse_array(params.get('hide', '')),
            'border_radius': int(params.get('border_radius', 4)),
        }
        
        try:
            stats = await self._fetch_user_stats(username)
            svg_content = create_stats_card(stats, options)
            
            # Cache headers
            cache_seconds = int(os.getenv('CACHE_SECONDS', 14400))  # 4 hours default
            headers = {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': f'max-age={cache_seconds}, s-maxage={cache_seconds}',
            }
            
            return svg_content, headers
            
        except GitHubAPIError as e:
            error_svg = self._create_error_svg(e.message)
            return error_svg, {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'max-age=300'
            }
    
    def _create_error_svg(self, message: str) -> str:
        """Create an error SVG"""
        return f'''
        <svg width="495" height="120" viewBox="0 0 495 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
                .error-title {{ font: 600 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e74c3c; }}
                .error-text {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #586069; }}
            </style>
            <rect width="495" height="120" fill="#fffefe" stroke="#e4e2e2" stroke-width="1" rx="4"/>
            <text x="25" y="35" class="error-title">Something went wrong!</text>
            <text x="25" y="60" class="error-text">{message}</text>
        </svg>
        '''

class TopLanguagesAPIHandler:
    """Handler for top languages API endpoint"""
    
    def __init__(self):
        self.api = GitHubStatsAPI()
    
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
    
    def _parse_boolean(self, value: str) -> bool:
        """Parse boolean from string"""
        if not value:
            return False
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _parse_array(self, value: str) -> List[str]:
        """Parse comma-separated array from string"""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]
    
    async def _fetch_top_languages(self, username: str, hide_languages: List[str] = None) -> List[Dict]:
        """Fetch top languages from GitHub API"""
        variables = {'login': username}
        
        try:
            response = await self.api._make_graphql_request(TOP_LANGS_QUERY, variables)
            user_data = response['data']['user']
            
            if not user_data:
                raise GitHubAPIError("User not found", "USER_NOT_FOUND")
            
            # Aggregate languages
            language_stats = {}
            
            for repo in user_data['repositories']['nodes']:
                for edge in repo['languages']['edges']:
                    lang_name = edge['node']['name']
                    lang_color = edge['node']['color']
                    lang_size = edge['size']
                    
                    if lang_name in language_stats:
                        language_stats[lang_name]['size'] += lang_size
                    else:
                        language_stats[lang_name] = {
                            'name': lang_name,
                            'color': lang_color or '#858585',
                            'size': lang_size
                        }
            
            # Convert to list and sort by size
            languages = list(language_stats.values())
            languages.sort(key=lambda x: x['size'], reverse=True)
            
            # Filter out hidden languages
            if hide_languages:
                hide_lower = [lang.lower() for lang in hide_languages]
                languages = [lang for lang in languages if lang['name'].lower() not in hide_lower]
            
            return languages[:10]  # Return top 10
            
        except GitHubAPIError:
            raise
        except Exception as e:
            raise GitHubAPIError(f"Failed to fetch languages: {str(e)}", "FETCH_ERROR")
    
    async def handle_request(self, query_string: str) -> tuple[str, Dict[str, str]]:
        """Handle top languages API request"""
        params = self._parse_query_params(query_string)
        
        # Required parameter
        username = params.get('username')
        if not username:
            return self._create_error_svg("Missing required parameter: username"), {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'max-age=300'
            }
        
        # Parse options
        hide_languages = self._parse_array(params.get('hide', ''))
        
        options = {
            'width': int(params.get('card_width', 300)),
            'title': params.get('custom_title'),
            'title_color': params.get('title_color'),
            'text_color': params.get('text_color'),
            'bg_color': params.get('bg_color'),
            'border_color': params.get('border_color'),
            'theme': params.get('theme', 'default'),
            'layout': params.get('layout', 'normal'),
            'hide_border': self._parse_boolean(params.get('hide_border')),
            'hide_title': self._parse_boolean(params.get('hide_title')),
            'hide_progress': self._parse_boolean(params.get('hide_progress')),
            'hide': hide_languages,
            'border_radius': int(params.get('border_radius', 4)),
        }
        
        try:
            languages = await self._fetch_top_languages(username, hide_languages)
            svg_content = create_top_languages_card(languages, options)
            
            # Cache headers
            cache_seconds = int(os.getenv('CACHE_SECONDS', 14400))  # 4 hours default
            headers = {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': f'max-age={cache_seconds}, s-maxage={cache_seconds}',
            }
            
            return svg_content, headers
            
        except GitHubAPIError as e:
            error_svg = self._create_error_svg(e.message)
            return error_svg, {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'max-age=300'
            }
    
    def _create_error_svg(self, message: str) -> str:
        """Create an error SVG"""
        return f'''
        <svg width="300" height="120" viewBox="0 0 300 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
                .error-title {{ font: 600 16px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e74c3c; }}
                .error-text {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #586069; }}
            </style>
            <rect width="300" height="120" fill="#fffefe" stroke="#e4e2e2" stroke-width="1" rx="4"/>
            <text x="15" y="35" class="error-title">Something went wrong!</text>
            <text x="15" y="60" class="error-text">{message}</text>
        </svg>
        '''
