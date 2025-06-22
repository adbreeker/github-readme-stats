"""
GitHub Contributions Calendar Logic Demo
Demonstrates how the contributions calendar positioning works with current date
"""

from datetime import datetime, timedelta, timezone
from github_contributions import get_contributions_year_range

def demo_calendar_logic():
    """Demonstrate the calendar logic and current date positioning"""
    
    print("📅 GitHub Contributions Calendar Logic Demo")
    print("=" * 50)
    
    # Get current date info
    today = datetime.now(timezone.utc).date()
    print(f"Today: {today.strftime('%A, %B %d, %Y')}")
    
    # Calculate current Sunday
    days_since_sunday = (today.weekday() + 1) % 7
    current_sunday = today - timedelta(days=days_since_sunday)
    print(f"Current Sunday: {current_sunday.strftime('%A, %B %d, %Y')}")
    
    # Get the contributions year range
    start_date, end_date = get_contributions_year_range()
    print(f"Contributions period: {start_date.date()} to {end_date.date()}")
    
    # Calculate weeks
    total_days = (end_date.date() - start_date.date()).days + 1
    total_weeks = total_days / 7
    print(f"Total days: {total_days}")
    print(f"Total weeks: {total_weeks:.1f}")
    
    print("\n🗓️  Week Structure:")
    print("   GitHub contributions calendar always starts on Sunday")
    print("   Shows exactly 53 weeks (371 days)")
    print("   Current week is the rightmost column")
    
    # Show current week position
    days_from_start = (today - start_date.date()).days
    current_week = days_from_start // 7
    current_weekday = days_from_start % 7
    
    weekday_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    print(f"\n📍 Current Position:")
    print(f"   Week: {current_week + 1}/53")
    print(f"   Day: {weekday_names[current_weekday]}")
    print(f"   If today is Sunday, there should be 1 square in the last column")
    print(f"   If today is Saturday, there should be 7 squares in the last column")
    
    # Show some key dates in the grid
    print(f"\n🔍 Key Dates in Grid:")
    
    # First Sunday
    first_sunday = start_date.date()
    print(f"   First square (top-left): {first_sunday.strftime('%A, %B %d, %Y')}")
    
    # Last Saturday of grid
    last_saturday = start_date.date() + timedelta(days=370)  # 53 weeks * 7 days - 1
    print(f"   Last possible square (bottom-right): {last_saturday.strftime('%A, %B %d, %Y')}")
    
    # Today's position
    if today >= first_sunday and today <= last_saturday:
        print(f"   Today's square: Week {current_week + 1}, {weekday_names[current_weekday]}")
    else:
        print(f"   Today is outside the grid range")

if __name__ == "__main__":
    demo_calendar_logic()
