# Unofficial client for [Eero Mesh Routers](https://eero.com)


# SDK Design Considerations
The SDK leverages pydantic to return models for all supported endpoints, endpoints are created using a method factory and configurations in the [routes.py](/eero//client//routes/routes.py) file allowing for easy extension.

- `GET` Methods are exposed as class properties
- `POST` Methods are exposed as class methods with `**kwargs` for route params (if applicable).

As this is an undocumented API, I was only able to create models for the objects returned in my network, please consider contributing / updating models if your network has additional parameters.


# Usage Example
[example.ipynb](/example.ipynb)

## Authentication
```
from eero import Eero, FileSessionStorage

session = FileSessionStorage("session.cookie")
eero = Eero(session=session)

if not eero.is_authenticated:
    auth_source = input("Phone Number or Email: ")
    user_token = eero.login(auth_source)
    verification_code = input("verification key from email or SMS: ")
    eero.login_verify(verification_code, user_token)
```

## Routes
### Get Requests
[GET_RESOURCES](/eero//client/routes/routes.py) defines the get properties in the structure of `{property_name: tuple[url, response_model]}`

The following get properties are defined:
```
account
ac_compat
device_blacklist
devices
diagnostics
eeros
forwards
ouicheck
guestnetwork
profiles
reservations
speedtest
updates
support
insights
routing
thread
networks
```
### Post Requests
[POST_RESOURCES](/eero//client/routes/routes.py) defines the post methods in the structure of `{property_name: tuple[url, response_model]}`

The following get properties are defined:
```
burst_reporters
reboot
reboot_eero - takes in the id of the error to reboot, available from the client.eeros get endpoint. 
run_speedtest
```
# Inspiration
Thank you to `Max von Webel` for his original work, [eero-client](https://github.com/343max/eero-client), I hadn't considered accesssing my router's data until I saw his project and only opted to fork and rewrite to add more of my own opinionated design patterns.

# Future Plans
## Device Triangulation
I played with the idea of using the signal strength for each connected device captured while looping over the network turn off all but one eero at a time, and the relative 3D coordinates of the eero devices to create a 3D rendering of all of the devices in my home. This worked decently well for devices in a room with an eero, but for obstructed devices their positions there were too many intersection points with a mesh of four units. If I circle back to this in the future I may add code in a post. 

## Home Assistant Integration
My next goal is to expose the eeros & devices in Home Assistant through an integration, when I'm successful I'll post a link to that repo/HACS integration here my intent is to use this SDK as the foundation for that work.