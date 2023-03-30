# Automatic Videography Ground Truth Constructor

This is a prototype application to build automatic videography ground truths for any audio sources. The system will also feature an automatic videography tool that programmatically generates a video consisting of timely imagery relevant to the textual information present in the audio.

Deployed here: https://automatic-videography.up.railway.app

[Python](https://www.python.org/downloads/) version `3.9.2` or later is required to run this application. To check what version you have run this command on a command line terminal:
```cmd
> python --version
```

## Installation
The following commands will show the steps to clone the repository. First navigate to a suitable workspace directory and run:
```cmd
> git clone https://github.com/StergiousAji/Autoamatic-Illustration-of-Text.git
> cd Automatic-Illustration-of-Text\src
```

Install the necessary packages from the `requirements.txt` file using the following command:
```cmd
> pip install -r requirements.txt
```

Finally, a **local**, static image collection must be present for this application to work correctly. There are many image datasets available from [ImageNet](https://www.image-net.org/download.php). Move this image collection into the Django project folder, `ground_truth_videography_project`.

**IMPORTANT:** You may need to change the `IMAGE_DATASET_DIR` path to point to your image collection in the [`settings.py`](https://github.com/StergiousAji/Automatic-Videography-Ground-Truth-Builder/blob/main/ground_truth_videography_project/ground_truth_videography_project/settings.py).

## Running
Once all the installation steps are completed, navigate into the Django project folder and run the following command to start a local instance of the web application:
```cmd
> cd Django\ground_truth_videography_project
> python manage.py runserver
```
