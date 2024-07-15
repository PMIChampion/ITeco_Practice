from redminelib import Redmine
import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from io import BytesIO


neural = load_model('screenshot_classification_model.h5')

redmine = Redmine()

school_project = redmine.project.get('szi_arm_ispp')
limit = 50
offset = 0
image_size = (256, 256)
classes_of_pics = ['Continent', 'KSC', 'SNS']
issues_of_school_project = redmine.issue.filter(project_id=school_project.id)
num_of_task = int(input('Введите номер вашей задачи:'))

issue_for_func = redmine.issue.get(num_of_task)
result_dict = {}


def normalize_image(picture):
    img = image.load_img(BytesIO(picture), target_size=image_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


def test_of_pictures(for_check):
     issue = for_check
     if issue.attachments:
         for attachment in issue.attachments:
            picture = attachment.download()
            pic_content = picture.content
            name_of_picture = attachment.filename.split('.')

            if name_of_picture[1] not in ['png', 'jpg', 'jpeg', 'bmp']:
                continue
            img = normalize_image(pic_content)
            prediction = neural.predict(img)
            print(f"Изображение {attachment.filename} относится к типу {classes_of_pics[np.argmax(prediction)]}")
            result_dict[classes_of_pics[np.argmax(prediction)]] = attachment.filename


if len(result_dict) < 3:
    print("Проверьте, что все приложенные изображения относятся к разным программам!")


test_of_pictures(issue_for_func)
print(result_dict)
if len(result_dict) < 3:
    print("Проверьте, что все приложенные изображения относятся к разным программам!")




