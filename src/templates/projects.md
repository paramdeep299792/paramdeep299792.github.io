# Projects

## On-going Projects

{% for proj in ongoing_projects %}
### {{ proj.title }} ({{ proj.type }})
*{{ proj.year }} | {{ proj.location }}*  
{% for highlight in proj.highlights %}  
- {{ highlight.replace('\\&', '&') }}  
{% endfor %}

{% endfor %}
---

## Past Projects

{% for proj in projects %}
### {{ proj.title }} ({{ proj.type }})
*{{ proj.year }} | {{ proj.location }}*  
{% for highlight in proj.highlights %}  
- {{ highlight.replace('\\&', '&') }}  
{% endfor %}

{% endfor %}