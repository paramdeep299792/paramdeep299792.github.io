# {{ basics.name }}

- [{{ basics.o_email }}](mailto:{{ basics.o_email }})
- [{{ basics.email }}](mailto:{{ basics.email }})
- *s*.paramdeep299792.me, ∀ *s* ∈ {[linkedin]({{ basics.linkedin }}), [github]({{ basics.github }}), [x]({{ basics.x }}), [instagram]({{ basics.instagram }}), [orcid]({{ basics.orcid }})}

---

## Technical & Research Skills

{% for category, tools in skills.items() %}
- **{{ category.replace('\\&', '&') }}:** {{ tools }} 
{% endfor %}

