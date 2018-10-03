/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'pets/cats',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(name, breed, owner) {
            let ajax_options = {
                type: 'POST',
                url: 'pets/cats',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'name': name,
                    'breed': breed,
                    'owner': owner
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(name, breed, owner) {
            let ajax_options = {
                type: 'PUT',
                url: 'pets/cats/' + name,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'name': name,
                    'breed': breed,
                    'owner': owner
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(name) {
            let ajax_options = {
                type: 'DELETE',
                url: 'pets/cats/' + name,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $name = $('#name'),
        $breed = $('#breed'),
        $owner = $('#owner');

    // return the API
    return {
        reset: function() {
            $name.val('');
            $breed.val('')
            $owner.val('').focus();
        },
        update_editor: function(name, breed, owner) {
            $name.val(name);
            $breed.val(breed);
            $owner.val(owner).focus();
        },
        build_table: function(cats) {
            let rows = '';

            // clear the table
            $('.cats table > tbody').empty();

            // did we get a cats array?
            if (cats) {
                for (let i=0, l=cats.length; i < l; i++) {
                    rows += `<tr><td class="name">${cats[i].name}</td><td class="breed">${cats[i].breed}</td><td class="owner">${cats[i].owner}</td><td>${cats[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $name = $('#name'),
        $breed = $('#breed'),
        $owner = $('#owner');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(name, breed, owner) {
        return name !== "" && breed !== "" && owner !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let name = $name.val(),
            breed = $breed.val(),
            owner = $owner.val();

        e.preventDefault();

        if (validate(name, breed, owner)) {
            model.create(name, breed, owner)
        } else {
            alert('Problem with input');
        }
    });

    $('#update').click(function(e) {
        let name = $name.val(),
            breed = $breed.val(),
            owner = $owner.val();

        e.preventDefault();

        if (validate(name, breed, owner)) {
            model.update(name, breed, owner)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let name = name.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            name,
            breed,
            owner;

        name = $target
            .parent()
            .find('td.name')
            .text();

        breed = $target
            .parent()
            .find('td.breed')
            .text();

        owner = $target
            .parent()
            .find('td.owner')
            .text();

        view.update_editor(name, breed, owner);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));