"""
GitHub Stats API - Python Implementation
Recreates the functionality of the JavaScript version for generating
GitHub profile statistics and top languages cards as SVG images.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import os
import json
import re
import math
from datetime import datetime
import asyncio
import aiohttp
from urllib.parse import parse_qs
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
GITHUB_API_URL = "https://api.github.com/graphql"
CARD_MIN_WIDTH = 287
CARD_DEFAULT_WIDTH = 287
RANK_CARD_MIN_WIDTH = 420
RANK_CARD_DEFAULT_WIDTH = 450

# Default cache times (in seconds)
CARD_CACHE_SECONDS = 14400  # 4 hours
TOP_LANGS_CACHE_SECONDS = 14400  # 4 hours
ERROR_CACHE_SECONDS = 7200  # 2 hours

# Themes configuration
THEMES = {
    "default": {
        "title_color": "2f80ed",
        "icon_color": "4c71f2", 
        "text_color": "434d58",
        "bg_color": "fffefe",
        "border_color": "e4e2e2",
    },
    "dark": {
        "title_color": "fff",
        "icon_color": "79ff97",
        "text_color": "9f9f9f", 
        "bg_color": "151515",
    },
    "radical": {
        "title_color": "fe428e",
        "icon_color": "f8d847",
        "text_color": "a9fef7",
        "bg_color": "141321",
    },
    "merko": {
        "title_color": "abd200",
        "icon_color": "b7d364",
        "text_color": "68b587",
        "bg_color": "0a0f0b",
    },
    "gruvbox": {
        "title_color": "fabd2f",
        "icon_color": "fe8019",
        "text_color": "8ec07c",
        "bg_color": "282828",
    },
    "tokyonight": {
        "title_color": "70a5fd",
        "icon_color": "bf91f3",
        "text_color": "38bdae",
        "bg_color": "1a1b27",
    },
}

# SVG Icons
ICONS = {
    "star": """<path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>""",
    "commits": """<path d="M1.643 3.143L.427 1.927A.25.25 0 000 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 00.177-.427L2.715 4.215a6.5 6.5 0 11-1.18 4.458.75.75 0 10-1.493.154 8.001 8.001 0 101.6-5.684zM7.75 4a.75.75 0 01.75.75v2.992l2.028.812a.75.75 0 01-.557 1.392l-2.5-1A.75.75 0 017 8.25v-3.5A.75.75 0 017.75 4z"/>""",
    "prs": """<path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/>""",
    "issues": """<path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/><path d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>""",
    "contribs": """<path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>""",
}

@dataclass
@dataclass
class GitHubStats:
    """Data structure for GitHub user statistics"""
    name: str
    total_stars: int = 0
    total_commits: int = 0
    total_issues: int = 0
    total_prs: int = 0
    total_prs_merged: int = 0
    total_reviews: int = 0
    total_discussions_started: int = 0
    total_discussions_answered: int = 0
    contributed_to: int = 0
    rank: int = 0
    rank_level: str = "A+"
    percentile: float = 0.0

@dataclass 
class LanguageData:
    """Data structure for programming language statistics"""
    name: str
    color: str
    size: int

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    def __init__(self, message: str, error_type: str = "UNKNOWN"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class GitHubStatsAPI:
    """Main class for fetching GitHub statistics and generating SVG cards"""
    
    def __init__(self):
        self.tokens = self._get_github_tokens()
        self.current_token_index = 0
        
    def _get_github_tokens(self) -> List[str]:
        """Get GitHub tokens from environment variables"""
        tokens = []
        i = 1
        while True:
            token = os.getenv(f'PAT_{i}')
            if token:
                tokens.append(token)
                i += 1
            else:
                break
        
        if not tokens:
            raise GitHubAPIError("No GitHub API tokens found. Please set PAT_1 environment variable.", "NO_TOKENS")
        
        return tokens
    
    def _get_current_token(self) -> str:
        """Get current GitHub token with rotation for rate limiting"""
        if self.current_token_index >= len(self.tokens):
            self.current_token_index = 0
        
        token = self.tokens[self.current_token_index]
        return token
    
    def _rotate_token(self):
        """Rotate to next available token"""
        self.current_token_index = (self.current_token_index + 1) % len(self.tokens)
    
    async def _make_graphql_request(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make GraphQL request to GitHub API with token rotation"""
        max_retries = len(self.tokens)
        
        for attempt in range(max_retries):
            token = self._get_current_token()
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            
            payload = {
                'query': query,
                'variables': variables
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(GITHUB_API_URL, json=payload, headers=headers) as response:
                        data = await response.json()
                        
                        if response.status == 200 and 'data' in data:
                            return data
                        
                        # Check for rate limiting
                        if ('errors' in data and 
                            any(error.get('type') == 'RATE_LIMITED' for error in data['errors'])):
                            print(f"Rate limit hit on token {self.current_token_index + 1}, rotating...")
                            self._rotate_token()
                            continue
                        
                        # Other errors
                        if 'errors' in data:
                            error_msg = data['errors'][0].get('message', 'Unknown GraphQL error')
                            error_type = data['errors'][0].get('type', 'GRAPHQL_ERROR')
                            
                            if error_type == 'NOT_FOUND':
                                raise GitHubAPIError("User not found", "USER_NOT_FOUND")
                            
                            raise GitHubAPIError(error_msg, error_type)
                        
                        raise GitHubAPIError(f"HTTP {response.status}: {await response.text()}", "HTTP_ERROR")
                        
            except aiohttp.ClientError as e:
                if attempt == max_retries - 1:
                    raise GitHubAPIError(f"Network error: {str(e)}", "NETWORK_ERROR")
                continue
        
        raise GitHubAPIError("All tokens exhausted due to rate limiting", "MAX_RETRY")

# GraphQL Queries
STATS_QUERY = """
query userInfo($login: String!) {
  user(login: $login) {
    name
    login
    contributionsCollection {
      totalCommitContributions
      totalPullRequestReviewContributions
    }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
      totalCount
    }
    pullRequests(first: 1) {
      totalCount
    }
    mergedPullRequests: pullRequests(states: MERGED, first: 1) {
      totalCount
    }
    openIssues: issues(states: OPEN, first: 1) {
      totalCount
    }
    closedIssues: issues(states: CLOSED, first: 1) {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, orderBy: {direction: DESC, field: STARGAZERS}) {
      totalCount
      nodes {
        name
        stargazers {
          totalCount
        }
      }
    }
  }
}
"""

TOP_LANGS_QUERY = """
query userInfo($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              color
              name
            }
          }
        }
      }
    }
  }
}
"""

# Export the main classes and functions
__all__ = ['GitHubStatsAPI', 'GitHubStats', 'LanguageData', 'THEMES', 'ICONS']
