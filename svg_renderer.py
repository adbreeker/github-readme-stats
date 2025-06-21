"""
SVG Card Renderer for GitHub Stats
Handles the creation of SVG cards for both stats and top languages
Matches the structure and styling of the original JavaScript implementation
"""

from typing import Dict, List, Optional, Tuple
import math
import html

class Card:
    """Base class for SVG card generation matching original Card.js structure"""
    
    def __init__(self, width: int = 100, height: int = 100, border_radius: float = 4.5,
                 colors: Dict[str, str] = None, custom_title: str = None,
                 default_title: str = "", title_prefix_icon: str = ""):
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.colors = colors or {}
        self.title = html.escape(custom_title if custom_title is not None else default_title)
        
        self.hide_border = False
        self.hide_title = False
        self.css = ""
        self.padding_x = 25
        self.padding_y = 35
        self.title_prefix_icon = title_prefix_icon
        self.animations = True
        self.a11y_title = ""
        self.a11y_desc = ""
    
    def disable_animations(self):
        """Disable animations"""
        self.animations = False
    
    def set_accessibility_label(self, title: str, desc: str):
        """Set accessibility labels"""
        self.a11y_title = title
        self.a11y_desc = desc
    
    def set_css(self, css: str):
        """Set custom CSS"""
        self.css = css
    
    def set_hide_border(self, hide: bool):
        """Hide or show border"""
        self.hide_border = hide
    
    def set_hide_title(self, hide: bool):
        """Hide or show title"""
        self.hide_title = hide
        if hide:
            self.height -= 30
    
    def get_animations(self) -> str:
        """Get animation CSS"""
        return """
          @keyframes scaleInAnimation {
            from {
              transform: translate(-5px, 5px) scale(0);
            }
            to {
              transform: translate(-5px, 5px) scale(1);
            }
          }
          @keyframes fadeInAnimation {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
        """
    
    def render_gradient(self) -> str:
        """Render gradient if background is array/object"""
        if isinstance(self.colors.get('bgColor'), str) and not self.colors.get('bgColor', '').startswith('#'):
            # Simple gradient for now
            return f"""
            <defs>
              <linearGradient id="gradient" gradientTransform="rotate(45)">
                <stop offset="0%" stop-color="#{self.colors.get('bgColor', 'fffefe')}" />
                <stop offset="100%" stop-color="#{self.colors.get('bgColor', 'fffefe')}" />
              </linearGradient>
            </defs>
            """
        return ""
    
    def render_title(self) -> str:
        """Render card title"""
        if not self.title:
            return ""
        
        return f"""
        <g data-testid="card-title" transform="translate({self.padding_x}, {self.padding_y})">
          {self.title_prefix_icon}
          <text x="0" y="0" class="header" data-testid="header">{self.title}</text>
        </g>        """
    
    def render(self, body: str) -> str:
        """Render complete SVG card"""
        bg_fill = self.colors.get('bgColor', '#fffefe')
        if isinstance(self.colors.get('bgColor'), str) and 'gradient' in str(bg_fill):
            bg_fill = "url(#gradient)"
        
        animations_css = "" if not self.animations else self.get_animations()
        animation_disable = "* { animation-duration: 0s !important; animation-delay: 0s !important; }" if not self.animations else ""
        
        return f"""
      <svg
        width="{self.width}"
        height="{self.height}"
        viewBox="0 0 {self.width} {self.height}"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-labelledby="descId"
      >
        <title id="titleId">{self.a11y_title}</title>
        <desc id="descId">{self.a11y_desc}</desc>
        <style>
          .header {{
            font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
            fill: {self.colors.get('titleColor', '#2f80ed')};
            animation: fadeInAnimation 0.8s ease-in-out forwards;
          }}
          @supports(-moz-appearance: auto) {{
            /* Selector detects Firefox */
            .header {{ font-size: 15.5px; }}
          }}
          {self.css}

          {animations_css}
          {animation_disable}
        </style>

        {self.render_gradient()}

        <rect
          data-testid="card-bg"
          x="0.5"
          y="0.5"
          rx="{self.border_radius}"
          height="99%"
          stroke="{self.colors.get('borderColor', '#e4e2e2')}"
          width="{self.width - 1}"
          fill="{bg_fill}"
          stroke-opacity="{0 if self.hide_border else 1}"
        />

        {'' if self.hide_title else self.render_title()}

        <g
          data-testid="main-card-body"
          transform="translate(0, {self.padding_x if self.hide_title else self.padding_y + 20})"
        >
          {body}
        </g>
      </svg>
    """

def k_formatter(num: int) -> str:
    """Format numbers with k, M notation like the original"""
    if abs(num) >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif abs(num) >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

def create_text_node(icon: str, label: str, value: int, id: str, index: int, 
                    show_icons: bool = False, shift_value_pos: int = 0, 
                    bold: bool = True, number_format: str = "short") -> str:
    """Create stat text node matching original createTextNode function"""
    k_value = value if number_format.lower() == "long" else k_formatter(value)
    stagger_delay = (index + 3) * 150
    
    # In the original: labelOffset = showIcons ? `x="25"` : "";
    # But this is applied WITHIN the transform group that already has translate(25, 0)
    label_offset = 'x="25"' if show_icons else ""
    
    icon_svg = f"""
    <svg data-testid="icon" class="icon" viewBox="0 0 16 16" version="1.1" width="16" height="16">
      {icon}
    </svg>
  """ if show_icons else ""
    
    bold_class = "bold" if bold else "not_bold"
    # Original: x="${(showIcons ? 140 : 120) + shiftValuePos}"
    value_x = (140 if show_icons else 120) + shift_value_pos
    
    return f"""
    <g class="stagger" style="animation-delay: {stagger_delay}ms" transform="translate(25, 0)">
      {icon_svg}
      <text class="stat {bold_class}" {label_offset} y="12.5">{label}:</text>
      <text
        class="stat {bold_class}"
        x="{value_x}"
        y="12.5"
        data-testid="{id}"
      >{k_value}</text>
    </g>
  """

def create_progress_node(x: int, y: int, color: str, width: int, progress: float,
                        progress_bar_bg_color: str = "#ddd", delay: int = 0) -> str:
    """Create progress bar node"""
    progress_width = (width * progress / 100)
    
    return f"""
    <g transform="translate({x}, {y})">
      <rect 
        rx="5" ry="5" x="0" y="0" 
        width="{width}" height="8" 
        fill="{progress_bar_bg_color}"
      ></rect>
      <rect 
        height="8" fill="{color}" rx="5" ry="5" x="0" y="0" 
        data-testid="lang-progress" 
        width="{progress_width}"
        class="lang-progress"
        style="animation-delay: {delay}ms"
      ></rect>
    </g>
    """

def create_progress_text_node(width: int, color: str, name: str, progress: float, index: int) -> str:
    """Create progress text node for languages"""
    stagger_delay = (index + 3) * 150
    padding_right = 95
    progress_text_x = width - padding_right + 10
    progress_width = width - padding_right
    
    return f"""
    <g class="stagger" style="animation-delay: {stagger_delay}ms">
      <text data-testid="lang-name" x="2" y="15" class="lang-name">{html.escape(name)}</text>
      <text x="{progress_text_x}" y="34" class="lang-name">{progress:.1f}%</text>
      {create_progress_node(0, 25, color, progress_width, progress, delay=stagger_delay + 300)}
    </g>
    """

def create_compact_lang_node(lang: Dict, total_size: int, hide_progress: bool, index: int) -> str:
    """Create compact language node"""
    percentage = (lang['size'] / total_size * 100) if total_size > 0 else 0
    stagger_delay = (index + 3) * 150
    color = lang.get('color', '#858585')
    
    progress_text = "" if hide_progress else f" {percentage:.1f}%"
    
    return f"""
    <g class="stagger" style="animation-delay: {stagger_delay}ms">
      <circle cx="5" cy="6" r="5" fill="{color}" />
      <text data-testid="lang-name" x="15" y="10" class="lang-name">
        {html.escape(lang['name'])}{progress_text}
      </text>
    </g>
    """

def flex_layout(items: List[str], gap: int, direction: str = "row") -> List[str]:
    """Flex layout utility matching original flexLayout function"""
    last_size = 0
    result = []
    
    for item in filter(None, items):  # Filter out empty strings
        if direction == "column":
            transform = f"translate(0, {last_size})"
        else:
            transform = f"translate({last_size}, 0)"
        
        result.append(f'<g transform="{transform}">{item}</g>')
        last_size += gap
    
    return result

class StatsCard:
    """SVG card for displaying GitHub statistics matching original stats-card.js"""
    
    def __init__(self, stats, **kwargs):
        # Extract Card parameters
        self.stats = stats
        self.hide = kwargs.get('hide', [])
        self.show_icons = kwargs.get('show_icons', False)
        self.include_all_commits = kwargs.get('include_all_commits', False)
        self.line_height = kwargs.get('line_height', 25)
        self.number_format = kwargs.get('number_format', 'short')
        self.bold = kwargs.get('text_bold', True)
        self.hide_rank = kwargs.get('hide_rank', False)
          # Calculate card dimensions using original constants
        visible_stats = self._count_visible_stats()
        height = max(150, 45 + (visible_stats + 1) * self.line_height)
        
        # Original width calculation logic
        icon_width = 16 + 1 if self.show_icons and visible_stats else 0  # 16px icon + 1px padding
        
        if self.hide_rank:
            # CARD_MIN_WIDTH = 287, CARD_DEFAULT_WIDTH = 287
            default_width = 287 + icon_width
        else:
            # RANK_CARD_DEFAULT_WIDTH = 450
            default_width = 450 + icon_width
            
        width = kwargs.get('width', default_width)
        
        # Setup colors for StatsCard
        colors = {
            'titleColor': f"#{kwargs.get('title_color', '2f80ed')}",
            'textColor': f"#{kwargs.get('text_color', '434d58')}",
            'iconColor': f"#{kwargs.get('icon_color', '4c71f2')}",
            'bgColor': f"#{kwargs.get('bg_color', 'fffefe')}",
            'borderColor': f"#{kwargs.get('border_color', 'e4e2e2')}",
        }
        
        # Create Card instance
        self.card = Card(
            width=width,
            height=height,
            border_radius=kwargs.get('border_radius', 4.5),
            colors=colors,
            custom_title=kwargs.get('custom_title'),
            default_title=f"{stats.name}'s GitHub Stats"
        )
        
        self.card.set_hide_border(kwargs.get('hide_border', False))
        self.card.set_hide_title(kwargs.get('hide_title', False))
        
        # Set CSS styles matching original
        self.card.set_css(self._get_styles(colors))
        
        if kwargs.get('disable_animations', False):
            self.card.disable_animations()
    
    def _count_visible_stats(self) -> int:
        """Count how many stats will be visible"""
        all_stats = ['stars', 'commits', 'prs', 'issues', 'contribs']
        return len([stat for stat in all_stats if stat not in self.hide])
    
    def _get_styles(self, colors: Dict[str, str]) -> str:
        """Get CSS styles matching original stats card"""
        return f"""
        .stat {{
          font: 600 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; 
          fill: {colors['textColor']};
        }}
        @supports(-moz-appearance: auto) {{
          /* Selector detects Firefox */
          .stat {{ font-size:12px; }}
        }}
        .stagger {{
          opacity: 0;
          animation: fadeInAnimation 0.3s ease-in-out forwards;
        }}
        .rank-text {{
          font: 800 24px 'Segoe UI', Ubuntu, Sans-Serif; 
          fill: {colors['textColor']};
          animation: scaleInAnimation 0.3s ease-in-out forwards;
        }}
        .rank-percentile-header {{
          font-size: 14px;
        }}
        .rank-percentile-text {{
          font-size: 16px;
        }}
        .not_bold {{ font-weight: 400 }}
        .bold {{ font-weight: 700 }}
        .icon {{
          fill: {colors['iconColor']};
          display: {'block' if self.show_icons else 'none'};
        }}
        .rank-circle-rim {{
          stroke: {colors['titleColor']};
          fill: none;
          stroke-width: 6;
          opacity: 0.2;
        }}
        .rank-circle {{
          stroke: {colors['titleColor']};
          stroke-dasharray: 250;
          fill: none;
          stroke-width: 6;
          stroke-linecap: round;
          opacity: 0.8;
          transform-origin: -10px 8px;
          transform: rotate(-90deg);
          animation: rankAnimation 1s forwards ease-in-out;
        }}
        .lang-progress {{
          animation: scaleXInAnimation 0.3s ease-in-out forwards;
        }}
        @keyframes rankAnimation {{
          from {{
            stroke-dashoffset: 250;
          }}
          to {{
            stroke-dashoffset: 50;
          }}
        }}
        @keyframes scaleXInAnimation {{
          0% {{
            transform: scaleX(0);
          }}
          100% {{
            transform: scaleX(1);
          }}
        }}
        """
    
    def _create_stats_content(self) -> str:
        """Create all stat items matching original structure"""
        from github_stats import ICONS
        
        # Define stats in order matching original STATS object
        stat_configs = [
            ('stars', 'Total Stars', self.stats.total_stars, ICONS['star']),
            ('commits', f'Total Commits{" (2025)" if not self.include_all_commits else ""}', 
             self.stats.total_commits, ICONS['commits']),
            ('prs', 'Total PRs', self.stats.total_prs, ICONS['prs']),
            ('issues', 'Total Issues', self.stats.total_issues, ICONS['issues']),
            ('contribs', 'Contributed to', self.stats.contributed_to, ICONS['contribs']),
        ]
          # Filter and create stat items
        stat_items = []
        index = 0
        
        # From original: shiftValuePos: 79.01 + (isLongLocale ? 50 : 0)
        # For now, let's use 79.01 (could be made locale-aware later)
        shift_value_pos = 79.01
        
        for stat_key, label, value, icon in stat_configs:
            if stat_key not in self.hide:
                stat_items.append(create_text_node(
                    icon=icon,
                    label=label,
                    value=value,
                    id=stat_key,
                    index=index,
                    show_icons=self.show_icons,
                    shift_value_pos=shift_value_pos,
                    bold=self.bold,
                    number_format=self.number_format
                ))
                index += 1        
        # Use flex layout like original
        return '\n'.join(flex_layout(stat_items, self.line_height, "column"))
    
    def _create_rank_circle(self) -> str:
        """Create rank circle matching original implementation"""
        if self.hide_rank:
            return ""
            
        # Calculate rank circle position
        rank_x_translation = self._calculate_rank_x_translation()
        rank_y = self.card.height // 2 - 50
        
        # Get rank info from stats
        rank_level = getattr(self.stats, 'rank_level', 'A+')
        percentile = getattr(self.stats, 'percentile', 95)
        
        # Create rank circle matching original JS positioning
        return f"""
        <g data-testid="rank-circle" transform="translate({rank_x_translation}, {rank_y})">
          <circle class="rank-circle-rim" cx="-10" cy="8" r="40" />
          <circle class="rank-circle" cx="-10" cy="8" r="40" />
          <g class="rank-text">
            <text x="-5" y="3" alignment-baseline="central" dominant-baseline="central" text-anchor="middle" data-testid="level-rank-icon">
              {rank_level}
            </text>
          </g>
        </g>
        """
    
    def _calculate_rank_x_translation(self) -> int:
        """Calculate rank circle X translation matching original logic"""
        # Original constants
        RANK_CARD_MIN_WIDTH = 420
        RANK_CARD_DEFAULT_WIDTH = 450
        
        icon_width = 16 + 1 if self.show_icons else 0  # 16px icon + 1px padding
        visible_stats = self._count_visible_stats()
        
        if visible_stats:
            min_x_translation = RANK_CARD_MIN_WIDTH + icon_width - 70
            if self.card.width > RANK_CARD_DEFAULT_WIDTH:
                x_max_expansion = min_x_translation + (450 - (RANK_CARD_MIN_WIDTH + icon_width)) // 2
                return x_max_expansion + self.card.width - RANK_CARD_DEFAULT_WIDTH
            else:
                min_card_width = RANK_CARD_MIN_WIDTH + icon_width
                return min_x_translation + (self.card.width - min_card_width) // 2
        else:
            return self.card.width // 2 + 20 - 10
    
    def render(self) -> str:
        """Render the stats card"""
        # Set accessibility labels
        labels = []
        stat_configs = [
            ('stars', 'Total Stars', self.stats.total_stars),
            ('commits', 'Total Commits', self.stats.total_commits),
            ('prs', 'Total PRs', self.stats.total_prs),
            ('issues', 'Total Issues', self.stats.total_issues),
            ('contribs', 'Contributed to', self.stats.contributed_to),
        ]
        
        for stat_key, label, value in stat_configs:
            if stat_key not in self.hide:
                labels.append(f"{label}: {value}")
        
        self.card.set_accessibility_label(
            title=f"{self.card.title}, Rank: A+",
            desc=", ".join(labels)
        )
          # Create main content
        body = f"""
        {self._create_rank_circle()}
        <svg x="0" y="0">
          {self._create_stats_content()}
        </svg>
        """
        
        return self.card.render(body)

class TopLanguagesCard:
    """SVG card for displaying top programming languages matching original top-languages-card.js"""
    
    def __init__(self, languages: List[Dict], **kwargs):
        self.languages = languages
        self.layout = kwargs.get('layout', 'normal')
        self.hide = kwargs.get('hide', [])
        self.hide_progress = kwargs.get('hide_progress', False)
        self.langs_count = kwargs.get('langs_count', 5)
        
        # Calculate dimensions
        if self.layout == 'compact':
            height = 200
        else:
            filtered_langs = self._filter_languages()
            height = max(200, 90 + len(filtered_langs) * 40)
        
        width = kwargs.get('width', 300)
          # Setup colors for TopLanguagesCard
        colors = {
            'titleColor': f"#{kwargs.get('title_color', '2f80ed')}",
            'textColor': f"#{kwargs.get('text_color', '434d58')}",
            'iconColor': f"#{kwargs.get('icon_color', '4c71f2')}",
            'bgColor': f"#{kwargs.get('bg_color', 'fffefe')}",
            'borderColor': f"#{kwargs.get('border_color', 'e4e2e2')}",
        }
        
        # Create Card instance
        self.card = Card(
            width=width,
            height=height,
            border_radius=kwargs.get('border_radius', 4.5),
            colors=colors,
            custom_title=kwargs.get('custom_title'),
            default_title="Most Used Languages"
        )
        
        self.card.set_hide_border(kwargs.get('hide_border', False))
        self.card.set_hide_title(kwargs.get('hide_title', False))
        
        # Set CSS styles
        self.card.set_css(self._get_styles(colors))
        
        if kwargs.get('disable_animations', False):
            self.card.disable_animations()
    
    def _get_styles(self, colors: Dict[str, str]) -> str:
        """Get CSS styles matching original top languages card"""
        return f"""        .lang-name {{
          font: 400 11px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif;
          fill: {colors['textColor']};
        }}
        .stagger {{
          opacity: 0;
          animation: fadeInAnimation 0.3s ease-in-out forwards;
        }}
        .lang-progress {{
          animation: scaleXInAnimation 0.3s ease-in-out forwards;
        }}
        @keyframes scaleXInAnimation {{
          0% {{
            transform: scaleX(0);
          }}
          100% {{
            transform: scaleX(1);
          }}
        }}
        """
    
    def _filter_languages(self) -> List[Dict]:
        """Filter and calculate percentages for languages"""
        # Filter out hidden languages
        filtered_langs = [
            lang for lang in self.languages 
            if lang['name'].lower() not in [h.lower() for h in self.hide]
        ]
        
        if not filtered_langs:
            return []
        
        # Sort by size and take top langs_count
        filtered_langs.sort(key=lambda x: x['size'], reverse=True)
        filtered_langs = filtered_langs[:self.langs_count]
        
        # Calculate total size for percentages
        total_size = sum(lang['size'] for lang in filtered_langs)
        
        # Add percentage to each language
        for lang in filtered_langs:
            lang['percentage'] = (lang['size'] / total_size * 100) if total_size > 0 else 0
        
        return filtered_langs
    
    def _create_normal_layout(self, languages: List[Dict]) -> str:
        """Create normal layout matching original createProgressTextNode"""
        if not languages:
            return '<text x="50%" y="50%" text-anchor="middle" class="lang-name">No languages found</text>'
        
        items = []
        for i, lang in enumerate(languages):
            items.append(create_progress_text_node(
                width=self.card.width,
                color=lang.get('color', '#858585'),
                name=lang['name'],
                progress=lang['percentage'],
                index=i
            ))
        
        return '\n'.join(flex_layout(items, 40, "column"))
    
    def _create_compact_layout(self, languages: List[Dict]) -> str:
        """Create compact layout matching original createCompactLangNode"""
        if not languages:
            return '<text x="50%" y="50%" text-anchor="middle" class="lang-name">No languages found</text>'
        
        total_size = sum(lang['size'] for lang in languages)
        items = []
        
        for i, lang in enumerate(languages):
            items.append(create_compact_lang_node(
                lang=lang,
                total_size=total_size,
                hide_progress=self.hide_progress,
                index=i
            ))
        
        # Split into columns like original
        mid_point = len(items) // 2
        left_column = items[:mid_point] if items else []
        right_column = items[mid_point:] if items else []
        
        left_layout = '\n'.join(flex_layout(left_column, 25, "column"))
        right_layout = '\n'.join(flex_layout(right_column, 25, "column"))        
        columns = [left_layout, right_layout] if right_layout else [left_layout]
        return '\n'.join(flex_layout(columns, 150, "row"))
    
    def _create_languages_content(self) -> str:
        """Create language content based on layout"""
        languages = self._filter_languages()
        
        if self.layout == 'compact':
            return self._create_compact_layout(languages)
        else:
            return self._create_normal_layout(languages)
    
    def render(self) -> str:
        """Render the top languages card"""
        languages = self._filter_languages()
        
        # Set accessibility labels
        lang_names = [lang['name'] for lang in languages[:5]]
        self.card.set_accessibility_label(
            title=self.card.title,
            desc=f"Most used languages: {', '.join(lang_names)}"
        )
        
        # Create main content with CARD_PADDING (25px) left margin like original
        body = f"""
        <svg data-testid="lang-items" x="25">
          {self._create_languages_content()}
        </svg>
        """
        
        return self.card.render(body)

# Utility functions for card creation
def create_stats_card(stats, options: Dict) -> str:
    """Create a GitHub stats card"""
    # Apply theme if specified
    theme_name = options.get('theme', 'default')
    from github_stats import THEMES
    
    if theme_name in THEMES:
        theme = THEMES[theme_name]
        for key, value in theme.items():
            if key not in options or options[key] is None:
                options[key] = value
    
    card = StatsCard(stats, **options)
    return card.render()

def create_top_languages_card(languages: List[Dict], options: Dict) -> str:
    """Create a top languages card"""
    # Apply theme if specified
    theme_name = options.get('theme', 'default')
    from github_stats import THEMES
    
    if theme_name in THEMES:
        theme = THEMES[theme_name]
        for key, value in theme.items():
            if key not in options or options[key] is None:
                options[key] = value
    
    card = TopLanguagesCard(languages, **options)
    return card.render()
