# create_it_dataset.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_it_invoice_data(num_samples=1500):
    """Generate synthetic IT service invoice data"""
    
    # IT-specific data
    service_categories = [
        'Software Development', 'Cloud Services', 'Cybersecurity', 
        'IT Consulting', 'System Integration', 'Data Analytics',
        'DevOps Services', 'AI/ML Solutions', 'Mobile Development',
        'Web Development', 'Database Management', 'Network Infrastructure'
    ]
    
    project_types = ['Fixed Price', 'Time & Materials', 'Retainer', 'Support Contract']
    client_industries = ['Finance', 'Healthcare', 'E-commerce', 'Education', 'Manufacturing', 'Government']
    countries = ['US', 'UK', 'CA', 'AU', 'DE', 'SG']
    
    # Common IT service items with realistic pricing
    service_items = {
        'Software Development': [
            ('Custom API Development', 150, 200),
            ('Frontend Development', 120, 180),
            ('Backend System Architecture', 180, 250),
            ('Database Design & Optimization', 160, 220)
        ],
        'Cloud Services': [
            ('AWS Infrastructure Setup', 100, 150),
            ('Azure Migration Services', 120, 180),
            ('Cloud Security Configuration', 140, 200),
            ('Kubernetes Cluster Management', 150, 220)
        ],
        'Cybersecurity': [
            ('Security Audit & Assessment', 200, 300),
            ('Penetration Testing', 180, 280),
            ('Security Policy Development', 150, 220),
            ('Incident Response Planning', 180, 250)
        ],
        'IT Consulting': [
            ('Technology Strategy Planning', 180, 250),
            ('System Architecture Review', 160, 220),
            ('Digital Transformation Consulting', 200, 300),
            ('IT Infrastructure Assessment', 150, 200)
        ]
    }
    
    data = []
    
    for i in range(num_samples):
        service_category = random.choice(service_categories)
        client_industry = random.choice(client_industries)
        country = random.choice(countries)
        project_type = random.choice(project_types)
        
        # Generate realistic items based on service category
        num_items = random.randint(1, 6)
        items = []
        total_hours = 0
        total_amount = 0
        
        available_services = service_items.get(service_category, [('General IT Consulting', 100, 150)])
        
        for j in range(num_items):
            service_name, min_rate, max_rate = random.choice(available_services)
            hours = random.randint(10, 100)
            hourly_rate = random.randint(min_rate, max_rate)
            amount = hours * hourly_rate
            
            items.append({
                'service_name': service_name,
                'hours': hours,
                'hourly_rate': hourly_rate,
                'amount': amount
            })
            total_hours += hours
            total_amount += amount
        
        # ML prediction targets
        # Discount based on project size and client industry
        discount = 0
        if total_amount > 20000:
            discount = round(random.uniform(8, 15), 2)
        elif total_amount > 10000 and client_industry in ['Finance', 'Healthcare']:
            discount = round(random.uniform(5, 12), 2)
        
        # Tax rate with IT-specific considerations
        tax_rates = {'US': 8.5, 'UK': 20.0, 'CA': 13.0, 'AU': 10.0, 'DE': 19.0, 'SG': 7.0}
        tax_rate = tax_rates[country]
        
        # Documentation complexity prediction
        doc_complexity = 'Low'
        if total_amount > 15000 or service_category in ['Cybersecurity', 'System Integration']:
            doc_complexity = 'High'
        elif total_amount > 8000:
            doc_complexity = 'Medium'
        
        # Payment terms based on project type
        payment_terms = 'Net 30'
        if project_type == 'Fixed Price':
            payment_terms = '50% Advance, 50% on Completion'
        elif project_type == 'Support Contract':
            payment_terms = 'Monthly in Advance'
        
        data.append({
            'invoice_id': f'IT-{2023000 + i}',
            'service_category': service_category,
            'client_industry': client_industry,
            'country': country,
            'project_type': project_type,
            'total_amount': total_amount,
            'total_hours': total_hours,
            'num_services': num_items,
            'discount': discount,
            'tax_rate': tax_rate,
            'documentation_complexity': doc_complexity,
            'payment_terms': payment_terms,
            'timestamp': datetime.now() - timedelta(days=random.randint(1, 365))
        })
    
    return pd.DataFrame(data)

# Generate dataset
df = generate_it_invoice_data(2000)
df.to_csv('it_invoice_dataset.csv', index=False)
print(f"IT Invoice dataset generated with {len(df)} records")