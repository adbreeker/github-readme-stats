from github_contributions import generate_text_pattern

patterns = generate_text_pattern('ADBREEKER')
print('Letter positions with proper spacing:')
print()

for pos in sorted(patterns.keys()):
    print(f'Column {pos}:')
    for row in patterns[pos]:
        print('  ' + ''.join(['█' if x else ' ' for x in row]))
    print()

print(f'Total width: {max(patterns.keys()) + 4} columns')
print()

# Show the letters in order
letters = "ADBREEKER"
positions = sorted(patterns.keys())
print("Letter spacing check:")
for i, pos in enumerate(positions):
    if i < len(letters):
        print(f"{letters[i]}: column {pos}")
    if i < len(positions) - 1:
        gap = positions[i+1] - pos - 4
        print(f"  -> gap of {gap} column(s) before next letter")
