"""
Debug script to understand the animation timing calculations
"""

def debug_animation_timing():
    # Simulate a grid with 53 columns (typical contributions grid)
    total_columns = 53
    middle_column = total_columns // 2  # This would be 26
    
    print(f"Total columns: {total_columns}")
    print(f"Middle column: {middle_column}")
    print()
    
    # Test first few columns (left line territory)
    print("LEFT LINE TERRITORY:")
    for week_idx in range(min(5, middle_column)):
        if week_idx < middle_column:
            eat_progress = week_idx / (middle_column - 1) if middle_column > 1 else 0
            eat_time = eat_progress * 25  # Updated formula
            print(f"Column {week_idx}: eat_progress={eat_progress:.3f}, eat_time={eat_time:.1f}")
    
    print(f"MIDDLE COLUMN: {middle_column} - eat_time=25.0, restore_time=100.0")
    print()
    
    # Test last few columns (right line territory)
    print("RIGHT LINE TERRITORY:")
    for week_idx in range(max(total_columns - 5, middle_column + 1), total_columns):
        if week_idx > middle_column:
            columns_from_right = total_columns - 1 - week_idx
            max_columns_right = total_columns - middle_column - 1
            if max_columns_right > 0:
                eat_progress = columns_from_right / (max_columns_right - 1) if max_columns_right > 1 else 0
            else:
                eat_progress = 0
            eat_time = eat_progress * 25  # Updated formula
            print(f"Column {week_idx}: columns_from_right={columns_from_right}, max_columns_right={max_columns_right}, eat_progress={eat_progress:.3f}, eat_time={eat_time:.1f}")

if __name__ == "__main__":
    debug_animation_timing()
