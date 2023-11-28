# Parallel functon calling in GPT-4-Turbo, with a companion Web API site

Version 1106 of Azure OpenAI GPT models, like GPT-35-Turbo and GPT-4-Turbo, now supports the use of parallel function calling. This new feature allows your Azure OpenAI based solution to extract multiple intents from a single prompt, check what functions are available and then execute them in parallel. As a result, your solution will perform more efficiently because of shorter round-trips between required API calls.

In this repo I'll demo the use of the latest openai Python package v1.x, that was released in November 2023. To use the latest version of *openai* python package, please upgrade it with the following pip command:
```
pip install --upgrade openai
```

Additionally, to help with the test of API calls, I built a companion Web app in Flask to expose in-car API endpoints of a fictitious automotive company. Detailed instructions on the Web app activation and the use of provided Jupyter notebooks are provided below.

## Table of contents:
- [Scenario 1: Authenticating with API Key]()
- [Scenario 2: Authenticating with Entra ID - Interactive Login]()
- [Scenario 3: Authenticating with Entra ID - Service Principal]()

