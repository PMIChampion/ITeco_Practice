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
image_size = (256, 256)
classes_of_pics = ['Continent', 'KSC', 'SNS']
issues_of_school_project = redmine.issue.filter(project_id=school_project.id)

num_of_task = int(input('Введите номер вашей задачи:'))

issue_for_func = redmine.issue.get(num_of_task)
result_dict = {}


def normalize_image(picture):
    """
    Эта функция принимает на вход метаданные изображения (requests.Response), преобразует байтовое содержимое в
    обьект PIL.Image и нормализует его.
    """
    img = image.load_img(BytesIO(picture), target_size=image_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


def test_of_pictures(picture):
    """
    Эта функция принимает на вход загруженное с сервера изображение(request.Response) и возвращает словарь,
    в котором определяется к какому типу относится изображение.
    """
    pic_content = picture.content

    img = normalize_image(pic_content)
    prediction = neural.predict(img)
    print(f"Изображение относится к типу {classes_of_pics[np.argmax(prediction)]}")


for attachment in issue_for_func.attachments:
    picture = attachment.download()
    if attachment.filename.split('.')[1] not in ['png', 'jpg', 'jpeg', 'bmp']:
        continue
    test_of_pictures(picture)