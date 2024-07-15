from redminelib import Redmine
import pandas as pd


redmine = Redmine()
delivery = redmine.project.get('return_repaired_10')
delivery_tasks = redmine.issue.filter(project_id=delivery.id, status_id='*')

issue = redmine.issue.get(150604)
workers_dict = {}
data = []
for issue in delivery_tasks:
    try:
        if issue.status.id in [17, 22, 23, 28, 29, 32, 38]:

            data.append({'Исполнитель': issue.assigned_to.name, 'Операция': issue.status.name, 'Адрес': issue.custom_fields[5]['value'],
                         'Дата': issue.updated_on.split('T')[0]})
    except Exception as e:
        pass

df = pd.DataFrame(data)
df.to_csv('Statistic_of_delivery.csv', sep=';', index=False, encoding='utf-8-sig')
print(df)