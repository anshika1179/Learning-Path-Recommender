# Simplified agents module to bypass CrewAI/Langchain compatibility issues with Python 3.14
import json

class MockCrew:
    """Mock Crew class that returns a sample roadmap"""
    def kickoff(self):
        # Return a sample roadmap structure
        return json.dumps({
            "roadmap": [
                {
                    "title": "Python Fundamentals",
                    "week": 1,
                    "week_end": 2,
                    "difficulty": "Beginner",
                    "tasks": "Learn basic syntax, data types, and control structures"
                },
                {
                    "title": "Data Structures & Algorithms",
                    "week": 3,
                    "week_end": 5,
                    "difficulty": "Intermediate",
                    "tasks": "Master lists, dictionaries, sets, and basic algorithms"
                },
                {
                    "title": "Machine Learning Basics",
                    "week": 6,
                    "week_end": 9,
                    "difficulty": "Intermediate",
                    "tasks": "Introduction to scikit-learn, pandas, and numpy"
                },
                {
                    "title": "Deep Learning with TensorFlow",
                    "week": 10,
                    "week_end": 14,
                    "difficulty": "Advanced",
                    "tasks": "Neural networks, CNNs, and model training"
                }
            ],
            "weekly_plan": [
                {"week": 1, "tasks": "Complete Python basics course, practice exercises"},
                {"week": 2, "tasks": "Build small projects, review concepts"},
                {"week": 3, "tasks": "Study data structures, implement common patterns"},
                {"week": 4, "tasks": "Practice algorithm problems"},
                {"week": 5, "tasks": "Complete data structures module"},
                {"week": 6, "tasks": "Introduction to ML concepts"},
                {"week": 7, "tasks": "Hands-on with scikit-learn"},
                {"week": 8, "tasks": "Data preprocessing and feature engineering"},
                {"week": 9, "tasks": "Build ML models, evaluate performance"},
                {"week": 10, "tasks": "Introduction to neural networks"},
                {"week": 11, "tasks": "TensorFlow basics"},
                {"week": 12, "tasks": "Build and train CNNs"},
                {"week": 13, "tasks": "Advanced architectures"},
                {"week": 14, "tasks": "Final project"}
            ]
        })

def create_crew(profile_text, progress=""):
    """
    Create a mock crew that returns a sample roadmap.
    
    Note: This is a simplified version to bypass CrewAI/Langchain compatibility
    issues with Python 3.14. For full AI-powered functionality, use Python 3.10-3.11.
    """
    print(f"Creating learning path for profile: {profile_text}")
    if progress:
        print(f"Progress: {progress}")
    
    return MockCrew()
