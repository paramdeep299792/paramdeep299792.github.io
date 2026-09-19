# Awards & Activities

## Awards and Recognition

{% for award in awards %}
- **{{ award.title }} ({{ award.year }})**  
  *{{ award.location | default('N/A') }}  
  *{{ award.description.replace('\\&', '&') }}

{% endfor %}
---

## Extracurricular and Volunteering Activities

{% for extra in extracurricular %}
- **{{ extra.title }} ({{ extra.year }})**  
  *{{ extra.location }}  
  *{{ extra.description.replace('\\&', '&') }}  
  {% if extra.attachments %}
  **Attachments:**<br>
  {% for attachment in extra.attachments %}
    {% if attachment.type == 'image' and attachment.inline %}
    📎 <b>{{ attachment.name }}</b><br>
    <img src="/{{ attachment.path }}" alt="{{ attachment.name }}" class="attachment-img"><br><br>
    {% else %}
    📎 [{{ attachment.name }}]({{ attachment.path }})<br>
    {% endif %}
  {% endfor %}
  {% else %}
  **Attachments:** None
  {% endif %}

{% endfor %}