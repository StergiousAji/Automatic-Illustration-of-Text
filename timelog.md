# Time Log
## **Automatic Illustration of Text via Multimodal Interaction**
* Stergious Aji
* 2546916A
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
* 2 hrs - Creating a small jupyter notebook script to query tiny-imagenet-200 dataset with keywords.

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

## 12/01/23
* 0.5 hr - Supervisor meeting
* 1 hrs - Reading reviewers' issues with the ECIR23 demonstration paper submission
* 1 hr - Resolving issues and rewriting parts of paper for camera-ready submission

## 14/01/23
* 2 hrs - Researching FAISS for fast similarity searching
* 1 hr - Implementing small script with FAISS

## 17/01/23
* 5 hrs - Added new features to project: Multi-lingual CLIP, Timestamp information in Chunk pages, Dynamic image checkboxes and completed ground truth building process

## 19/01/23
* 0.5 hr - Supervisor meeting
* 1 hr - Researching adding text to video generation

## 21/01/23
* 3 hrs - Implemented YouTube caption extraction to the videography pipeline

## 23/01/23
* 5 hrs - Added text/lyrics to the video generation pipeline
* 1 hr - Improved caption conversion to LRC format

## 25/01/23
* 5 hrs - Added more features: Added Download button to Ground Truth page, Fixed audio model updating bug, and made links more intuitive

## 26/01/23
* 0.5 hr - Supervisor meeting
* 2 hrs - Added OpenAI's Whisper Audio-to-Text Transcription as a backup

## 28/01/23
* 1 hr - Added flag to support both English-only and Multi-lingual CLIP models
* 1 hr - Added selected image ids and paths to ground truth data
* 4 hrs - Starting to write Introduction of dissertation

## 30/01/23
* 2 hrs - Restructured GitHub Project Structure to match template
* 3 hrs - Building mulitple FAISS indexes with different parameter settings and analysing results against exhaustive searching (Jaccard Similarities and Runtimes)

## 31/01/23
* 3 hrs - Added functionality to save selected images for all chunks with repeating texts.
* 2 hrs - Creating Usability survey evaluation forms
* 2 hrs - Performing PCA to reduce dimensions for FAISS indexing

## 02/02/23
* 0.5 hr - Supervisor meeting
* 0.5 hr - Researching SIGIR paper submission deadlines

## 03/02/23
* 4 hrs - Performed bug fixes: Fixed image indexes not saving bug, final ground truth building bug, abstracted the ground truth building code to its own file

## 06/02/23
* 4 hrs - Writing Analysis/Requirements of dissertation
* 1 hr - Added functionality to directly view previously created ground truths

## 07/02/23
* 2 hrs - Listing and prioritising the requirements of the project formally
* 2 hrs - Writing up User stories for Requirements section of dissertation
* 3 hrs - Writing introduction and designing system architecture diagram for SIGIR paper

## 09/02/23
* 0.5 hr - Supervisor meeting
* 1 hr - Researching Query Expansion and captionising images for text-to-text querying

## 13/02/23
* 2 hrs - Redesigning system architecture diagram from annotator's perspective for SIGIR paper
* 2 hrs - Writing Implementation details in SIGIR paper

## 14/02/23
* 3 hrs - Writing illustrated walkthrough of annotation task for SIGIR paper
* 2 hrs - Writing Conclusion and Future Work for SIGIR paper

## 20/02/23
* 3 hrs - Writing up list of MOSCOW prioritised requirements in dissertation
* 1.5 hrs - Conducting usability evaluation with four participants
* 3 hrs - Rewriting SIGIR paper as per notes from supervisor

## 21/02/23
* 2 hrs - Conducting usability evaluation with six participants
* 2 hrs - Starting to write Background chapter of dissertation

## 23/02/23
* 0.5 hr - Supervisor meeting
* 2 hrs - Reading and summarising Variable Depth Pooling paper

## 25/02/23
* 2 hrs - Researching and taking notes on other annotation interfaces

## 26/02/23
* 4 hrs - Rewriting Introduction and motivations in dissertation

## 27/02/23
* 4 hrs - Writing Background chapter introduction and begining literature review of Variable Depth Pooling paper

## 28/02/23
* 2 hrs - Performing 4 more user evaluations and validating completed ground-truths
* 1 hr - Making system architecture diagrams for the Transcription Extractor and Annotation Interface

## 02/03/23
* 0.5 hr - Supervisor meeting
* 2 hrs - Reading OpenAI paper on CLIP
* 2 hrs - Researching papers for Image Retrieval History

## 04/03/23
* 3 hrs - Writing history of image retrieval within IR (BACKGROUND)

## 05/03/23
* 3 hrs - Writing history of relevance assessment within IR (BACKGROUND)

## 06/03/23
* 3 hrs - Writing analysis of previous thesis (BACKGROUND)
* 2 hrs - Researching and writing existing annotation tools: Labelbox and SuperAnnotate (BACKGROUND)

## 07/03/23
* 3 hrs - Finishing Background chapter and writing summaries
* 3 hrs - Creating wireframes for Design chapter

## 08/03/23
* 3 hrs - Proof-reading Introduction and Background chapters
* 3 hrs - Writing User Interface Design section (DESIGN)

## 09/03/23
* 4 hrs - Writing about Audio page, Chunk page, Video page and Ground-Truth page (DESIGN)
* 2 hrs - Writing summaries for Requirements and Design chapters

## 10/03/23
* 3 hrs - Writing three more sections (IMPLEMENTATION)
* 2 hrs - Adding try-catch to fix ImageMagick bug

## 11/03/23
* 3 hrs - Writing more sections (IMPLEMENTATION)
* 2 hrs - Fixing multilingual conditional bug

## 12/03/23
* 3 hrs - Finishing Implementation chapter
* 3 hrs - Listing MoSCoW requirements (REQUIREMENTS/ANALYSIS)

## 13/03/23
* 4 hrs - Creating/Running video generation time experiment on current system (EVALUATION)
* 2 hrs - Performed 4 more user evaluations

## 14/03/23
* 4 hrs - Running video generation time experiment on previous system (EVALUATION)
* 2 hrs - Adding results to Appendix

## 15/03/23
* 2 hrs - Adding signed Ethics Checklist to Appendix
* 2 hrs - Creating tables and adding figures for FAISS experiment

## 16/03/23
* 3 hrs - Completing Requirement Fulfillment section (EVALUATION)

## 17/03/23
* 3 hrs - Adding usability evaluation and writing about results (EVALUATION)
* 2 hrs - Adding usability results and survey to Appendix

## 18/03/23
* 3 hrs - Finishing Evaluation summary and starting final chapter (CONCLUSIONS)

## 19/03/23
* 2 hrs - Writing Reflection and Future Work sections (CONCLUSTIONS)
* 4 hrs - Creating graphs using matplotlib for experiments

## 20/03/23
* 4 hrs - Finishing dissertation and proof-reading up to Evaluation 6.1.2

## 21/03/23
* 4 hrs - Adding application walkthrough to Appendix
* 2 hrs - Proof-reading rest of dissertation

## 23/03/23
* 2 hrs - Creating presentation slides
* 2 hrs - Spellchecking dissertation
* 1 hr - Working on deploying website with Railway

## 24/03/23
* 2 hrs - Checking timelog and repository structure
* 3 hrs - Further work on deploying website