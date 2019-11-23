from EmoPy.src.fermodel import FERModel

models = []
models.append(FERModel(['happiness', 'anger'], verbose=True))
models.append(FERModel(['surprise', 'disgust', 'sadness'], verbose=True))
models.append(FERModel(['surprise', 'disgust', 'happiness'], verbose=True))


