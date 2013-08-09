import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories
from datetime import datetime
from project.apps.api.reports import graphhelpers

client = Client()

class GraphJson(TestCase):
    def setUp(self):
        self.municipality = factories.MunicipalityFactory()
        self.district = self.municipality.district
        self.year, self.month = 2013, 6
        self.url = reverse("api:reports:district_graphs", args=(self.district.id, self.year, self.month))
        self.date = datetime(self.year, self.month, 1)

        for i in range(5):
            project = factories.ProjectFactory(municipality=self.municipality)
            submission = factories.MonthlySubmissionFactory(project=project, actual_progress=i*10, actual_expenditure=i*10, date=self.date)
            planning = factories.PlanningFactory(project=project, planned_progress=i*20, planned_expenses=i*20, date=self.date)
            factories.ProjectFinancialFactory(project=project, total_anticipated_cost=10)

        self.response = client.get(self.url)
        self.js = json.loads(self.response.content)

    def test_gauges(self):

        self.assertEqual(self.response.status_code, 200)

        for i in range(0, 5):
            gauge = "gauge%d" % (i + 1)
            self.assertIn(gauge, self.js)
            self.assertEqual(self.js[gauge][0]["position"], (i * 2) / 10.)
            self.assertEqual(self.js[gauge][1]["position"], i / 10.)

    #def test_pies(self):
    #    for i in range(0, 5):
    #        pie = "stagespie%d" % (i + 1)
    #        print pie
    #        self.assertIn(pie, self.js)
        

    # TODO re-enable
    def test_client_sliders(self):

        for i in range(0, 5):
            slider = "client_slider%d" % (i + 1)
            self.assertIn(slider, self.js)
            if i == 0:
                # Minimum value for the position is 0.1 regardless of the actual value
                self.assertEqual(self.js[slider][0]["position"], 0.1)
                self.assertEqual(self.js[slider][1]["position"], 0.1)
    #        else:
    #            # Values should swap around because the position of the sliders
    #            # swaps if val1 > val 2
    #            import pdb; pdb.set_trace()
    #            self.assertEqual(self.js[slider][0]["position"], i / 10.)
    #            self.assertEqual(self.js[slider][1]["position"], (i * 2) / 10.)
    # TODO add tests to test budget calculations for slider and also when budget is 0

class TestGraphHelpers(TestCase):
    def test_dashboard_gauge(self):
        gauge2 = graphhelpers.dashboard_gauge(1, 1)
        self.assertEqual(gauge2[0]["text"], "Planned")
        self.assertEqual(gauge2[1]["text"], "Actual")

        gauge3 = graphhelpers.dashboard_gauge(1, 1, text1="abc", text2="def")
        self.assertEqual(gauge3[0]["text"], "abc")
        self.assertEqual(gauge3[1]["text"], "def")

    def test_dashboard_slider(self):
        slider1 = graphhelpers.dashboard_slider(0, 0, "DoE")
        self.assertEqual(slider1[0]["position"], 0.1)
        self.assertEqual(slider1[1]["position"], 0.1)

        slider2 = graphhelpers.dashboard_slider(1, 1, "DoE")
        self.assertEqual(slider2[0]["position"], 0.8)
        self.assertEqual(slider2[1]["position"], 0.8)

        slider3 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE")
        self.assertEqual(slider3[0]["marker-text"], "Planned")
        self.assertEqual(slider3[1]["marker-text"], "Actual")
        slider3 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE", text1="aaa", text2="bbb")
        self.assertEqual(slider3[0]["marker-text"], "aaa")
        self.assertEqual(slider3[1]["marker-text"], "bbb")

        slider4 = graphhelpers.dashboard_slider(0.7, 0.5, "DoE", threshold=0.5)
        self.assertEqual(slider4[0]["bar-color"], graphhelpers.clientcolors["DoE"])
        self.assertEqual(slider4[1]["bar-color"], graphhelpers.clientcolors["DoE"])

        slider5 = graphhelpers.dashboard_slider(0.7, 0.5, "DoE", threshold=0.1)
        self.assertEqual(slider5[1]["bar-color"], graphhelpers.red)
        self.assertEqual(slider5[0]["bar-color"], graphhelpers.clientcolors["DoE"])

        slider6 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE", threshold=0.1)
        self.assertEqual(slider6[0]["bar-color"], graphhelpers.clientcolors["DoE"])
        self.assertEqual(slider6[1]["bar-color"], graphhelpers.red)

        
        slider7 = graphhelpers.dashboard_slider(0.5, 0.55, "DoE", threshold=0.1)
        self.assertEqual(slider7[0]["marker-text"], "")

