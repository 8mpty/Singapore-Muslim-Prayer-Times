import re
import sys
from pathlib import Path

def update_readme(year, parent_link, readme_path=None):
    if readme_path is None:
        script_dir = Path(__file__).parent
        readme_path = script_dir.parent / 'README.md'
    
    readme_path = Path(readme_path)
    
    new_entry = f"""<details>
<summary>{year}</summary>

```
Muslim Prayer Timetable {year} ({year}) [Dataset]. data.gov.sg.
{parent_link}
```

</details>"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Found existing README.md at {readme_path}")
    except FileNotFoundError:
        print(f"README.md not found at {readme_path}, creating default...")
        content = """# Singapore-Muslim-Prayer-Times
    Timings for the prayer times for the muslims in Singapore

    # Citations & Sources 
    [Majlis Ugama Islam Singapura](https://www.muis.gov.sg/) 

    [data.gov.sg](https://data.gov.sg/)

    <p>
    </p>"""
    
    pattern = rf'<details>\s*\n\s*<summary>{year}</summary>.*?</details>\s*\n'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        print(f"Removed existing entry for year {year}")
    
    if '</p>' in content:
        content = content.replace('</p>', f'{new_entry}\n\n</p>')
        print(f"Added new entry for year {year}")
    else:
        content = content + f'\n{new_entry}\n'
        print(f"Added new entry for year {year} (no closing tag found)")
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully updated README.md with entry for {year}")
    print(f"README.md location: {readme_path.absolute()}")
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python readme-updater.py <year> <parent_link>")
        print("Example: python readme-updater.py 2026 https://data.gov.sg/datasets/d_xxx/view")
        sys.exit(1)
    
    year = sys.argv[1]
    parent_link = sys.argv[2]
    
    if not year.isdigit():
        print(f"Error: Year must be a number, got '{year}'")
        sys.exit(1)
    
    if not parent_link.startswith('http'):
        print(f"Error: Parent link must be a valid URL, got '{parent_link}'")
        sys.exit(1)
    
    try:
        update_readme(year, parent_link)
    except Exception as e:
        print(f"Error updating README: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()