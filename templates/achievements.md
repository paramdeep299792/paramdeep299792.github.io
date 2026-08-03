# Awards & Activities

## Awards and Recognition

{% for award in awards %}
- **{{ award.title }} ({{ award.year }})**  
  {% if award.location %}*{{ award.location }}*{% endif %}  
  {{ award.description.replace('\\&', '&') }}

{% endfor %}
---

## Extracurricular and Volunteer

{% for extra in extracurricular %}
- **{{ extra.title }} ({{ extra.year }})**  
  {{ extra.description.replace('\\&', '&') }}

{% endfor %}