import unittest
from datetime import datetime
from models.country import Country, HistoricalEvent
from models.world import World
from simulation.engine import SimulationEngine

class TestEnhancedState(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.world = World()
        self.engine = SimulationEngine()
        
    def test_country_sentiment(self):
        """Test sentiment tracking system."""
        country = Country("TestCountry", 100, "Democratic")
        
        # Test initial sentiment
        self.assertEqual(country.sentiment.get("OtherCountry", 0.0), 0.0)
        
        # Test sentiment update
        country.update_sentiment("OtherCountry", 0.5)
        self.assertEqual(country.sentiment["OtherCountry"], 0.5)
        
        # Test sentiment bounds
        country.update_sentiment("OtherCountry", 0.6)  # Should cap at 1.0
        self.assertEqual(country.sentiment["OtherCountry"], 1.0)
        
        country.update_sentiment("OtherCountry", -2.0)  # Should cap at -1.0
        self.assertEqual(country.sentiment["OtherCountry"], -1.0)
        
    def test_historical_events(self):
        """Test historical event tracking."""
        country = Country("TestCountry", 100, "Democratic")
        
        # Create and add historical event
        event = HistoricalEvent(
            timestamp=datetime.now(),
            description="Test Event",
            impact=0.5,
            related_countries=["TestCountry", "OtherCountry"]
        )
        country.add_historical_event(event)
        
        # Verify event was added
        self.assertEqual(len(country.history), 1)
        self.assertEqual(country.history[0].description, "Test Event")
        
    def test_world_global_tension(self):
        """Test global tension tracking."""
        # Add event with positive impact
        self.world.add_event("War declared", 0.3, ["Country1", "Country2"])
        self.assertAlmostEqual(self.world.global_tension, 0.3)
        
        # Add event with negative impact
        self.world.add_event("Peace treaty signed", -0.2, ["Country1", "Country2"])
        self.assertAlmostEqual(self.world.global_tension, 0.1)
        
    def test_resource_management(self):
        """Test country resource management."""
        country = Country("TestCountry", 100, "Democratic")
        
        # Test initial resources
        self.assertEqual(country.resources["military"], 100)
        self.assertEqual(country.resources["economic"], 100)
        self.assertEqual(country.resources["diplomatic"], 100)
        
        # Test resource updates
        country.update_resources("military", -20)
        self.assertEqual(country.resources["military"], 80)
        
        # Test resource bounds
        country.update_resources("economic", -150)  # Should not go below 0
        self.assertEqual(country.resources["economic"], 0)
        
    def test_relationship_context(self):
        """Test relationship context generation."""
        country = Country("TestCountry", 100, "Democratic")
        
        # Set up relationship and sentiment
        country.set_relationship("OtherCountry", "Ally")
        country.update_sentiment("OtherCountry", 0.5)
        
        # Add historical event
        event = HistoricalEvent(
            timestamp=datetime.now(),
            description="Alliance formed",
            impact=0.3,
            related_countries=["TestCountry", "OtherCountry"]
        )
        country.add_historical_event(event)
        
        # Get and verify context
        context = country.get_relationship_context("OtherCountry")
        self.assertEqual(context["formal_relation"], "Ally")
        self.assertEqual(context["sentiment"], 0.5)
        self.assertEqual(len(context["recent_history"]), 1)
        
    def test_war_resolution(self):
        """Test enhanced war resolution system."""
        # Set up countries
        usa = Country("USA", 100, "Democratic")
        ussr = Country("USSR", 80, "Communist")
        
        self.world.add_country(usa)
        self.world.add_country(ussr)
        
        # Simulate war victory
        events = self.engine._handle_war_victory(usa, ussr)
        
        # Verify war effects
        self.assertLess(usa.resources["military"], 100)  # Resources should be depleted
        self.assertLess(ussr.resources["military"], 80)
        self.assertLess(ussr.internal_stability, 1.0)  # Stability should be affected
        self.assertLess(ussr.sentiment["USA"], 0)  # Sentiment should be negative
        
    def test_simulation_snapshot(self):
        """Test enhanced simulation snapshot generation."""
        # Add countries
        self.engine.add_country_with_agent("USA", 100, "Democratic", "Cautious")
        self.engine.add_country_with_agent("USSR", 80, "Communist", "Aggressive")
        
        # Run simulation for one turn
        history = self.engine.run_simulation(turns=1)
        
        # Verify snapshot structure
        snapshot = history[0]
        self.assertIn("global_state", snapshot)
        self.assertIn("countries", snapshot)
        
        # Verify country data includes new fields
        usa_data = snapshot["countries"]["USA"]
        self.assertIn("internal_stability", usa_data)
        self.assertIn("resources", usa_data)
        self.assertIn("sentiment", usa_data)

if __name__ == '__main__':
    unittest.main() 