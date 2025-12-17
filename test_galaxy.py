#!/usr/bin/env python3
"""
Test script for the GalaxyService implementation
"""

import sys
import os
sys.path.append('/home/engine/project')

from database import Database
from services import GalaxyService

def test_galaxy_service():
    """Test the GalaxyService functionality"""
    print("Testing GalaxyService...")
    
    # Initialize database and service
    db = Database()
    galaxy_service = GalaxyService(db)
    
    # Test getting all prompts
    prompts = db.get_all_prompts()
    print(f"Found {len(prompts)} prompts in database")
    
    if prompts:
        print("\nFirst few prompts:")
        for i, prompt in enumerate(prompts[:3]):
            print(f"{i+1}. {prompt.title} ({prompt.category}) - Tags: {prompt.tags}")
    
    # Test galaxy data creation
    try:
        galaxy_data = galaxy_service.create_galaxy_data()
        print(f"\nGalaxy data created successfully!")
        print(f"- Nodes: {len(galaxy_data['nodes'])}")
        print(f"- Edges: {len(galaxy_data['edges'])}")
        print(f"- Categories: {galaxy_data['categories']}")
        print(f"- Stats: {galaxy_data['stats']}")
        
        # Test statistics
        stats = galaxy_service.get_galaxy_statistics()
        print(f"\nGalaxy statistics:")
        for key, value in stats.items():
            print(f"- {key}: {value}")
        
        # Test similarity calculation if we have at least 2 prompts
        if len(prompts) >= 2:
            similarity = galaxy_service.calculate_similarity_score(prompts[0], prompts[1])
            print(f"\nSimilarity between first two prompts: {similarity:.3f}")
        
    except Exception as e:
        print(f"Error creating galaxy data: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\nGalaxyService test completed successfully!")
    return True

if __name__ == "__main__":
    test_galaxy_service()