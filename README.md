Creation of a backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading).

This app is part of the selection process to fulfill a position as software developer at MODEC, Inc.

Please take note that this is my first real project and it is prone to a lot of errors, mainly in the code execution. With that said, let's begin. =D


The first real step here is to understand why we need this API and what exactly it does. This system will be used to register vessels owned by the company and assign several different kinds of equipment to each vessel. Each vessel will have its own unique code of identification, and also each equipment will have its own unique code. Each piece of equipment must be related to a specific vessel, and will have an indication of whether it is active or not.

Here we can determine that our application needs two resources: vessels and equipments.

All this data must be persisted into a database so it can be retrieved later by other applications for different use cases. So the best approach to build our application is to create a RESTful API, which means our system will handle the logic internally, but will receive and deliver information in a standard way, so that it can be accessed by different other systems regardless of the language or architecture they were built.

Our implementation will be built using the Django Web Framework along with the Django REST Framework and the data will be persisted using the SQLite databse.

The Django REST Framework utilizes the Model, View, Serializer archutecture, where:
    The Model layer represents the data persistence into the database;
    The View layer represents the business logic of the application;
    And the Serializer layer handles the conversion of the data to a web standard format, namely JSON.

So the typicall flow of and application using this archutecture is like:
    1. User sends a request for a specific resource using the JSON format;
    2. The View passes the data through the Serializer;
    3. The Serializer translates the request into query format for communication with the database, and sends it back to the View;
    4. The View forwards the request to the Model;
    5. The Model will communicate directly with the database retrieving the specific data asked for in the request and will send it back to the View;
    6. Here, the process is inverted: The view sends the data to the Serializer to be converted into the JSON format and generates a response;
    7. The response will be sent back to the user with the data from the resource requested.


The resources in our application can be accessed via URLs, and the type of interaction will be determined by the HTTP verbs used in the request. So, our API has two resources and four main functionalities:
    Resources: vessel and equipment, where equipment is a subset of vessel.

Functionalities:
1. Register a vessel.
    The information used to describe a vessel will be solely its code.
    For a vessel to be registered, we need to input its code, which is unique for each vessel.
    To input vessel data, we use the POST HTTP method.
    A valid input to register a vessel is:
    {
        "code": "MV32"
    }
            
    
2. Register an equipment in a vessel.
    There are a few information used to describe an equipment: name, code, location, status and vessel.
    Every and each piece of equipment must be related to a single vessel, and a vessel can have lots of equipment.
    The code of each equipment is unique, and all equipment is automatically active after registration.
    To input equipment data, we use the POST HTTP method.
    A valid input to register a piece of equipment is:
    {
        "name": "sensor",
        "code": "53A95057",
        "location": "Brazil"
    }

        Here we can note that it is not mandatory to provide the vessel where the sensor is installed. So we can assume that, unless specified, all sensors are to be installed in a default vessel.
    

    3. Set an equipment's status to inactive.
        Since all equipment are initially registered as active, a situation may arise where we need to deactivate one or a few of them.
        Since we are changing only a single data of the equipment, namely its status, we use the HTTP PATCH method.
        We must specify which equipment we want to deactivate.

        OBS: There may be a discussion on whether to use PUT or PATCH to update a resource. In this specific case, we can assuredly use PATCH, since we only want to apply a partial update to the resource, which will slightly reduce bandwidth consumption and increase speed of the processing. This difference may not be noted in a small application such as this one, but in larger real-time applications it may represent a significant gain in performance.


    4. Return all active equipment in a given vessel.
        Here we want to retrieve a resource, so we use the GET HTTP method.
        We a pass a single vessel and want to see all of its equipment that is active.
        This resource needs a filter to work, because we need to check whether each equipment is active and in the requested vessel.


So, our database tables will look something like this:


    Vessel
        code: string


    Equipment
        name: string
        code: string
        location: string
        vessel: foreign_key
        status: boolean


We could make the code field in each table be our primary keys, but it is not a good practice to make strings as primary keys, since the code for an item may change in the future and database management systems process number data faster than character data types. So we will let Django handle the primary keys creation process, where it will be the standard unique, auto incremented integer.


The URLs used to access the resources will be the following:
    vessel/
        Using the POST HTTP method.
        Will be used to register a new vessel.
        Ex: Let's register the MV33 vessel into our system.
            We need to access http://localhost:8000/vessel/ and fill the body of our request with the data we need, which is:

            {
                "code": "MV33"
            }

            This will result in a 201 Created HTTP status code.

            But if we try to register the same vessel again, we will receive the 400 Bad Request HTTP status code, saying that a vessel with this code already exists.

            Also, trying to use a different HTTP method other than POST will render the 405 Method Not Allowed HTTP response.

    vessel/equipment/
        Using the POST HTTP method.
        Will be used to register a new equipment.
        Ex: Let's register a new equipment.
            We need to access http://localhost:8000/vessel/equipment/ and fill the body of our request with the data we need, which is:
            
            {
                "name": "sensor",
                "code": "53A94248",
                "location": "Brazil"
            }

            This will result in a 201 Created HTTP status code.
            
            And since all new equipment are automatically set to active, we don't need to provide that data. It is also important to note that if we don not provide a vessel, the new equipment will be assigned to the first vessel registered, which is the vessel MV102.

            If we try to register the same equipment again, we will receive the 400 Bad Request HTTP status code, saying that an equipment with this code already exists.

            Also, trying to use a different HTTP method other than POST will render the 405 Method Not Allowed HTTP response.


    vessel/<pk>/
        Using the GET HTTP method.
        Will be used to return all active equipment in the given vessel.
        Ex: Let's list all the active equipment of the MV102 vessel, which is the first register in our database.
            We just need to access http://localhost:8000/vessel/1/ and the response will be something like:
            [
                {
                    "id": 4,
                    "name": "compressor",
                    "code": "6410B9D8",
                    "location": "Brazil",
                    "status": true,
                    "vessel": 1
                },
                {
                    "id": 7,
                    "name": "sensor",
                    "code": "53654248",
                    "location": "Brazil",
                    "status": true,
                    "vessel": 1
                },
                {
                    "id": 6,
                    "name": "sensor",
                    "code": "53A94248",
                    "location": "Brazil",
                    "status": true,
                    "vessel": 1
                },
                {
                    "id": 5,
                    "name": "sensor",
                    "code": "53A95057",
                    "location": "Brazil",
                    "status": true,
                    "vessel": 1
                }
            ]

            And the 200 OK HTTP status code.

            If we pass a vessel that does not exist, or if there is no active equipment in that vessel, the API will return the 404 Not Found HTTP status code.

    vessel/equipment/<pk>/
        Using the PATCH HTTP method.
        Will be used to set the status of a given equipment to inactive.
        
        The idea here is to receive partial data from an equipment, or a list of equipment, in the request and update its field "status" in the database, but I lack the technical knowledge to make it work ate the moment.


