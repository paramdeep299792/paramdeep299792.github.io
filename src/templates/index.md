# {{ basics.name }}

- [<u>{{ basics.o_email }}</u>](mailto:{{ basics.o_email }})
- [<u>{{ basics.email }}</u>](mailto:{{ basics.email }})
- s.[<u>paramdeep299792.me</u>]({{ basics.website}}), ∀s ∈ {[<u>linkedin</u>]({{ basics.linkedin }}), [<u>github</u>]({{ basics.github }})}

---

## Technical & Research Skills

{% for category, tools in skills.items() %}
- **{{ category.replace('\\&', '&') }}:** {{ tools }} 
{% endfor %}

