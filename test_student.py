import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positively to your grade.
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(lo_lat=0.0, hi_lat=1.0, west_long=0.0, east_long=1.0)
        self.region = Region(rect=self.rect, name="EquatorLand", terrain="other")
        self.rc = RegionCondition(region=self.region, year=2024, pop=1000, ghg_rate=5000.0)

    #Task 3 Test Cases

    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(self.rc), 5.0)
        zero_rc = RegionCondition(self.region, 2024, 0, 5000.0)
        self.assertEqual(emissions_per_capita(zero_rc), 0.0)

    def test_area(self):
        value = area(self.rect)
        self.assertGreater(value, 0)
        wrap_rect = GlobeRect(lo_lat=0.0, hi_lat=1.0, west_long=179.0, east_long=-179.0)
        wrap_area = area(wrap_rect)
        self.assertGreater(wrap_area, 0)
        self.assertAlmostEqual(wrap_area, value * 2, delta=1.0)

    def test_emissions_per_square_km(self):
        a = area(self.rect)
        expected = 5000.0 / a
        self.assertAlmostEqual(emissions_per_square_km(self.rc), expected)

    def test_densest(self):
        tokyo_rc = region_conditions[1]
        ocean_rc = region_conditions[2]
        self.assertEqual(densest([tokyo_rc, ocean_rc]), "Tokyo")
        self.assertEqual(densest([self.rc, tokyo_rc]), "Tokyo")

#Task 4 test cases
    def test_project_condition(self):
        # Test 1 year growth for "other" terrain
        projected = project_condition(self.rc, 1)
        self.assertEqual(projected.year, 2025)
        self.assertEqual(projected.pop, 1000)
        self.assertAlmostEqual(projected.ghg_rate, 5000.0)

        # Test 1 year growth for "mountains" (SLO)
        slo_rc = region_conditions[3]
        projected_slo = project_condition(slo_rc, 1)
        # 47000 * 1.0005 = 47023.5 -> 47023
        self.assertEqual(projected_slo.pop, 47023)


if __name__ == '__main__':
    unittest.main()