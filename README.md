[![buddy pipeline](https://app.buddy.works/rohitjain00/fatburn/pipelines/pipeline/141212/badge.svg?token=12a288850ff10ce4a9786d411f40bd0933f81d9a662591f5b63c30e61f461cf1 "buddy pipeline")](https://app.buddy.works/rohitjain00/fatburn/pipelines/pipeline/141212)
[![CodeFactor](https://www.codefactor.io/repository/github/rohitjain00/fatburn/badge)](https://www.codefactor.io/repository/github/rohitjain00/fatburn)
[![Maintainability](https://api.codeclimate.com/v1/badges/601612fa95c7ef64dd68/maintainability)](https://codeclimate.com/github/rohitjain00/FatBurn/maintainability)
# FatBurn
Fitness based web application

We have created a web app to track our day to day life activities and helps us to lose weight in no time.In this app, we can add our day to day activities and further provides information and all possible Indexes possible.We can find a gym nearby and get involved in its workout plans and also for the sake of traditions we have added a special feature "Yoga" which plays a mind relaxing tune to help you build your mental as well as physical fitness.It shows you the total steps walked and total calories burned as a log i.e A complete history is saved of the person's entered data.

Video Representation : https://vimeo.com/250457962
<br>
Presentation : https://he-s3.s3.amazonaws.com/media/sprint/bobs-build-a-thon/team/316576/d4e8f26photo_album__2_.pptx
<br>
Created for Hackathon (https://www.hackerearth.com/sprints/bobs-build-a-thon/)

<img src = "https://he-s3.s3.amazonaws.com/media/sprint/bobs-build-a-thon/team/316576/798defchomepage.png" height = 450 width = 800)/>

<img src = "https://he-s3.s3.amazonaws.com/media/sprint/bobs-build-a-thon/team/316576/807eed7map.png" height = 450 width = 800)/>

<img src = "https://he-s3.s3.amazonaws.com/media/sprint/bobs-build-a-thon/team/316576/898977fyoga.png" height = 450 width = 800)/>

<img src = "https://he-s3.s3.amazonaws.com/media/sprint/bobs-build-a-thon/team/316576/b689074exercise.png" height = 450 width = 800)/>

# Setup Development Environment

1. This project is created using Python (Flask)

2. Create a virtual environment:
  ```sh
  $ python3 -m venv venv
  ```
3. Activate the virtual environment:
  - On Windows:
    ```sh
    $ venv\Scripts\activate
    ```
  - On macOS and Linux:
    ```sh
    $ source venv/bin/activate
    ```
4. Install all dependencies required:
  ```sh
  $ pip install -r requirements.txt
  ```
5. To run the application, you can either use the `flask` command or Python’s `-m` switch with Flask. Before you can do that, you need to tell your terminal the application to work with by exporting the `FLASK_APP` environment variable:
  ```sh
  $ export FLASK_APP=application.py
  $ flask run
  ```
  * Running on `127.0.0.*:\****`
6. If running the application for the first time, create the schema by running:
  ```sh
  $ python create_schema.py
  ```
7. Go to `127.0.0.*:\****` to see your application running.

# Running with Docker

1. Build the Docker image:
  ```sh
  $ docker-compose build
  ```

2. Run the Docker container:
  ```sh
  $ docker-compose up
  ```

3. Go to `http://localhost:5000` to see your application running.