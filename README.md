# Parallel functon calling in Azure OpenAI GPT-4-Turbo, with a companion Web API app.

Version 1106 of Azure OpenAI GPT models, such as GPT-35-Turbo and GPT-4-Turbo, now supports the use of parallel function calling. This new feature allows your Azure OpenAI based solution to extract multiple intents from a single prompt, check the functions available and then execute them in parallel. As a result, your solution will perform more effectively and efficiently because of fewer round-trips between required multiple API calls.

In this repo I'll demo the use of the latest *openai* Python package v1.x, that was released in November 2023. To upgrade your *openai* python package, please use the following pip command:
```
pip install --upgrade openai
```

Additionally, to help with the practical test of API calls, I provided a companion Web app in Flask to expose in-car API endpoints of a fictitious automotive company. Detailed steps on the Web app setup and the use of provided Jupyter notebook are described below.

## Table of contents:
- [Step 1: Configuring Flask Web app](https://github.com/LazaUK/AOAI-ParallelFunctionCalling-SDKv1#step-1-configuring-flask-web-app)
- [Step 2: Configuring Azure OpenAI environment](https://github.com/LazaUK/AOAI-ParallelFunctionCalling-SDKv1#step-2-configuring-azure-openai-environment)
- [Step 3: End-to-end testing of parallel function calling](https://github.com/LazaUK/AOAI-ParallelFunctionCalling-SDKv1#step-3-end-to-end-testing-of-parallel-function-calling)

## Step 1: Configuring Flask Web app
1. Add a new environment variable named **FLASK_APP** that points to the provided *Vehicle_API_Simulations.py* Python script.
![screenshot_1.1_environment](images/step1_flask_env.png)
2. Install required Python packages, by using pip command and provided requirements.txt file.
```
pip install -r requirements.txt
```
3. Start Flask Web app from the repo's root folder:
```
python -m flask run
```
4. You should be able to access its home page at http://localhost:5000/
![screenshot_1.2_webapp](images/step1_flask_app.png)
5. As described on the home page, this Web app exposes the following 5 API endpoints of a fictitious vehicle's in-car controls:
   - GET endpoint at http://localhost:5000/status to get the latest **status** of each vehicle control;
   - POST endpoint at http://localhost:5000/airconditioner to switch the **air conditioner** on / off;
   - POST endpoint at http://localhost:5000/lights to switch the **lights** on / off;
   - POST endpoint at http://localhost:5000/radio to switch the **radio** on / off;
   - POST endpoint at http://localhost:5000/windows to roll the **windows** up / down.

6. The Status endpoint returns key/value pairs for all 4 controls in JSON format.
``` JSON
{'airconditioner': 'OFF', 'lights': 'OFF', 'radio': 'OFF', 'windows': 'DOWN'}
```
7. The POST endpoints expect you to add a **Content-Type** header, set to **application/json**.
``` JSON
{"Content-Type": "application/json"}
```
8. Air Conditioner, Lights and Radio endpoints require a body payload, which accepts **ON** and **OFF** values for its *switch* key.
``` JSON
{"switch": "ON"}
```
9. Windows endpoint also requires a body payload, although it accepts **UP** and **DOWN** values for its *roll* key. 
``` JSON
{"roll": "DOWN"}
```

## Step 2: Configuring Azure OpenAI environment
1. Assign Azure OpenAI API endpoint name, version and key, along with the Azure OpenAI deployment name of GPT-4-Turbo model to **OPENAI_API_BASE**, **OPENAI_API_VERSION**, **OPENAI_API_KEY** and **OPENAI_API_DEPLOY** environment variables.
![screenshot_2.1_environment](images/step2_aoai_env.png)
2. An AzureOpenAI client will be instantiated with retrieved environment variables.
``` Python
client = AzureOpenAI(
    azure_endpoint = os.getenv("OPENAI_API_BASE"),
    api_key = os.getenv("OPENAI_API_KEY"),
    api_version = os.getenv("OPENAI_API_VERSION")
)
```
3. GPT-4-Turbo model will be called twice:
- to analyse the original prompt and decide which functions to use.
``` Python
response = client.chat.completions.create(
    model = os.getenv("OPENAI_API_DEPLOY"),
    messages = messages,
    tools = tools,
    tool_choice = "auto"
)
```
- and then again later to process data retrieved from API endpoints and send its final completion back to the client.
``` Python
second_response = client.chat.completions.create(
    model = os.getenv("OPENAI_API_DEPLOY"),
    messages=messages
)
```

## Step 3: End-to-end testing of parallel function calling
1. The set of available functions is described in the **tools** list. Each function's description will provide a hint to the GPT model on its capabilities, while the list of its properties will be used to match with the prompt's entities. 
``` Python
tools = [
    {
        "type": "function",
        "function": {
            "name": "set_vehicle_feature_on_off",
            "description": "Set or switch features like air conditioner, lights and radio on or off",
            "parameters": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "string",
                        "enum": ["airconditioner", "lights", "radio"]
                    },
                    "status": {
                        "type": "string",
                        "enum": ["on", "off"]
                    },
                },
                "required": ["feature", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_vehicle_feature_up_down",
            "description": "Set or roll features like windows up or down",
            "parameters": {
                "type": "object",
                "properties": {
                    "feature": {
                        "type": "string",
                        "enum": ["windows"]
                    },
                    "status": {
                        "type": "string",
                        "enum": ["up", "down"]
                    },
                },
                "required": ["feature", "status"]
            }
        }
    }
]
```
2. The next step is to match the list of functions from **tools** with the actual Python functions.
``` Python
available_functions = {
    "set_vehicle_feature_on_off": vehicle_control,
    "set_vehicle_feature_up_down": vehicle_control
}
```
3. Based on the intent and entities extracted, the Jupyter notebook will call the relevant API endpoint of our Flask Web app.
``` Python
def vehicle_control(feature, action, status):
    vehicle_control_api = f"{VEHICLE_URL}/{feature}"
    headers = {"Content-Type": "application/json"}
    data = {action: status}
    vehicle_control_status = requests.post(
        vehicle_control_api,
        headers = headers,
        json = data
    )
    function_response = vehicle_control_status.json()
    return function_response
```
4. You may now set your system and user prompts, or pass user messages dynamically.
``` JSON
[
    {"role": "system", "content": "You are a smart in-car assistant. Your listen to commands and control vehicle features like air conditioner, lights, radio and windows."},
    {"role": "user", "content": "Please, switch off the air conditioner and roll the windows down."}
]
```
5. If everything was setup correctly, you should get something like this. Enjoy!
``` JSON
The air conditioner is now switched off, and the windows have been rolled down. Enjoy the breeze!
```
