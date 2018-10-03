from datetime import datetime
from flask import (
    make_response,
    abort
)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Data to serve with our API
CATS = {
    "Tiger": {
        "name": "Tiger",
        "breed": "siamese",
        "owner": "Michael",
        "timestamp": get_timestamp()
    },
    "Misty": {
        "name": "Misty",
        "breed": "himalayan",
        "owner": "Karan",
        "timestamp": get_timestamp()
    },
    "Oscar": {
        "name": "Oscar",
        "breed": "burmese",
        "owner": "Neal",
        "timestamp": get_timestamp()
    }
}

def read_all():
    """
    This function responds to a request for /api/cat
    with the complete lists of cats
    :return:        json string of list of cats
    """
    # Create the list of cats from our data
    return [CATS[key] for key in sorted(CATS.keys())]

def read_one(name):
    """
    This function responds to a request for /api/cat/{name}
    with one matching cat from cats
    :param name:    name of cat to find
    :return:        cat matching name
    """
    # Does the cat exist in cats?
    if name in CATS:
        cat = CATS.get(name)

    # otherwise, nope, not found
    else:
        abort(404, 'Cat with name {name} not found'.format(
            name=name))

    return cat

def create(cat):
    """
    This function creates a new cat in the cats structure
    based on the passed in cat data
    :param cat:  cat to create in cats structure
    :return:        201 on success, 406 on cat exists
    """
    name = cat.get('name', None)
    breed = cat.get('breed', None)
    owner = cat.get('owner', None)


    # Does the cat exist already?
    if name not in CATS and name is not None:
        CATS[name] = {
            'name': name,
            'breed': breed,
            'owner': owner,
            "timestamp": get_timestamp()
        }
        return make_response('{name} successfully created'.format(
            name=name), 201)

    # Otherwise, cat exists
    else:
        abort(406, 'Cat with name {name} already exists'.format(
            name=name))

def update(name, cat):
    """
    This function updates an existing cat in the cats structure
    :param name:   name of cat to update in the cat structure
    :param cat:  cat to update
    :return:        updated cat structure
    """
    # Does the cat exist in cats?
    if name in CATS:
        CATS[name]['breed'] = cat.get('breed')
        CATS[name]['owner'] = cat.get('owner')
        CATS[name]['timestamp'] = get_timestamp()

        return CATS[name]

    # otherwise, the cat does not exist
    else:
        abort(404, 'Cat with name {name} not found'.format(
            name=name))

def delete(name):
    """
    This function deletes a cat from the cats structure
    :param name:   name of cat to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the cat to delete exist?
    if name in CATS:
        del CATS[name]
        return make_response('{name} successfully deleted'.format(
            name=name), 200)

    # Otherwise, cat does not exist
    else:
        abort(404, 'Cat with name {name} not found'.format(
            name=name))