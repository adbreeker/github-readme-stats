from github_contributions import generate_text_pattern

patterns = generate_text_pattern('ADBREEKER')
print('Letter positions and patterns:')
print()

for pos, pattern in sorted(patterns.items()):
    print(f'Starting at column {pos}:')
    for row in pattern:
        print('  ' + ''.join(['█' if x else ' ' for x in row]))
    print()

print(f'Total width needed: {max(patterns.keys()) + 4} columns')
