from datetime import datetime
from flask import (
    make_response,
    abort
)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Data to serve with our API
DOGS = {
    "Max": {
        "name": "Max",
        "breed": "Lab",
        "owner": "Michael",
        "timestamp": get_timestamp()
    },
    "Charlie": {
        "name": "Charlie",
        "breed": "Mutt",
        "owner": "Karan",
        "timestamp": get_timestamp()
    },
    "Buddy": {
        "name": "Buddy",
        "breed": "Beagle",
        "owner": "Neal",
        "timestamp": get_timestamp()
    }
}

def read_all():
    """
    This function responds to a request for /api/dog
    with the complete lists of dogs
    :return:        json string of list of dogs
    """
    # Create the list of dog from our data
    return [DOGS[key] for key in sorted(DOGS.keys())]

def read_one(name):
    """
    This function responds to a request for /api/dogs/{name}
    with one matching dog from dogs
    :param name:    name of dog to find
    :return:        dog matching name
    """
    # Does the dog exist in dogs?
    if name in DOGS:
        dog = DOGS.get(name)

    # otherwise, nope, not found
    else:
        abort(404, 'Dog with name {name} not found'.format(
            name=name))

    return dog

def create(dog):
    """
    This function creates a new dog in the dogs structure
    based on the passed in dog data
    :param dog:  dog to create in dogs structure
    :return:        201 on success, 406 on dog exists
    """
    name = dog.get('name', None)
    breed = dog.get('breed', None)
    owner = dog.get('owner', None)


    # Does the dog exist already?
    if name not in DOGS and name is not None:
        DOGS[name] = {
            'name': name,
            'breed': breed,
            'owner': owner,
            "timestamp": get_timestamp()
        }
        return make_response('{name} successfully created'.format(
            name=name), 201)

    # Otherwise, dog exists
    else:
        abort(406, 'Dog with name {name} already exists'.format(
            name=name))

def update(name, dog):
    """
    This function updates an existing dog in the dogs structure
    :param name:   name of dog to update in the dog structure
    :param dog:  dog to update
    :return:        updated dog structure
    """
    # Does the dog exist in dogs?
    if name in DOGS:
        DOGS[name]['breed'] = dog.get('breed')
        DOGS[name]['owner'] = dog.get('owner')
        DOGS[name]['timestamp'] = get_timestamp()

        return DOGS[name]

    # otherwise, the dog does not exist
    else:
        abort(404, 'Dog with name {name} not found'.format(
            name=name))