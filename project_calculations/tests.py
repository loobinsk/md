from django.test import TestCase
from .services import BasicCalculation 
from projects.models import Project
from sales.models import SalesInit


class TestServices(TestCase):

    def setUp(self):
        # prj = Project.objects.create(name='блаблаб', currency_multiplication=1,
        #                         time_detalization=1, tax_model=1, author=1,)
        # SalesInit.objects.create(project=prj)
        print("setUp: Run once for every test method to setup clean data.")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        project = Project.objects.all().first()
        bc = BasicCalculation(project)
        self.assertEqual(bc.main_parameters_calc(), 'The lion says "roar"')