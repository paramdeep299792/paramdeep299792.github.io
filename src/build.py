import json
import jinja2
from pathlib import Path

# Set up paths relative to this script
src_dir = Path(__file__).resolve().parent
root_dir = src_dir.parent
templates_dir = root_dir / 'templates'
docs_dir = root_dir / 'docs'

# Ensure the docs directory exists for MkDocs
docs_dir.mkdir(exist_ok=True)

# 1. Load the JSON data
with open(root_dir / 'params.json', 'r') as f:
    data = json.load(f)

# 2. Configure Jinja2 for Markdown (Using standard {{ }} and {% %} tags)
md_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_dir),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False
)

# 3. Define which templates map to which output files
pages = {
    'index.md': 'index.md',
    'experience.md': 'experience.md',
    'projects.md': 'projects.md',
    'achievements.md': 'achievements.md',
    'references.md': 'references.md'
}

# 4. Render each template and save it to the docs/ folder
for template_name, output_name in pages.items():
    template = md_jinja_env.get_template(template_name)
    rendered_md = template.render(data)
    
    output_path = docs_dir / output_name
    with open(output_path, 'w') as f:
        f.write(rendered_md)
        
    print(f"Generated: docs/{output_name}")

print("MkDocs Markdown generation complete!")