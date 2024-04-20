import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, storage
from tensorflow.keras import datasets, layers, models

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class CNNUploader(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.btn = Button(text='Upload CNN Model', on_press=self.upload_model)
        layout.add_widget(self.btn)
        return layout

    def upload_model(self, instance):
        # Initialize Firebase Admin SDK (replace 'path/to/serviceAccountKey.json' with your service account key file)
        cred = credentials.Certificate("./image-recog-aaf2b-firebase-adminsdk-9d4o6-6207255a80.json")
        firebase_admin.initialize_app(cred, {'storageBucket': 'image-recog-aaf2b.appspot.com'})

        # Load CIFAR-10 dataset
        (training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
        training_images, testing_images = training_images / 255, testing_images / 255

        # Limit dataset size
        training_images = training_images[:20000]
        training_labels = training_labels[:20000]
        testing_images = testing_images[:4000]
        testing_labels = testing_labels[:4000]

        # Define and compile the CNN model
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(64, (3,3), activation='relu'))
        model.add(layers.MaxPooling2D((2,2)))
        model.add(layers.Conv2D(64, (3,3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))

        # Evaluate the model
        loss, accuracy = model.evaluate(testing_images, testing_labels)
        print(f"Loss: {loss}")
        print(f"Accuracy: {accuracy}")

        # Save the trained model
        model_file_path = 'image_classifier.keras'
        model.save(model_file_path)
        print("Model saved.")

        # Upload the model file to Firebase Storage (replace 'path/to/firebase/model/image_classifier.keras' with desired filepath)
        firebase_storage_path = 'model/image_classifier.keras'
        bucket = storage.bucket()
        blob = bucket.blob(firebase_storage_path)
        blob.upload_from_filename(model_file_path)

        print("Model uploaded to Firebase Storage.")

if __name__ == '__main__':
    CNNUploader().run()
