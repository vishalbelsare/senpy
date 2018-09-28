from senpy import AnalysisPlugin, easy


class maxSentiment(AnalysisPlugin):
    '''Plugin to extract max emotion from a multi-empotion set'''
    author = '@dsuarezsouto'
    version = '0.1'

    extra_params = {
        'max': {
            "aliases": ["maximum", "max"],
            'required': True,
            'options': [True, False],
            "@id": 'maxSentiment',
            'default': False
        }
    }

    def analyse_entry(self, entry, params):
        if params["max"]==True:
            set_emotions= entry.emotions[0]['onyx:hasEmotion']  
            max_emotion =set_emotions[0]
         
            # Extract max emotion from the set emotions (emotion with highest intensity)
            for tmp_emotion in set_emotions:
                if tmp_emotion['onyx:hasEmotionIntensity']>max_emotion['onyx:hasEmotionIntensity']:
                    max_emotion=tmp_emotion

            if max_emotion['onyx:hasEmotionIntensity'] == 0:
                max_emotion['onyx:hasEmotionCategory'] = "neutral"
                max_emotion['onyx:hasEmotionIntensity'] = 1.0

            entry.emotions[0]['onyx:hasEmotion'] = [max_emotion]
            
            
            
        entry.emotions[0]['prov:wasGeneratedBy'] = "maxSentiment"
        #print(entry)
        yield entry
        


    
    # Test Cases:
    #   1º Normal Situation.
    #   2º Case to return a Neutral Emotion.
    test_cases = [{
        "entry": {
            "@id": "#",
            "@type": "entry",
            "emotions": [
                {
                    "@id": "Emotions0",
                    "@type": "emotionSet",
                    "onyx:hasEmotion": [
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "anger",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "joy",
                            "onyx:hasEmotionIntensity": 0.3333333333333333
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "negative-fear",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "sadness",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "disgust",
                            "onyx:hasEmotionIntensity": 0
                        }
                    ],
                    'prov:wasGeneratedBy':"maxSentiment_plugin"

                }
            ],
            "entities": [],
            "nif:isString": "This text makes me sad.\nwhilst this text makes me happy and surprised at the same time.\nI cannot believe it!",
            "sentiments": [],
            "suggestions": [],
            "topics": []

        },
        'params': {
            'max': True
        },
        'expected' : {
            "@id": "#",
            "@type": "entry",
            "emotions": [
                {
                    "@id": "Emotions0",
                    "@type": "emotionSet",
                    "onyx:hasEmotion": [
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "joy",
                            "onyx:hasEmotionIntensity": 0.3333333333333333
                        }
                    ]
                }
            ],
            "entities": [],
            "nif:isString": "This text makes me sad.\nwhilst this text makes me happy and surprised at the same time.\nI cannot believe it!",
            "sentiments": [],
            "suggestions": [],
            "topics": []
        }
    },
    {
        "entry": {
            "@id": "#",
            "@type": "entry",
            "emotions": [
                {
                    "@id": "Emotions0",
                    "@type": "emotionSet",
                    "onyx:hasEmotion": [
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "anger",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "joy",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "negative-fear",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "sadness",
                            "onyx:hasEmotionIntensity": 0
                        },
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "disgust",
                            "onyx:hasEmotionIntensity": 0
                        }
                    ],
                    'prov:wasGeneratedBy':"maxSentiment_plugin"

                }
            ],
            "entities": [],
            "nif:isString": "This text makes me sad.\nwhilst this text makes me happy and surprised at the same time.\nI cannot believe it!",
            "sentiments": [],
            "suggestions": [],
            "topics": []

        },
        'params': {
            'max': True
        },
        'expected' : {
            "@id": "#",
            "@type": "entry",
            "emotions": [
                {
                    "@id": "Emotions0",
                    "@type": "emotionSet",
                    "onyx:hasEmotion": [
                        {
                            "@id": "_:Emotion_1538121033.74",
                            "@type": "emotion",
                            "onyx:hasEmotionCategory": "neutral",
                            "onyx:hasEmotionIntensity": 1
                        }
                    ]
                }
            ],
            "entities": [],
            "nif:isString": "This text makes me sad.\nwhilst this text makes me happy and surprised at the same time.\nI cannot believe it!",
            "sentiments": [],
            "suggestions": [],
            "topics": []
        }
    
    }]


if __name__ == '__main__':
    easy()
