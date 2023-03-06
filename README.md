# Fleet management system

The system consists of three microservices:
- fleet management service (FMS): manages the driver-vehicle-trip database and triggers the chain of events.
- GPS simulator (GS): simulates trips sending out the positions and speeds along a trip.
- vehicle monitoring system (VMS): supervises the motion of the vehicles and penalizes the speeding.

The speed over 100 km/h implies 5 penalty points per km/h, over 80 km/h, 2 points per km/h
and over 60 km/h, 1 point per km/h.

To be able to finish with most of the work, I used one dimensional coordinate system which does not effect the main
business logic.

For the ID values of the driver-vehicle-trip database, the auto generated UUID was used avoiding the entering of
the fields and reducing the chance of collision during testing.


## Assumption on the event flow

Only one driver can drive one vehicle on a trip.
Supposing that when a driver and a trip are assigned to a vehicle, the trip starts immediately implies
that in the vehicle-trip assignments one vehicle can be included once
and in the vehicle-driver assignments one vehicle can be included once and one driver can be included once as well.

The GPS simulator gets the trip information and leads the vehicle from the departure to the destination position
gradually accelerating, then gradually decelerating, in order to be able to stop at the destination.


## Design decisions

### Framework

The miscroservices are implemented as Django applications:
- using one framework for all saved time;
- Django rest framework is very simple (but not so intuitive) to implement a REST service;
- Django ORM allows handling data easily.

### Testing

Integration-like automated tests have been preferred now to save time. Also, not everything is tested.

### Asynchronous operations

Unfortunately, infinite background tasks are not simple to start from django and the custom management command was
chosen to implement the message queue consumers. This is not an optimal solution with several issues.

### Messaging protocol

The `direct` exchange type of the AMQP has been choosen to peer-to-peer sending messages.
One message route is identified by the routing key and the message type.

The messages are serialized to JSON string and parsed and validated using Pydantic data models.
[One of my repository](https://github.com/matez0/rabbitmq-callback-decorator) is reused to implement this layer.

The schemas of the messages and the routing keys are grouped into interface modules, e.g. [if_fms_gs.py](if_fms_gs.py).

### Database

Since Django ORM supports maximally the relational databases, the postgres DBMS has been easy to use.


## Local testing

Create a Python virtual environment:
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```
Install dependencies:
```
pip install -r requirements.txt
```
Make migrations, if it is needed:
```
python manage.py makemigrations --settings=project.settings.fms
python manage.py migrate --settings=project.settings.fms
```
Run the tests of a microservice:
```
python manage.py test -v3 --settings=project.settings.fms &
```

## Setting up the system

```
docker network create fms_net
docker-compose up
```

## Manual testing

Create a driver, vehicle, trip and assign them by using the Django rest framework UI:
```
$BROWSER http://localhost:8888
```
After a driver-vehicle-driver triplet is assigned, the FMS shall message the GPS simulator which shall start sending
the GPS events along the trip until reaching the destination.

When VMS detects speed limit violation, it shall message the FMS to update the penalty points.

The process can be followed on the rabbitmq UI as well:
```
$BROWSER http://localhost:15672/#/queues
```
