 
# lib/utils/tools.py
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class CalculateEmissionsInput(BaseModel):
    category: str = Field(..., description="Category like transportation, diet, energy")
    parameters: dict = Field(..., description="Key-value pairs for calculation")

class CalculateEmissionsTool(BaseTool):
    name: str = "calculate_emissions"
    description: str = "Calculate carbon emissions for a specific category using emission factors"
    args_schema: Type[BaseModel] = CalculateEmissionsInput

    def _run(self, category: str, parameters: dict) -> float:
        # Implement your emission calculation logic here
        # This could use a database, API, or local calculation
        
        emission_factors = {
            "transportation": {
                "gasoline_car": 0.404,  # kg CO2 per mile
                "diesel_car": 0.453,    # kg CO2 per mile
                "electric_car": 0.200,   # kg CO2 per mile (varies by grid)
            },
            "diet": {
                "beef": 27.0,    # kg CO2 per kg
                "chicken": 6.9,  # kg CO2 per kg
                "vegetables": 2.0, # kg CO2 per kg
            }
        }
        
        # Simple calculation example
        if category == "transportation":
            vehicle_type = parameters.get("vehicle_type", "gasoline_car")
            distance_miles = parameters.get("distance_miles", 0)
            return distance_miles * emission_factors[category][vehicle_type]
        
        # Add more category calculations...
        
        return 0.0

class FetchBenchmarkDataInput(BaseModel):
    region: str = Field(..., description="Geographic region for benchmarking")
    household_size: int = Field(..., description="Number of people in household")

class FetchBenchmarkDataTool(BaseTool):
    name: str = "fetch_benchmark_data"
    description: str = "Fetch benchmark carbon footprint data for comparison"
    args_schema: Type[BaseModel] = FetchBenchmarkDataInput

    def _run(self, region: str, household_size: int) -> dict:
        # This could fetch from your Supabase database or external API
        benchmark_data = {
            "regional_average": 12000,  # kg CO2 annually
            "similar_household_average": 11000,
            "national_average": 16000,
            "sustainable_target": 4000
        }
        
        return benchmark_data