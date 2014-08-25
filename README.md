pystubhub
=========

python bindings to the stubhub api

usage
-----

    from stubhub import StubhubClient

    stubhub = StubhubClient()  

    # Fetch Event 12345.
    events = stubhub.Event.fetch(12345)

    # Search Event objects by name/description.
    events = stubhub.Event.search_by_name('chvrches')

    # Search Event objects by arbitrary fields.
    events = stubhub.Event.search(description='chvrches')


Supports the following objects:

  - Event
  - Genre
  - Geo
  - Ticket
  - Venue

Supports the following methods per object:

  - fetch(object_id)
  - search_by_name(search_query)
  - search(param=val, param2=val)


notes, etc
----------

- loosely based on https://github.com/rloomba/stubhub (Ruby)
