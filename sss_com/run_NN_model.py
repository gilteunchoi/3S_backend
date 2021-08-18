from tensorflow.keras.models import Sequential, load_model

new_model = load_model("best_model.h5")
print(new_model.summary())

