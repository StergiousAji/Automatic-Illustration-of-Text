# Meeting Notes

## **Automatic Illustration of Text via Multimodal Interaction**
* Stergious Aji
* 2546916A
* **Supervisor:** Debasis Ganguly

<br />

## Meeting 1 (13/10/22) - 0:28

- Use [Wikimedia](https://commons.wikimedia.org/wiki/Main_Page) database as has captions
- Pre-trained model Clip (Image and text embeddings)
- [ecir2023.org](http://ecir2023.org/) - Reformat Demo Paper and submit on October 22, 2022
    - [Demo Paper Overleaf](https://www.overleaf.com/project/6349947a99d6902905460a9b)
- Read previous thesis


## Meeting 2 (20/10/22) - 0:15

- Use static image collection and index it
- Limitations with current thesis
    - APIs change
- Better Evaluation
    - Similarity to semantically relevant images
- https://github.com/openai/CLIP - supervised database encoding text prompts to images.
- **Next Week:** 10 slides explaining the thesis and what I can extend


## Meeting 3 (03/11/22) - 0:30

- Download Wikimedia collection.  ([How To](https://how-to.fandom.com/wiki/How_to_download_all_image_files_in_a_Wikimedia_Commons_page_or_directory)?)
- Download random 5 images for each category from ImageNet
- Image indexing by caption locally. https://github.com/gdebasis/luc4ir
- Read Intro to IR [https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf](https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf)
- Don’t use YAKE!!


## Meeting 4 (10/11/22) - 0:28

- USE WIKIMEDIA
    - [WIT Image-Text Dataset](https://ai.googleblog.com/2021/09/announcing-wit-wikipedia-based-image.html) :  
        [https://github.com/google-research-datasets/wit](https://github.com/google-research-datasets/wit)
    
    - [WIT Hugging Face Guide](https://huggingface.co/datasets/google/wit)
- Retrieve from a dense index representation of image vectors
    - sparse index of text
- PyTerrier: [https://github.com/terrier-org/pyterrier](https://github.com/terrier-org/pyterrier)


## Meeting 5 (17/11/22) - 0:16

- Go to Alwyn’s Building Room M111 next week
- Look into vectorising images with CLIP
- Somehow transform query to some image-caption to text vector form and retrieve relevant image
- Read on multimodal paper (Dataset looks interesting…)
    
    https://gla-my.sharepoint.com/:b:/g/personal/debasis_ganguly_glasgow_ac_uk/EW_0koAdFntCg-ci0RnO55wBGRjBRS2iKD6BG3lC8yBFPA
    
    - **MobileNetV2 (Embed Images to Vectors)**:
        
        *Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, and Liang-Chieh Chen. 2018. Mobilenetv2: Inverted residuals and linear bottlenecks. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 4510–4520.*
        

## Meeting 6 (24/11/22) - 0:30

- Problem with user surveys: subjective, every time system is changed need to do user survey again.
- Build a system to generate a ground truth (True Labels)
- Input video/audio → divide into chunks → for each chunk let user query/select relevant image from a set → build the ground truth video.
- Build a Gantt chart


## Meeting 7 (01/12/22) - 0:30

- Vectorise images using captions
- Combine text and images vectors
- Select 25 songs to build ground truth
- Ground truth not a video will be data
- Work on any mp3 file not just YouTube URL??
- Status Report


## Meeting 8 (12/01/23) - 0:30

- Improve similarity search efficiency using Facebook’s FAISS
- Reread and resolve reviewers’ issues to submit camera-ready paper (ECIR23)


## Meeting 9 (19/01/23) - 0:30

- FAISS may not be helpful when creating ground truth as accuracy is important
- Add text/lyrics to the video generation
- Think about evaluation and surveying


## Meeting 10 (26/01/23) - 0:30

- Get Jaccard overlaps between FAISS retrieved images vs. exhaustive
- Show runtimes
- Change videography to get top image not random.
- Make backend to get metrics between ground truth and videography images.
    - Possible metrics: P@1, MRR, nDCG, AP

## Meeting 11 (02/02/23) - 0:35

- Look into and start writing for SIGIR23 call for papers.
- Showed FAISS analysis and concluded that it was not needed. Exhaustive is fast enough.
- Possibly add ground truth building percentage done in collections page.

## Meeting 12 (09/02/23) 0:30

- Focus te SIGIR paper from annotators perspective and change system architecture diagram.
- Lookin into Query expansion for alternative system to evaluate.
- Captionise images for text-to-text querying as alternative system to evaluate.
- Change the diagram in the SIGIR to a PDF format.
- Provide an illustrated walkthrough of an annotation task in SIGIR paper.

## Meeting 13 (23/02/23) - 0:30

- Asked supervisor to sign Ethics Checklist for usability evaluations with other participants.
- Read ‘Variable Depth Pooling’ paper and write a literature review for the dissertation.
- Research into other annotation interfaces to contrast with our own.
- Rewrite Introduction and motivations in dissertation according to notes

## Meeting 14 (02/03/23) - 0:25

- Talk about the variable depth pooling as a specific avenue to pooling (old method).
- Talk about new idea of active learning vs. pooling.
- Talk about FAISS as separate system and how it didn’t have any overlap with current system.
- Always ask why did I do it this way, contextualise everything.
- CLIP uses mutlimodal transformers, early days used static word and image vectors and alignment (NIPS paper).
- Deploy web app to work on static song collections ([Railway](https://railway.app/)).