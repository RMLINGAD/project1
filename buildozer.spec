[app]

# (str) Title of your application
title = CNNUploader

# (str) Package name
package.name = cnnuploader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (list) Application requirements
requirements = python3,kivy,opencv-python-headless,numpy,matplotlib,firebase-admin,tensorflow

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (str) Android app orientation (landscape, portrait or all)
orientation = portrait

# (int) Target Android API
android.api = 29

# (int) Minimum API your APK will support
android.minapi = 21

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE
