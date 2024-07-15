from redminelib import Redmine
import os


attachment_cattegories = {
    'KSC.png': 'images/KSC',
    'sns.png': 'images/SNS',
    'Континент.png': 'images/Континент'
}

redmine = Redmine()
issues = redmine.issue.all()
cnt_ksc = 0
limit = 50
offset = 0
schools = redmine.project.get('szi_arm_ispp')
example = ''
cnt_sns = 0
cnt_continent = 0
cnt_trash = 0
while True:
    issues_of_schools = redmine.issue.filter(project_id=schools.id, limit=limit, status_id=15, offset=offset)
    for task in issues_of_schools:
        if task.attachments:
            for picture in task.attachments:
                name_of_picture = picture.filename.split('.')
                if name_of_picture[0] in 'KESKSCkesksckasperKASPER':
                    save_path = '../pythonProject7/images/KSC/'
                    picture.download(savepath=save_path)
                    os.rename(save_path + f'{picture.filename}', save_path + f'{cnt_ksc}.png')
                    cnt_ksc += 1
                if name_of_picture[0] in 'SNSsns':
                    save_path = '../pythonProject7/images/SNS/'
                    picture.download(savepath=save_path)
                    os.rename(save_path + f'{picture.filename}', save_path + f'{cnt_sns}.png')
                    cnt_sns += 1
                if name_of_picture[0] in 'Continentcontinent':
                    save_path = '../pythonProject7/images/Континент/'
                    picture.download(savepath=save_path)
                    os.rename(save_path + f'{picture.filename}', save_path + f'{cnt_continent}.png')
                    cnt_continent += 1
                else:
                    name_of_file = picture.filename.split('.')
                    if name_of_file[1] == 'pdf':
                        continue
                    save_path = '../pythonProject7/images/мусор/'
                    picture.download(savepath=save_path)

                    cnt_trash += 1
    offset += limit

    if cnt_ksc == 2000 or cnt_sns == 2000 or cnt_continent == 2000:
        break