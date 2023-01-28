# Time Log
## **Automatic Illustration of Text**
* 2546916A - Stergious Aji
* **Supervisor:** Debasis Ganguly

## 13/10/22
* 0.5 hrs - Researching multimodal interactions and text to image generation/retrieval
* 0.1 hrs - Prepare for first meeting
* 0.5 hrs - Supervisor meeting

## 16/10/22
* 1 hr - Reading and reformatting demo paper on overleaf to LLNCS format
* 2 hrs - Rewriting and shortening of demo paper to fit page limit

## 19/10/22
* 1 hr - Further rewriting demo paper for submission

## 20/10/22
* 0.5 hrs - Supervisor meeting
* 1 hr - Researching Wikimedia and Clip

## 22/10/22
* 3 hrs - Reading previous dissertation thoroughly and summarising (Stopped at System Design)
* 0.25 hrs - Setting up a GitHub Repository

## 23/10/22
* 3 hrs - Further reading of dissertation and summarising (Stopped at Evaluation)

## 24/10/22
* 2 hrs - Final reading of dissertation and summarising (Evaluation and Conclusion)
* 3 hrs - Researching Forced Alignment, Genius and Shazam APIs
* 3 hrs - Creating small program that uses Shazam and Genius APIs to recognise and retrieve lyrics of a song in Python

## 25/10/22
* 3 hrs - Creating 10 slides for small presentation of previous dissertation and initial ideas
* 2 hrs - Researching ideas for project plan
  
## 27/10/22
* 2 hrs - Pushing finished script to download YouTube video, recognise song and retrieve lyrics to GitHub repo
* 1 hr - Researching possible ImageNet implementation
  
## 29/10/22
* 2 hrs - Downloading tiny-imagenet-200 dataset to experiment with

## 30/10/22
* 2 hrs - Creating a small jupyter notebook script to query tiny-imagenet-200 dataset from keywords.

## 02/11/22
* 1 hr - Repreparing the small presentation as meeting missed last week

## 03/11/22
* 0.5 hrs - Supervisor meeting with initial project plan presentation
* 2 hrs - Researching ways to download Wikimedia Commons Collection
* 2 hrs - Reading "Introduction to IR" as suggested from meeting, particularly on indexing

## 04/11/22
* 4 hrs - Creating a jupyter notebook script to programmatically download 5 random images for each ImageNet synset (category)

## 05/11/22
* 4 hrs - Continuing work on downloading real ImageNet collection and fixing bugs

## 06/11/22
* 2 hrs - Researching 'luc4ir' for indexing as suggested at previous meeting
  
## 08/11/22
* 5 hrs - Running created script to download real ImageNet programmatically

## 09/11/22
* 6 hrs - Continuing to run script (10% of database downloaded at the end of day).

## 10/11/22
* 0.5 hrs - Supervisor meeting
* 2 hrs - Researching Wikipedia Image-Text Dataset (WIT)
  
## 11/11/22
* 3 hrs - Cloning the 'luc4ir' repo to understand how it works
* 2 hrs - Researching retrieval of dense index representations

## 14/11/22
* 2 hrs - Researching pyterrier as suggested from previous meeting

## 17/11/22
* 0.5 hrs - Supervisor meeting (in-person)
* 1 hr - Researching CLIP for image vectorisation
  
## 20/11/22
* 3 hrs - Reading suggested multimodal research paper
* 1 hr - Researching MobileNetV2 to embed images to vectors (from above paper)
  
## 24/11/22
* 0.5 hrs - Supervisor meeting

## 26/11/22
* 2 hrs - Building Gantt chart to plan out work

## 01/12/22
* 0.5 hrs - Supervisor meeting

## 10/11/22
* 2 hrs - Researching image vectorisation using CLIP and implementing it
* 3 hrs - Making initial Django Webapp

## 11/11/22
* 2 hrs - Researcing and registering musixmatch api to pipeline to get synced lyrics
  
## 12/12/22
* 3 hrs - Writing intial draft of status report

## 18/12/22
* 3 hrs - Making and desinging the Home page of webapp
* 4 hrs - Working on input YouTube URL and upload file functionality
  
## 19/12/22
* 3 hrs - Making a script that gets synced lyric transcripts from Musixmatch
* 3 hrs - Designing the Audio page showing result of song recogniser and lyrics retriever
* 9 hrs - Downloading WIT images in batches (Stopped at 2k images since was taking too long)
  
## 20/12/22
* 2 hrs - Making backend Django models for Audio tracks and Chunks
* 3 hrs - Adding functionality to select a chunk within audio transcript
* 2 hrs - Designing Chunk page that will show chunk text and top 10 images

## 21/12/22
* 3 hrs - Making a script to embed images using pre-trained CLIP model
* 3 hrs - Testing running script to process imagenette dataset from HuggingFace and evaluating its performance

## 22/12/22
* 4 hrs - Designing and adding top ten images to Chunk pages
* 1 hr - Adding functionality to navigate the Audio chunks
* 8 hrs - Downloading ImageNet-1k dataset
  
## 23/12/22
* 7 hrs - Running script to process ImageNet-1k test (Size: 100k) and validation images (Size: 50k) and saving in .npy files
* 3 hrs - Testing performance of validation vs. test images at retrieving best images

## 26/12/22
* 14 hrs - Running script to process ImageNet-1k train images (Size: 1.2M) and saving in .npy file
* 2 hrs - Testing performance of train images at retrieving best images

## 27/12/22
* 2 hrs - Adding form validation in Home page for inputting YouTube URL and file upload
* 4 hrs - Redesigning Audio page, now showing coverart, song title and artist.

## 28/12/22
* 3 hrs - Adding coverart primary colour identifier to show in pages, make webapp more dynamic

## 04/01/23
* 1 hr - Added video generation functionality to the Audio page
* 3 hrs - Making videography script to create video with Moviepy by getting a random top 10 image for each audio chunk

## 10/01/23
* 2 hrs - Designing and finishing the Collections page showing all audio tracks stored in database
* 2 hrs - Designing and finishing the About page