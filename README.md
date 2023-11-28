# Parallel functon calling in Azure OpenAI GPT-4-Turbo, with a companion Web API app.

Version 1106 of Azure OpenAI GPT models, such as GPT-35-Turbo and GPT-4-Turbo, now supports the use of parallel function calling. This new feature allows your Azure OpenAI based solution to extract multiple intents from a single prompt, check the functions available and then execute them in parallel. As a result, your solution will perform more effectively and efficiently because of a shorter round-trips between required multiple API calls.

In this repo I'll demo the use of the latest openai Python package v1.x, that was released in November 2023. To use the latest version of *openai* python package, please upgrade it with the following pip command:
```
pip install --upgrade openai
```

Additionally, to help with the practical test of API calls, I provide a companion Web app in Flask to expose in-car API endpoints of a fictitious automotive company. Detailed instructions on the Web app activation and the use of provided Jupyter notebooks are provided below.

## Table of contents:
- [Step 1: Configuring Flask Web app]()
- [Step 2: Configuring Azure OpenAI environment]()
- [Step 3: End-to-end testing of parallel function calling]()

## Step 1: Configuring Flask Web app

## Step 2: Configuring Azure OpenAI environment

## Step 3: End-to-end testing of parallel function calling
