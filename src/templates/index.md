# {{ basics.name }}

- [{{ basics.email }}](mailto:{{ basics.email }})
- [{{ basics.linkedin.split('https://')[1] }}]({{ basics.linkedin }})
- [{{ basics.github.split('https://')[1] }}]({{ basics.github }})

---

## Technical & Research Skills

{% for category, tools in skills.items() %}
- **{{ category.replace('\\&', '&') }}:** {{ tools }} 
{% endfor %}

