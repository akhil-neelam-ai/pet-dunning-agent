"""
ezyVet Mock API Integration
Simulates veterinary practice management system data
In production, this would connect to real ezyVet REST API
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def get_pet_medical_history(pet_id: str, user_id: str) -> Dict:
    """
    Fetch complete medical history for a pet from ezyVet.

    In production, this would call:
    GET https://api.trial.ezyvet.com/v2/animal/{pet_id}

    Returns detailed medical records, visit history, treatments, and prescriptions.
    """

    # Mock medical histories for demo pets
    mock_medical_data = {
        'user_123': {  # Maria Rodriguez - Bella (Diabetes)
            'pet_id': 'pet_001',
            'pet_name': 'Bella',
            'species': 'Dog',
            'breed': 'Golden Retriever',
            'age_years': 8,
            'weight_lbs': 68,
            'primary_condition': 'Diabetes Mellitus (Insulin Dependent)',
            'diagnosis_date': '2022-03-15',
            'current_medications': [
                {
                    'name': 'Vetsulin (Porcine Insulin)',
                    'dosage': '12 units',
                    'frequency': 'Twice daily',
                    'cost_per_month': 85.00,
                    'critical': True
                },
                {
                    'name': 'Glucose Test Strips',
                    'dosage': 'As needed',
                    'frequency': 'Daily monitoring',
                    'cost_per_month': 45.00,
                    'critical': True
                }
            ],
            'recent_visits': [
                {
                    'date': '2024-11-20',
                    'type': 'Regular Checkup',
                    'veterinarian': 'Dr. Sarah Chen',
                    'notes': 'Blood glucose levels stable. Continue current insulin regimen. Schedule recheck in 6 weeks.',
                    'total_cost': 125.00
                },
                {
                    'date': '2024-10-05',
                    'type': 'Emergency',
                    'veterinarian': 'Dr. Michael Torres',
                    'notes': 'Hypoglycemic episode. Adjusted insulin dose from 14 to 12 units. Owner educated on early warning signs.',
                    'total_cost': 380.00
                }
            ],
            'upcoming_appointments': [
                {
                    'date': '2025-01-02',
                    'type': 'Insulin Recheck',
                    'veterinarian': 'Dr. Sarah Chen',
                    'estimated_cost': 125.00
                }
            ],
            'medical_alerts': [
                'CRITICAL: Insulin-dependent diabetes. Missing doses can be life-threatening.',
                'Monitor for signs of hypoglycemia: weakness, trembling, confusion.',
                'Keep Karo syrup on hand for emergency glucose support.'
            ],
            'lifetime_value_drivers': [
                'Requires bi-weekly vet visits for monitoring',
                'Monthly medication costs: $130',
                'Annual diabetic workup: $450',
                'High risk for complications requiring emergency care'
            ],
            'continuity_of_care_importance': 'CRITICAL',
            'estimated_remaining_treatment_duration': 'Lifelong'
        },

        'user_456': {  # James Mitchell - Max (Heartworm)
            'pet_id': 'pet_002',
            'pet_name': 'Max',
            'species': 'Dog',
            'breed': 'Labrador Mix',
            'age_years': 5,
            'weight_lbs': 72,
            'primary_condition': 'Heartworm Disease (Stage 2)',
            'diagnosis_date': '2024-09-10',
            'current_medications': [
                {
                    'name': 'Doxycycline',
                    'dosage': '200mg',
                    'frequency': 'Twice daily',
                    'cost_per_month': 35.00,
                    'critical': True
                },
                {
                    'name': 'Prednisone',
                    'dosage': '20mg',
                    'frequency': 'Once daily',
                    'cost_per_month': 15.00,
                    'critical': True
                }
            ],
            'recent_visits': [
                {
                    'date': '2024-11-15',
                    'type': 'Treatment Follow-up',
                    'veterinarian': 'Dr. Emily Rodriguez',
                    'notes': 'Completed month 2 of slow-kill protocol. Coughing has decreased. Continue current medications.',
                    'total_cost': 95.00
                }
            ],
            'upcoming_appointments': [
                {
                    'date': '2024-12-20',
                    'type': 'Treatment Progress Check',
                    'veterinarian': 'Dr. Emily Rodriguez',
                    'estimated_cost': 95.00
                },
                {
                    'date': '2025-03-10',
                    'type': 'Heartworm Antigen Test',
                    'veterinarian': 'Dr. Emily Rodriguez',
                    'estimated_cost': 180.00
                }
            ],
            'medical_alerts': [
                'Currently undergoing heartworm treatment - exercise restriction required',
                'Watch for coughing, lethargy, or difficulty breathing',
                'Treatment protocol: 6-12 months'
            ],
            'lifetime_value_drivers': [
                'Active treatment requiring monthly monitoring',
                'Monthly medication costs: $50',
                'Mid-protocol - requires completion for full recovery'
            ],
            'continuity_of_care_importance': 'HIGH',
            'estimated_remaining_treatment_duration': '4-10 months'
        },

        'user_789': {  # Sarah Chen - Whiskers (Kidney Disease)
            'pet_id': 'pet_003',
            'pet_name': 'Whiskers',
            'species': 'Cat',
            'breed': 'Domestic Shorthair',
            'age_years': 12,
            'weight_lbs': 9,
            'primary_condition': 'Chronic Kidney Disease (Stage 3)',
            'diagnosis_date': '2023-06-20',
            'current_medications': [
                {
                    'name': 'Benazepril',
                    'dosage': '2.5mg',
                    'frequency': 'Once daily',
                    'cost_per_month': 25.00,
                    'critical': True
                },
                {
                    'name': 'Epakitin (Phosphate Binder)',
                    'dosage': '1 scoop',
                    'frequency': 'With meals',
                    'cost_per_month': 40.00,
                    'critical': True
                },
                {
                    'name': 'Kidney Support Diet (Hill\'s k/d)',
                    'dosage': 'Prescription food',
                    'frequency': 'Daily',
                    'cost_per_month': 65.00,
                    'critical': True
                }
            ],
            'recent_visits': [
                {
                    'date': '2024-11-10',
                    'type': 'Quarterly Bloodwork',
                    'veterinarian': 'Dr. Jessica Park',
                    'notes': 'Creatinine 3.2 (stable). Continue current management. Discuss SubQ fluids if values worsen.',
                    'total_cost': 245.00
                }
            ],
            'upcoming_appointments': [
                {
                    'date': '2025-02-10',
                    'type': 'Kidney Recheck Bloodwork',
                    'veterinarian': 'Dr. Jessica Park',
                    'estimated_cost': 245.00
                }
            ],
            'medical_alerts': [
                'CRITICAL: Stage 3 CKD. Missing medications accelerates kidney decline.',
                'Monitor for decreased appetite, vomiting, or increased lethargy.',
                'May require subcutaneous fluid therapy if disease progresses.'
            ],
            'lifetime_value_drivers': [
                'Requires quarterly bloodwork monitoring',
                'Monthly medication + special diet: $130',
                'Progressive disease - may need hospitalization',
                'Quality of life heavily dependent on consistent treatment'
            ],
            'continuity_of_care_importance': 'CRITICAL',
            'estimated_remaining_treatment_duration': 'Lifelong'
        }
    }

    return mock_medical_data.get(user_id, {
        'pet_id': 'unknown',
        'pet_name': 'Unknown',
        'species': 'Unknown',
        'primary_condition': 'Unknown',
        'current_medications': [],
        'recent_visits': [],
        'upcoming_appointments': [],
        'medical_alerts': [],
        'continuity_of_care_importance': 'MEDIUM'
    })


def get_medication_adherence_score(user_id: str) -> Dict:
    """
    Calculate medication adherence score based on prescription refill history.

    In production, would analyze:
    - Prescription refill timing
    - Missed appointment patterns
    - Historical payment reliability
    """

    mock_adherence_data = {
        'user_123': {  # Maria - Very compliant
            'adherence_score': 95,
            'adherence_tier': 'Excellent',
            'refills_on_time': 18,
            'refills_late': 1,
            'missed_appointments_last_year': 0,
            'notes': 'Highly engaged pet parent. Refills medications early. Always keeps appointments.'
        },
        'user_456': {  # James - Good compliance
            'adherence_score': 82,
            'adherence_tier': 'Good',
            'refills_on_time': 6,
            'refills_late': 2,
            'missed_appointments_last_year': 1,
            'notes': 'Generally compliant. Occasional late refills but always follows through.'
        },
        'user_789': {  # Sarah - Struggling with compliance
            'adherence_score': 65,
            'adherence_tier': 'Fair',
            'refills_on_time': 4,
            'refills_late': 5,
            'missed_appointments_last_year': 2,
            'notes': 'Shows signs of financial stress. Often delays refills until last minute.'
        }
    }

    return mock_adherence_data.get(user_id, {
        'adherence_score': 70,
        'adherence_tier': 'Fair',
        'refills_on_time': 0,
        'refills_late': 0,
        'missed_appointments_last_year': 0,
        'notes': 'Insufficient history'
    })


def assess_medical_urgency(medical_data: Dict, adherence_data: Dict) -> Dict:
    """
    Assess how urgent it is to keep this customer's care continuous.
    Combines medical criticality + adherence history.
    """

    care_importance = medical_data.get('continuity_of_care_importance', 'MEDIUM')
    adherence_score = adherence_data.get('adherence_score', 70)

    # Calculate urgency score (0-100)
    importance_weight = {
        'CRITICAL': 100,
        'HIGH': 75,
        'MEDIUM': 50,
        'LOW': 25
    }

    base_urgency = importance_weight.get(care_importance, 50)

    # Boost urgency if they have good adherence (don't want to lose engaged customers)
    if adherence_score >= 85:
        urgency_modifier = 1.2
        urgency_reason = 'Highly engaged pet parent at risk of churn'
    elif adherence_score >= 70:
        urgency_modifier = 1.1
        urgency_reason = 'Generally compliant customer worth retaining'
    else:
        urgency_modifier = 1.0
        urgency_reason = 'Support needed to maintain treatment adherence'

    final_urgency = min(100, base_urgency * urgency_modifier)

    # Determine retention strategy
    if final_urgency >= 90:
        strategy = 'MAXIMUM_RETENTION'
        action = 'Offer Bridge Plan + payment flexibility + medication assistance program'
    elif final_urgency >= 70:
        strategy = 'HIGH_RETENTION'
        action = 'Offer Bridge Plan + emphasize continuity of care'
    elif final_urgency >= 50:
        strategy = 'MODERATE_RETENTION'
        action = 'Offer Bridge Plan + flexible payment options'
    else:
        strategy = 'STANDARD_RETENTION'
        action = 'Standard retry with payment plan offer'

    return {
        'urgency_score': round(final_urgency, 1),
        'urgency_tier': strategy,
        'recommended_action': action,
        'reasoning': urgency_reason,
        'medical_importance': care_importance,
        'adherence_score': adherence_score
    }


# Production ezyVet API integration (commented out for mock demo)
"""
import requests

def get_pet_medical_history_production(pet_id: str, api_key: str) -> Dict:
    '''
    Production ezyVet API call
    Documentation: https://developer.ezyvet.com/docs
    '''
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        f'https://api.trial.ezyvet.com/v2/animal/{pet_id}',
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'ezyVet API error: {response.status_code}')
"""
