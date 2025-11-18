import re

with open('templates/new_proposal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines, 1):
    # Find if tags
    if_match = re.search(r'{%\s*if\s+', line)
    endif_match = re.search(r'{%\s*endif\s*%}', line)
    
    if if_match:
        stack.append((i, line.strip()[:100]))
    elif endif_match:
        if stack:
            stack.pop()
        else:
            print(f"Line {i}: Unmatched endif")

print(f"\nUnclosed if tags: {len(stack)}")
for line_num, text in stack:
    print(f"Line {line_num}: {text}")
