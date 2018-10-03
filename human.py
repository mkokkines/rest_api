from datetime import datetime
from flask import (
    make_response,
    abort
)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Data to serve with our API
HUMANS = {
    "Michael": {
        "name": "Michael Kokkines",
        "age": "19",
        "gender": "Male",
        "timestamp": get_timestamp()
    },
    "Neal": {
        "name": "Neal Sarraf",
        "age": "24",
        "gender": "Male",
        "timestamp": get_timestamp()
    },
    "Karan": {
        "name": "Karan",
        "age": "24",
        "gender": "Male",
        "timestamp": get_timestamp()
    }
}

def read_all():
    """
    This function responds to a request for /pets/humans
    with the complete lists of humans
    :return:        json string of list of humans
    """
    # Create the list of human from our data
    return [HUMANS[key] for key in sorted(HUMANS.keys())]

def read_one(name):
    """
    This function responds to a request for /pets/humans/{name}
    with one matching human from humans
    :param name:    name of human to find
    :return:        human matching name
    """
    # Does the human exist in humans?
    if name in HUMANS:
        human = HUMANS.get(name)

    # otherwise, nope, not found
    else:
        abort(404, 'Person with name {name} not found'.format(
            name=name))

    return human

def create(human):
    """
    This function creates a new human in the humans structure
    based on the passed in human data
    :param human:  human to create in human structure
    :return:        201 on success, 406 on human exists
    """
    name = human.get('name', None)
    age = human.get('breed', None)
    gender = human.get('owner', None)


    # Does the human exist already?
    if name not in HUMANS and name is not None:
        HUMANS[name] = {
            'name': name,
            'age': age,
            'gender': gender,
            "timestamp": get_timestamp()
        }
        return make_response('{name} successfully created'.format(
            name=name), 201)

    # Otherwise, human exists
    else:
        abort(406, 'Person with name {name} already exists'.format(
            name=name))