# References

{% for ref in references %}
**{{ ref.name }}**  
*{{ ref.role }}* | {{ ref.location }}  
Contact: [{{ ref.contact }}](mailto:{{ ref.contact }})

{% endfor %}