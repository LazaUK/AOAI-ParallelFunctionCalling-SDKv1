# Importing the libraries
from flask import Flask, render_template, request, json
from werkzeug.exceptions import HTTPException
from markupsafe import Markup

# Setting constants
ON = "ON"
OFF = "OFF"
UP = "UP"
DOWN = "DOWN"
SWITCH = "switch"
ROLL = "roll"
ERROR = "Missing payload value for the requested API."

# Creating a Vehicle class
class Vehicle:
    # Defining the constructor
    def __init__(
            self,
            airconditioner = OFF,
            lights = OFF,
            radio = OFF,
            windows = UP
        ):
        self.radio = radio
        self.airconditioner = airconditioner
        self.windows = windows
        self.lights = lights

    # Defining a method to get the vehicle features status
    def get_status(self):
        return json.dumps({
            "radio": self.radio,
            "airconditioner": self.airconditioner,
            "windows": self.windows,
            "lights": self.lights
        })
    
    # Defining a method to set the vehicle feature status
    def set_features(self, feature, Status_A, Status_B, status_Request):
        if (status_Request == Status_A or status_Request == Status_B):
            setattr(self, feature, status_Request)
            return json.dumps({
                feature: status_Request
            })
        else:
            return json.dumps({
                "error": f"Invalid switch value for the {feature} API. I can only accept {Status_A} and {Status_B} values."
            })
myVehicle = Vehicle()

# Creating a Flask app
app = Flask(__name__)

# Creating a route for the home page
@app.route("/")
def home_page():
    # Defining description for HTML page
    api_description = Markup(
        """
        <p>Solaria Tech Engineering is a company that designs and manufactures innovative cars. Our latest models now support API integration with the following in-car features.</p>
        <h2>API Documentation:</h2>
        <ul>
            <li><strong>API Endpoint:</strong> /status
                <ul>
                    <li><strong>Method:</strong> GET</li>
                    <li><strong>Response:</strong> JSON string, e.g. {"airconditioner":"OFF", "lights":"OFF", "radio":"OFF", "windows":"UP"}</li>
                </ul>
            </li>
            </br>
            <li><strong>API Endpoint:</strong> /airconditioner
                <ul>
                    <li><strong>Method:</strong> POST</li>
                    <li><strong>Request:</strong> "application/json" type with payload: {"switch": "ON"} or {"switch": "OFF"}</li>
                    <li><strong>Response:</strong> JSON string, e.g. {"airconditioner": "OFF"}</li>
                </ul>
            </li>
            </br>
            <li><strong>API Endpoint:</strong> /lights
                <ul>
                    <li><strong>Method:</strong> POST</li>
                    <li><strong>Request:</strong> "application/json" type with payload: {"switch": "ON"} or {"switch": "OFF"}</li>
                    <li><strong>Response:</strong> JSON string, e.g. {"lights": "ON"}</li>
                </ul>
            </li>
            </br>
            <li><strong>API Endpoint:</strong> /radio
                <ul>
                    <li><strong>Method:</strong> POST</li>
                    <li><strong>Request:</strong> "application/json" type with payload: {"switch": "ON"} or {"switch": "OFF"}</li>
                    <li><strong>Response:</strong> JSON string, e.g. {"radio": "OFF"}</li>
                </ul>
            </li>
            </br>
            <li><strong>API Endpoint:</strong> /windows
                <ul>
                    <li><strong>Method:</strong> POST</li>
                    <li><strong>Request:</strong> "application/json" type with payload: {"roll": "UP"} or {"roll": "DOWN"}</li>
                    <li><strong>Response:</strong> JSON string, e.g. {"windows": "UP"}</li>
                </ul>
            </li>
        </ul>
        """
    )
    # Rendering the home.html template with API image and description as arguments
    return render_template(
        "home.html",
        api_image = "car.jpg",
        api_description = api_description
    )

# Creating a route for the status API
@app.get("/status")
def status_api():
    vehicle_status = myVehicle.get_status()
    return vehicle_status

# Creating a route for the airconditioner API
@app.post("/airconditioner")
def airconditioner_api():
    if (request.json[SWITCH]):
        airconditioner_status = myVehicle.set_features("airconditioner", ON, OFF, request.json[SWITCH].upper())
        return airconditioner_status
    else:
        return json.dumps({
            "error": ERROR
        })

# Creating a route for the lights API
@app.post("/lights")
def lights_api():
    if (request.json[SWITCH]):
        lights_status = myVehicle.set_features("lights", ON, OFF, request.json[SWITCH].upper())
        return lights_status
    else:
        return json.dumps({
            "error": ERROR
        })
    
# Creating a route for the radio API
@app.post("/radio")
def radio_api():
    if (request.json[SWITCH]):
        radio_status = myVehicle.set_features("radio", ON, OFF, request.json[SWITCH].upper())
        return radio_status
    else:
        return json.dumps({
            "error": ERROR
        })

# Creating a route for the windows API
@app.post("/windows")
def windows_api():
    if (request.json[ROLL]):
        windows_status = myVehicle.set_features("windows", UP, DOWN, request.json[ROLL].upper())
        return windows_status
    else:
        return json.dumps({
            "error": ERROR
        })

# Defining generic HTTP error handler
@app.errorhandler(HTTPException)
def internal_server_error(error):
    return json.dumps({
            "error": error.description
    })

# Running the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
