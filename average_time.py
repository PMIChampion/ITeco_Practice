from redminelib import Redmine
from datetime import datetime, timedelta

redmine = Redmine()

delivery = redmine.project.get('return_repaired_10')
delivery_tasks = redmine.issue.filter(project_id=delivery.id, status_id='*')
average_time = {}
issue = redmine.issue.get(150403)
total_time = timedelta()
cnt = 0
tracker = 0
for task in delivery_tasks:
    try:
        start_time = ''
        task_assigned = datetime.fromisoformat(task.journals[0]['created_on'])
        task_closed = datetime.fromisoformat(task.closed_on)
        total_time += task_closed - task_assigned
        cnt += 1
    except Exception as e:
        pass
print(total_time / cnt)
