# {{ basics.name }}

- **Email:** [{{ basics.email }}](mailto:{{ basics.email }})
- **LinkedIn:** [{{ basics.linkedin.split('in/')[1].strip('/') }}]({{ basics.linkedin }})
- **GitHub:** [{{ basics.github.split('github.com/')[1].strip('/') }}]({{ basics.github }})

---

## Technical & Research Skills

{% for category, tools in skills.items() %}
- **{{ category.replace('\\&', '&') }}:** {{ tools }} 
{% endfor %}

