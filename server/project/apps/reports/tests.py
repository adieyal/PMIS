from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories

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
