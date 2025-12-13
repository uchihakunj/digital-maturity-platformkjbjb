import pandas as pd

def calculate_maturity_index(row):
    """
    Calculates the overall Maturity Index from individual dimension scores.
    Simple average.
    """
    # Assuming the row contains the score columns
    scores = [row['tech_score'], row['culture_score'], row['process_score'], row['skills_score'], row['risk_score']]
    return sum(scores) / len(scores)

def get_recommendations(row):
    """
    Generates recommendations based on scores.
    Returns a dictionary of dimension -> recommendation string.
    """
    recommendations = {}
    
    # Tech Recommendations
    if row['tech_score'] < 2.5:
        recommendations['Tech'] = "Legacy systems detected. Prioritize cloud migration and API modernization."
    elif row['tech_score'] < 4.0:
        recommendations['Tech'] = "Good foundation. Focus on AI integration and data analytics."
    else:
        recommendations['Tech'] = "Industry leader. Explore cutting-edge tech like Quantum or Edge computing."
        
    # Culture Recommendations
    if row['culture_score'] < 2.5:
        recommendations['Culture'] = "Siloed teams. Implement cross-functional agile squads."
    elif row['culture_score'] < 4.0:
        recommendations['Culture'] = "Collaborative. Encourage more experimentation and psychological safety."
    else:
        recommendations['Culture'] = "Innovative culture. Maintain by sponsoring hackathons and external partnerships."

    # Process Recommendations
    if row['process_score'] < 2.5:
        recommendations['Process'] = "Manual & reactive. Automate core workflows immediately."
    elif row['process_score'] < 4.0:
        recommendations['Process'] = "Defined processes. Move towards data-driven process optimization."
    else:
        recommendations['Process'] = "Optimized. focus on predictive process modeling."

    # Skills Recommendations
    if row['skills_score'] < 2.5:
        recommendations['Skills'] = "Critical skill gaps. Initiate comprehensive upskilling programs."
    elif row['skills_score'] < 4.0:
        recommendations['Skills'] = "Specialized gaps. Hire for key roles in AI/Data."
    else:
        recommendations['Skills'] = "Strong talent pool. Focus on retention and leadership."

    # Risk Recommendations
    if row['risk_score'] < 2.5:
        recommendations['Risk'] = "High Exposure. Implement robust cybersecurity frameworks immediately."
    elif row['risk_score'] < 4.0:
        recommendations['Risk'] = "Moderate Risk. Regular audits and compliance checks needed."
    else:
        recommendations['Risk'] = "Resilient. Focus on proactive threat hunting and zero-trust."

    return recommendations
