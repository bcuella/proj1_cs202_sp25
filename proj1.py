#complete your tasks in this file
import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

#Task 1: Data Classes
@dataclass (frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str # "ocean", "mountains", "forest", "other"

@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

# --- Task 2: Example Data ---

region_conditions = [
    # Guatemala City, Guatemala (Central America)
    RegionCondition(
        Region(GlobeRect(14.5, 14.7, -90.6, -90.4), "Guatemala City", "mountains"),
        2024, 3000000, 12000000.0),

    # Tokyo, Japan (Asia)
    RegionCondition(
        Region(GlobeRect(35.5, 35.8, 139.5, 139.9), "Tokyo", "other"),
        2024, 37300000, 155000000.0),

    # Gulf of Mexico (Ocean)
    RegionCondition(
        Region(GlobeRect(25.0, 28.0, -95.0, -90.0), "Gulf of Mexico", "ocean"),
        2024, 0, 0.0),

    # SLO/Cal Poly
    RegionCondition(
        Region(GlobeRect(35.2, 35.4, -120.7, -120.6), "San Luis Obispo", "mountains"),
        2024, 47000, 250000.0)]

#Task 3: Implement External Functions (with Design Recipe)
#Purpose: Returns the tons of CO₂-equivalent emitted per person in the region per year. Returns 0.0 if population is zero.
#Input type: RegionCondition
#Output type: float
#Example input: emissions_per_capita(rc(pop=1000, ghg=5000.0))
#Example output:5.0
def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate / rc.pop

# Purpose: Estimates surface area of the region in square kilometers.
#Input type: GlobeRect
#Output type: float
#Example input:area(GlobeRect(0, 1, 0, 1))
#Example output: 12391.0
def area(gr: GlobeRect) -> float:
    r = 6378.1
    phi1, phi2 = math.radians(gr.lo_lat), math.radians(gr.hi_lat)
    lam1, lam2 = math.radians(gr.west_long), math.radians(gr.east_long)
    delta_lambda = lam2 - lam1
    if delta_lambda < 0:
        delta_lambda += 2 * math.pi
    return (r ** 2) * delta_lambda * abs(math.sin(phi2) - math.sin(phi1))

#Purpose: Returns the tons of CO₂-equivalent per square kilometer.
#Input type: RegionCondition
#Output type: float
#Example input: emissions_per_square_km(RC(ghg=1000, area=200))
#Example output: 5.0
def emissions_per_square_km(rc: RegionCondition) -> float:
    return rc.ghg_rate / area(rc.region.rect)

# Purpose: Takes a list of RegionCondition values and returns the name of the region with the highest population density
#Input type: List[RegionCondition]
#Output type: string
#Example input: densest([SmallDenseCity, LargeRural])
#Example output: "SmallDenseCity"
def densest(rc_list: List[RegionCondition]) -> str:
    if not rc_list:
        raise ValueError("List cannot be empty")
#Purpose: It's a helper function to fund the density.
#Input type: RegionCondition
#Output type: float
    def density(rc: RegionCondition) -> float:
        return rc.pop / area(rc.region.rect)

#Purpose: Recursive helper to find the RegionCondition with the maximum density.
#Input type: List[RegionCondition]
#Output type: RegionCondition
    def find_max(current_list: List[RegionCondition]) -> RegionCondition:
        if len(current_list) == 1:
            return current_list[0]

        first = current_list[0]
        max_of_rest = find_max(current_list[1:])

        if density(first) > density(max_of_rest):
            return first
        else:
            return max_of_rest

    top_region = find_max(rc_list)
    return top_region.region.name

#Task 4: Simulate Future Projections
#Purpose: SHows how regions change over time based on terrain-specific population growth.
#Input type: RegionCondition, int
#Output type: RegionCondition
#Example Input: project_condition(RC(pop=1000, terrain="other"), 10)
#Example Output: 1003
def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    rates = {
        "ocean": 0.0001,
        "mountains": 0.0005,
        "forest": -0.00001,
        "other": 0.0003
    }
    rate = rates.get(rc.region.terrain, 0.0)
    new_pop = int(rc.pop * ((1 + rate) ** years))
    if rc.pop == 0:
        new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)
    return RegionCondition(
        region=rc.region,
        year=rc.year + years,
        pop=new_pop,
        ghg_rate=new_ghg
    )