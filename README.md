pystubhub
=========

python bindings to the stubhub api

usage
=====

    from stubhub import StubhubClient

    stubhub = StubhubClient()  

    # Fetch Event 12345.
    events = stubhub.Event.fetch(12345)

    # Search Event objects by name/description.
    events = stubhub.Event.search_by_name('chvrches')

    # Search Event objects by arbitrary fields.
    events = stubhub.Event.search(description='chvrches')


Supports the following objects: Ticket, Event, Geo, Venue

Supports the following methods per object: fetch, search_by_name, search