from django import template
from django.template.defaultfilters import stringfilter
from django.template import Template, Context

register = template.Library()



@register.filter(is_safe=True)
@register.simple_tag(takes_context=True)
def worst_project(context, index):
    
    template = Template("""
        {% load formatters %}
        {% load perform_blocks %}
        <div class="client-worst-project-{{ index1 }} client-worst-project cf">
        	<div class="client-location cf">
            	<div class="client-worst-project-name client-{{ data.client|lower }}"><span class="worst-project-name">{{ data.name }}</span> (<a href="perform.html#">{{ data.client }}</a> | <a href="perform.html#">{{ data.municipality.name }}</a>)</div><!-- .location-main -->
                <div class="cap-image"></div><!-- .cap-image -->
                <div class="job-detail">Jobs created : {{ data.jobs|format_number }}</div><!-- .job-detail -->
            </div><!-- .client-location -->
            <div class="client-row cf">
            	<div class="client-main">
                	<div class="date-main-row cf">
                    	<div class="budget">Budget: <span>{{ data.budget|format_currency }}</span></div><!-- .budget-price -->
                    	<div class="start-date">Start: <span>{{ data.milestones.start_date|date:"N Y" }}</span></div><!-- .budget-price -->
                    	<div class="completion-date">Completion: <span>{{ data.milestones.practical_completion|date:"N Y" }}</span></div><!-- .budget-price -->
                    </div><!-- .date-main-row -->
                    <div class="actual-client-area cf">
                    	<div class="actual-client-row cf">
                        	<div class="actual-client-main cf">
                            	<div class="overall-progress">Overall Progress: {{ data.progress.actual|format_percentage }}</div><!-- .actual-price -->
                                <div class="worst-project-gauge worst-project-gauge{{ index1 }}" data-widget="gauge" data-src="{% url 'api:reports:district_graphs' district.id date.year date.month %}#worst_project{{ index }}"></div>
                            </div><!-- .actual-client-main -->
                            <div class="actual-client cf">
                            	<div class="over-expenditure">{% overunder_expenditure data.expenditure.actual data.expenditure.planned %}
                                    <br>({% overunder_percentage data.expenditure.actual data.expenditure.planned %})</div><!-- .expend-text -->
                                <div class="expenditure-to-date">Expenditure to date: {{data.expenditure.actual|format_currency }}</div><!-- .date-text -->
                                <div class="client-slider" data-widget="slider" data-src="{% url 'api:reports:district_graphs' district.id date.year date.month %}#worst_project_expenditure{{ index }}"> </div>
                            </div><!-- .actual-client -->
                        </div><!-- .actual-client-row -->
                    </div><!-- .actual-client-area -->
                </div><!-- .client-main -->
                <div class="comment-main-area">
                	<div class="comment-main marg cf">
                    	<div class="comment-text"><span class="comment">COMMENTS</span> (previous month): {{ data.last_month.comment }}<br><br><span class="comment">MITIGATION</span> (previous month): {{ data.last_month.mitigation }}</div><!-- .comment-text -->
                    </div><!-- .comment-main -->
                	<div class="comment-main cf">
                    	<div class="comment-text"><span class="comment">CURRENT COMMENTS: </span>{{ data.current_month.comment }}<br><br><span class="comment">CURRENT MITIGATION: </span>{{ data.current_month.mitigation }}</div><!-- .comment-text -->
                    </div><!-- .comment-main -->
                </div><!-- .comment-main-area -->
            </div><!-- .client-row -->
        </div>
    """)
    val = template.render(Context({
        "data" : context["projects"]["worst_performing"][index],
        "index" : index,
        "index1" : index + 1,
        "district" : context["district"],
        "date" : context["date"]
    }))

    return val
