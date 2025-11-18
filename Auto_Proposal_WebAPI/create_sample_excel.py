"""
Create a sample Excel template for BOQ Items import
"""
import pandas as pd

# Sample data
data = {
    'ProjectType': ['Residential', 'Commercial', 'Saloon', 'Hospital'],
    'Title': ['PVC Pipes', 'Electrical Wiring', 'False Ceiling', 'Medical Gas Pipeline'],
    'Description': [
        '110mm PVC plumbing pipes for drainage system',
        'Complete electrical wiring work with MCB board',
        'Providing and fixing suspended false ceiling',
        'Complete medical gas pipeline installation'
    ],
    'Unit': ['running meter', 'point', 'sqft', 'point'],
    'BasicRate': [150.00, 250.00, 70.00, 5000.00],
    'PremiumRate': [185.00, 300.00, 80.00, 6000.00]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
excel_file = 'BOQ_Items_Template.xlsx'
df.to_excel(excel_file, index=False, sheet_name='BOQ Items')

print(f"✅ Sample Excel template created: {excel_file}")
print(f"\nTemplate contains {len(df)} sample rows")
print("\nColumns:")
for col in df.columns:
    print(f"  - {col}")
