from typing import Dict, List, Any
import matplotlib.pyplot as plt
import networkx as nx
from src.models.world import World
from src.models.country import Country

class WorldVisualizer:
    def __init__(self, world: World):
        self.world = world
        
    def plot_relationship_network(self) -> None:
        """Plot the network of country relationships"""
        G = nx.Graph()
        
        # Add nodes (countries)
        for name, country in self.world.countries.items():
            G.add_node(name, 
                      ideology=country.ideology,
                      state=country.state,
                      strength=country.strength)
        
        # Add edges (relationships)
        for name, country in self.world.countries.items():
            for other, relation in country.relationships.items():
                if relation in ["Ally", "Enemy"]:
                    G.add_edge(name, other, relationship=relation)
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        
        # Draw the network
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                             node_color=[self._get_node_color(G.nodes[node]['ideology']) 
                                       for node in G.nodes()],
                             node_size=[G.nodes[node]['strength'] * 100 
                                      for node in G.nodes()])
        
        # Draw edges
        nx.draw_networkx_edges(G, pos,
                             edge_color=[self._get_edge_color(G.edges[edge]['relationship']) 
                                       for edge in G.edges()],
                             width=2)
        
        # Add labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        # Add title
        plt.title("World Relationship Network")
        plt.axis('off')
        plt.show()
        
    def plot_resource_trends(self, country_name: str) -> None:
        """Plot resource trends for a specific country"""
        country = self.world.get_country(country_name)
        if not country:
            return
            
        plt.figure(figsize=(10, 6))
        
        # Plot resource levels
        resources = list(country.resources.keys())
        values = [country.resources[r]['value'] for r in resources]
        trends = [country.resources[r]['trend'] for r in resources]
        
        x = range(len(resources))
        width = 0.35
        
        plt.bar(x, values, width, label='Current Level')
        plt.plot(x, [v + t * 5 for v, t in zip(values, trends)], 
                'r--', label='Trend (5x)')
        
        plt.xlabel('Resource Type')
        plt.ylabel('Level')
        plt.title(f'Resource Levels and Trends for {country_name}')
        plt.xticks(x, resources)
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_global_trends(self) -> None:
        """Plot global trends over time"""
        plt.figure(figsize=(10, 6))
        
        trends = list(self.world.global_trends.keys())
        values = list(self.world.global_trends.values())
        
        plt.bar(trends, values)
        plt.xlabel('Trend Type')
        plt.ylabel('Value')
        plt.title('Global Trends')
        plt.ylim(0, 1)
        plt.grid(True)
        plt.show()
        
    def plot_sentiment_network(self) -> None:
        """Plot the network of country sentiments"""
        G = nx.DiGraph()
        
        # Add nodes (countries)
        for name, country in self.world.countries.items():
            G.add_node(name)
        
        # Add edges (sentiments)
        for name, country in self.world.countries.items():
            for other, sentiment in country.sentiment.items():
                if other in self.world.countries:
                    G.add_edge(name, other, weight=sentiment['value'])
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        
        # Draw the network
        pos = nx.spring_layout(G)
        
        # Draw edges with colors based on sentiment
        edges = G.edges()
        colors = [self._get_sentiment_color(G.edges[edge]['weight']) 
                 for edge in edges]
        widths = [abs(G.edges[edge]['weight']) * 2 
                 for edge in edges]
        
        nx.draw_networkx_edges(G, pos, edge_color=colors, width=widths)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=1000)
        
        # Add labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        # Add title
        plt.title("World Sentiment Network")
        plt.axis('off')
        plt.show()
        
    def _get_node_color(self, ideology: str) -> str:
        """Get color for node based on ideology"""
        colors = {
            "Democratic": "blue",
            "Authoritarian": "red",
            "Nationalist": "green",
            "Communist": "yellow",
            "Fascist": "purple"
        }
        return colors.get(ideology, "gray")
        
    def _get_edge_color(self, relationship: str) -> str:
        """Get color for edge based on relationship"""
        if relationship == "Ally":
            return "green"
        else:  # Enemy
            return "red"
            
    def _get_sentiment_color(self, sentiment: float) -> str:
        """Get color for edge based on sentiment value"""
        if sentiment > 0.3:
            return "green"
        elif sentiment < -0.3:
            return "red"
        else:
            return "gray"
            
    def generate_text_report(self) -> str:
        """Generate a text report of the current world state"""
        report = []
        
        # Add global trends
        report.append("=== Global Trends ===")
        for trend, value in self.world.global_trends.items():
            report.append(f"{trend}: {value:.2f}")
            
        # Add country states
        report.append("\n=== Country States ===")
        for name, country in self.world.countries.items():
            report.append(f"\n{name}:")
            report.append(f"  Ideology: {country.ideology}")
            report.append(f"  State: {country.state}")
            report.append(f"  Strength: {country.strength}")
            report.append("  Resources:")
            for resource, level in country.resources.items():
                trend_symbol = "↑" if level["trend"] > 0 else "↓" if level["trend"] < 0 else "→"
                report.append(f"    {resource}: {level['value']:.1f} {trend_symbol}")
                
        # Add recent events
        report.append("\n=== Recent Events ===")
        for event in self.world.events[-5:]:
            report.append(f"Turn {event['turn']}: {event['text']}")
            
        return "\n".join(report) 