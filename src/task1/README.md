# Task 1

## Productionise the training and inference of a model

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

## How-to

### Prerequisites

- A virtual Python3.10 environment. For instance, using `pipenv install` in the project root
- Rename `.env_template` to `.env`

### Run as a local script

Run [task1.py](./task1.py): `python src/task1/task1.py`

### Deploy in a Docker container

- Build and run the container:

```bash
cd src/task1
docker build . --tag task1
docker run -p 5000:5000 task1
```

- Access the FastAPI on the host: <http://localhost:5000>
- Manually test the container on a given dataset: `python src/task1/test_app.py`

## Results

Given Jupyter notebook is productionalized following best practices

### Implemented

#### :heavy_check_mark: Primary functionality

- Refactored codebase with functionality to load, preprocess data, run latest model to batch predict
- CI workflow: [workflow.yaml](../../.github/workflows/workflow.yaml)
- FastAPI [app.py](./app.py) to create an endpoint for predict_batch()
- [Dockerfile](./Dockerfile) to containerize the app

#### :heavy_check_mark: Secondary functionality

- OOP-based solution: Predictor() class
- CI includes static linting, unit-testing, but also integration and deployment tests
- [pre-commit-hooks](../../.pre-commit-config.yaml)
- logging
- FastAPI app [status endpoints](./tools/state.py)
- unittests stub: [test_tasks.py](../../tests/test_tasks.py)

#### ⬜ TODO ideas

- Makefile
- FIXME: /predict endpoint for single datapoint predictions (nan-filling fails with all-nans in a column)
- FIXME: nan-values are not json-serializable
- Pydantic models with type-checking in-place
