from EmoPy.src.fermodel import FERModel

models = []
models.append(FERModel(['happiness', 'anger'], verbose=True))
models.append(FERModel(['surprise', 'disgust', 'sadness'], verbose=True))
models.append(FERModel(['surprise', 'calm', 'disgust'], verbose=True))
models.append(FERModel(['disgust', 'fear', 'anger'], verbose=True))
models.append(FERModel(['happiness', 'calm', 'anger'], verbose=True))
models.append(FERModel(['calm', 'fear', 'anger'], verbose=True))
models.append(FERModel(['surprise', 'fear', 'anger'], verbose=True))
models.append(FERModel(['surprise', 'disgust', 'happiness'], verbose=True))
models.append(FERModel(['surprise', 'calm', 'fear', 'anger'], verbose=True))


