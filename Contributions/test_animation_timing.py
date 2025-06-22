"""
Test script to verify animation timing for first and last columns
"""

def test_animation_timing():
    """Test the animation timing calculation logic"""
    
    # Simulate grid with 53 weeks (0-52)
    total_columns = 53
    middle_column = total_columns // 2  # Should be 26
    
    print(f"Total columns: {total_columns}")
    print(f"Middle column: {middle_column}")
    print("\nTesting animation timing for each column:")
    print("Column | Territory | Eat Progress | Eat Time | Restore Time")
    print("-" * 60)
    
    for week_idx in range(total_columns):
        if week_idx <= middle_column:
            # Left line territory (columns 0 to middle_column inclusive)
            if middle_column > 0:
                eat_progress = week_idx / middle_column
            else:
                eat_progress = 0
            # Ensure eat_time is never 0 to avoid keyframe issues
            eat_time = max(0.1, eat_progress * 24.5)  # 0.1-24.5%
            restore_time = 75 + (1 - eat_progress) * 24.5  # 75.5-99.5%
            territory = "Left"
        else:
            # Right line territory (columns after middle_column)
            columns_from_right = total_columns - 1 - week_idx
            max_columns_right = total_columns - middle_column - 1
            if max_columns_right > 0:
                eat_progress = columns_from_right / max_columns_right
            else:
                eat_progress = 0
            # Ensure eat_time is never 0 to avoid keyframe issues
            eat_time = max(0.1, eat_progress * 24.5)  # 0.1-24.5%
            restore_time = 75 + (1 - eat_progress) * 24.5  # 75.5-99.5%
            territory = "Right"
        
        print(f"{week_idx:6d} | {territory:9s} | {eat_progress:11.3f} | {eat_time:8.1f} | {restore_time:12.1f}")
        
        # Highlight problematic columns
        if week_idx == 0 or week_idx == total_columns - 1:
            print(f"       ^ {'FIRST' if week_idx == 0 else 'LAST'} COLUMN")

if __name__ == "__main__":
    test_animation_timing()
