from svg_renderer import create_stats_card
from github_stats import GitHubStats

# Create test stats
stats = GitHubStats(
    name='testuser',
    total_stars=1250,
    total_commits=3420,
    total_prs=156,
    total_issues=89,
    contributed_to=23,
    rank=3,
    rank_level='A+',
    percentile=95
)

# Generate card with rank circle
svg = create_stats_card(stats, {
    'show_icons': True,
    'theme': 'default',
    'hide_rank': False
})

# Write to file
with open('Tests/stats_with_rank.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print('Generated stats card with rank circle')
