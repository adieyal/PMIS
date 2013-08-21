from django import template
from django.template.defaultfilters import stringfilter
from django.template import Template, Context
from django.conf import settings

register = template.Library()

@register.filter(is_safe=True)
@register.simple_tag(takes_context=True)
def department_project(context, index):
    
    template = Template("""
        {% load formatters %}
        <div class="department-projects department-projects-{{ index1 }}">
        <div class="project-brdr marg">
            <div class="border">
                <div class="project-main">
                    <div class="department-name client-{{ client.name|lower }}"><div>{{ client.fullname }}</div></div><!-- .project-name -->
                    <div class="total_projects">Total Projects: {{ client.total_projects }}</div><!-- .project-budget -->
                    <div class="in-planning"><div class="left">Currently in planning</div><span class="right">{{ client.projects.currently_in_planning }}</span></div><!-- .in-planning -->
                    <div class="in-planning"><div class="left"></div>In Implementation<span class="right">{{ client.projects.currently_in_implementation }}</span></div><!-- .in-planning -->
                    <div class="in-planning"><div class="left">Completed by FYE</div><span class="right">{{ client.projects.completed_in_fye}}</span></div><!-- .in-planning -->
                    <div class="in-planning"><div class="left">Practical Completion</div><span class="right">{{ client.projects.currently_in_practical_completion }}</span></div><!-- .in-planning -->
                    <div class="in-planning"><div class="left">Final Completion</div><span class="right">{{ client.projects.currently_in_final_completion }}</span></div><!-- .in-planning -->
                    <div class="donut-widget" data-widget="donut" data-src="{% url 'api:reports:district_graphs' district.id date.year date.month %}#client_projects_pie{{ index }}"></div>
                </div><!-- .project-main -->
            </div><!-- .border -->
        </div><!-- .project-brdr -->
        </div><!-- .department-projects-{{ index1 }} -->
    """)
    val = template.render(Context({
        "client" : context["clients"][index],
        "index" : index,
        "index1" : index + 1,
        "district" : context["district"],
        "date" : context["date"],
        "STATIC_URL" : settings.STATIC_URL
    }))

    return val
