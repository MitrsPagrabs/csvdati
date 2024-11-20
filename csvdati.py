import pandas as pd
from datetime import datetime

def calculate_hours(start_time, end_time):
    try:
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        if end < start:
            return None
        return (end - start).seconds / 3600
    except Exception:
        return None

file_path = 'darba_laiki.csv'
data = pd.read_csv(file_path)

data['Nostrādātās stundas'] = data.apply(
    lambda row: calculate_hours(row['Sākums'], row['Beigas']), axis=1
)

data['Statuss'] = data['Nostrādātās stundas'].apply(
    lambda x: 'Valid' if x is not None else 'Invalid'
)

neparstradatas_dienas = data[data['Nostrādātās stundas'].isnull()]

if not neparstradatas_dienas.empty:
    for _, row in neparstradatas_dienas.iterrows():
        print(f"Darbinieks {row['Darbinieks']} nav nostrādājis derīgu darba dienu {row['Diena']}.")

data['Nostrādātās stundas'].fillna(0, inplace=True)

weekly_hours = data.groupby('Darbinieks')['Nostrādātās stundas'].sum().reset_index()
weekly_hours.columns = ['Darbinieks', 'Kopā stundas']

most_hours_employee = weekly_hours.loc[weekly_hours['Kopā stundas'].idxmax()]

output_path = 'darba_laika_rezultati.csv'
weekly_hours.to_csv(output_path, index=False)

print("Darba laika analīzes rezultāti:")
print(data)
print(f"Darbinieks ar visvairāk nostrādātām stundām: {most_hours_employee['Darbinieks']} ({most_hours_employee['Kopā stundas']} stundas)")
print(f"Rezultāti saglabāti failā: {output_path}")
