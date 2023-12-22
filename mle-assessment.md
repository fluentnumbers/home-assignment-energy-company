# Eneco - Machine Learning Engineer (MLE)

---

Date: 2023-12-15

The following exercises are designed to be a quick assessment of the candidates affinity with handling and analysing data as well as some general-purpose software/scripting tooling. Please find the most important guidelines below.

1. **It is expected that you will spend a maximum of 3-6 hours working on these exercises.** It is OK if you do not complete all exercises in this time. It is up to you on which exercises you spend your time and they can be completed in any order. We recommend you play to your strengths.

2. **The choice of tooling to conclude any of the exercises is up to the candidate.** There are no requirements regarding tools or techniques, use whatever you think will be a good fit. Please note that in this case it would be wise to favor fast/pragmatic results over rigid engineering. However, we may ask you about how your solution could be used in a production environment.

3. **You are requested to provide a summary write-up of your results.** If you have any code to share, please include that as well. Note that some assignments are intentionally vague. You're free to make any assumptions you think are necessary, but be prepared to defend the choices you made. 

4. **On the usage of (instruct) LLMs / ChatGPT**.
If you decide to use LLMs (e.g. `ChatGPT`, `Copilot`, `Bard`, `Mistral`), make sure to be transparent about it and include a comment or a section in your write-up explaining how you have used it. We are interested in your thought process and how you would approach the problem, not in the output of the LLMs (while they are very useful for prototyping!). If you would like to go the extra mile, you can provide the reproducibility parameters of the LLMs if available (e.g. `system_fingerprint`, `seed`, `temperature=0` and `model` (i.e. `gpt-4-1106-preview` ) for `ChatGPT`).

## 1. Productionise the training and inference of a model

### Scenario

You are the new, lone Machine Learning Engineer at an energy provider called *Oconé*. A data scientist in the company has handed this notebook (i.e. [model_toon.ipynb](https://sacodeassessment.blob.core.windows.net/public/model_toon.ipynb), with saved [models.zip](https://sacodeassessment.blob.core.windows.net/public/models.zip)) over to you. The notebook needs to be quickly put into production. 

Unfortunately, the data scientist in question has gone on holiday. This notebook is all you have to work with, there are no questions you can ask. Your tech lead is a terribly busy person, but luckily, they have left some instructions. 

You have limited time to complete the assignment, your schedule allows you 3-6 hours to work on this. A sticky situation. However, luck is that you can completely choose your own tooling for this work. 

Your tech lead expects you to complete the minimum requirements. However, to make a good impression on your first delivery, you might want to add a few more bells and whistles, than just these bare requirements. 

The extra tricks you possibly have up your sleeve can consist of any good practices in the field but are expected to fit within the boundaries of a coding repository. See the other files that are part of this section in the files paragraph.

### Instructions 
 
>Hi new Machine Learning Engineer, 
>
>Welcome aboard! For this solution I expect you to use best practices when deploying ML solutions. I trust your expertise and am giving you a free hand in how to set this up, but I would like you to at least include: 
>
>- Refactoring of the code
>- Some form of CI 
>- Containerization 
>
>
>Good luck and I will see you next week when I have time. I am looking forward to your solution! 
>
>Greetings, 
>
>Tech Lead

### Files

  - [model_toon.ipynb](https://sacodeassessment.blob.core.windows.net/public/model_toon.ipynb)
  - [models.zip](https://sacodeassessment.blob.core.windows.net/public/models.zip)
  - [data_set.csv](https://sacodeassessment.blob.core.windows.net/public/data_set.csv)
  - [column_info.csv](https://sacodeassessment.blob.core.windows.net/public/column_info.csv)

## 2. Acquire data from vendor API

Our supplier of high quality, curated country data no longer provides access to a file-based dataset (csv). Instead, they request you the gather this data through their next-generation data broker platform, in exchange for a detailed overview of revenues generated from this data.

a. Gather country data for every country, that has an airport (use [countries.csv](https://sacodeassessment.blob.core.windows.net/public/countries.csv)/[airports.csv](https://sacodeassessment.blob.core.windows.net/public/airports.csv) datasets), and store this in a single file. Which countries information is missing from the broker platform?

b. Upload an empty file named 'revenues.txt' to the upload endpoint (HTTP POST).

Details;
```
client id                   : abc123
host address                : code001.ecsbdp.com
HTTP path (get country info): /countries/{iso_code}
HTTP path (upload data)     : /revenues?client={client_id}
```

## 3. Halt excessive API usage

One of your colleagues, Bob, made an automatic collection script to retrieve data from a world-leading SaaS solution. However, the API usage is billed per call and expenses run rampant. The script needs to be stopped ASAP. Fortunately for Bob, but unfortunately for you, Bob is enjoying his holiday. All you know is that Bob's script runs somewhere on a server as a cron job.

Stop Bob's script! Although even better would be to just limit the frequence of his script to execute once every hour during office hours.

Also, find and retrieve the picture of Bob's cats.

Details;
```
server address   : 95.179.138.59
ssh port         : 22
user             : bob
password (of Bob): Bob@SuperS3cret
```
---
`539a214e74ceeb784dbe9aea78aca2f747a1b8ed`