# Experience & Education

## Work Experience

{% for job in experience %}
### [{{ job.company }}]({{ job.company_url }})
**{{ job.title }}** | *{{ job.dates }}*  
*{{ job.location }}*
{% for highlight in job.highlights %}
- {{ highlight.replace('\\&', '&') }}
{% endfor %}

{% endfor %}
---

## Education

{% for edu in education %}
### {{ edu.institution }}
**{{ edu.degree.replace('\\%', '%') }}** | *{{ edu.dates }}*  
*{{ edu.location }}*

{% endfor %}