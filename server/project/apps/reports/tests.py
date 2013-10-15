from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.template import Template, Context
from project.apps.projects import factories
from project.apps.reports.templatetags import formatters

client = Client()

class ReportsTest(TestCase):
    def setUp(self):
        self.district = factories.DistrictFactory()

    def test_dashboard(self):
        url = reverse("reports:district_dashboard", args=(999, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse("reports:district_dashboard", args=(self.district.id, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_progress(self):
        url = reverse("reports:district_progress", args=(999, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse("reports:district_progress", args=(self.district.id, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_perform(self):
        url = reverse("reports:district_perform", args=(999, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse("reports:district_perform", args=(self.district.id, 2013, 6))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


class FormatterTest(TestCase):
    def test_currency_formatter(self):
        self.assertEqual(formatters.format_currency(10000), "R10,000")
        self.assertEqual(formatters.format_currency(10000.23), "R10,000.23")
        self.assertEqual(formatters.format_currency(10000.569), "R10,000.57")
        self.assertEqual(formatters.format_currency(10000.573), "R10,000.57")
        self.assertEqual(formatters.format_currency(0), "R0.00")
        self.assertEqual(formatters.format_currency(""), "-")

    def test_percentage_formatter(self):
        self.assertEqual(formatters.format_percentage(20), "20%")
        self.assertEqual(formatters.format_percentage(20.5), "20.5%")
        self.assertEqual(formatters.format_percentage(20.56), "20.6%")
        self.assertEqual(formatters.format_percentage(""), "-")

    def test_currency_tag(self):

        template = Template(
            """
            {% load formatters %}
            {{ num|format_currency }}
            """
        )
        val = template.render(Context({"num" : 10000}))
        self.assertEqual(val.strip(), "R10,000")
        
        val = template.render(Context({"num" : 10000.23}))
        self.assertEqual(val.strip(), "R10,000.23")

    def test_percentage_tag(self):
        template = Template("""
            {% load formatters %}
            {{ num|format_percentage }}
        """)

        val = template.render(Context({"num" : 20}))
        self.assertEqual(val.strip(), "20%")

        val = template.render(Context({"num" : 20.23}))
        self.assertEqual(val.strip(), "20.2%")

        val = template.render(Context())
        self.assertEqual(val.strip(), "-")
