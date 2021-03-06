import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='34ffa0b3ed9064b202665412651232828bdbd8c0')

def isSky(image):
    with open(image, 'rb') as image_file:
        visual_recognition_result = visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['SkyDetection_1096606956'])
        score_info = visual_recognition_result['images'][0]['classifiers'][0]['classes']
        ad = 0
        sky = 0
        for score in score_info:
            if score['class'] == 'ad':
                ad = score['score']
            else:
                sky = score['score']
        if ad < 0.1 and sky > 0.4:
            return True
        else:
            return False