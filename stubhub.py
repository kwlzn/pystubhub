import requests
import simplejson

# Simple python bindings for the StubHub LCS.
# http://stubhubapi.stubhub.com/index.php/Anatomy_of_a_Listing_Catalog_Service_HTTP_Request


class RemoteObject(object):
  def __init__(self, parent, obj_type=None):
    self.parent = parent
    self.obj_type = obj_type or self.__class__.__name__.lower()

  def make_params(self, **kwargs):
    return dict(stubhubDocumentType=self.obj_type, **kwargs)

  def fetch(self, obj_id, meta_param='id', **uri_params):
    params = self.make_params(**{meta_param: obj_id})
    return self.parent.make_call(params, uri_params)

  def search(self, uri_params={}, **query_params):
    params = self.make_params(**query_params)
    return self.parent.make_call(params, uri_params)

  def search_by_name(self, query, uri_params={}, **query_params):
    params = self.make_params(**dict(description=query, **query_params))
    return self.parent.make_call(params, uri_params)

  def __repr__(self):
    return '<%s>' % self.obj_type.title()


class Event(RemoteObject):
  """A Stubhub Event object."""

  def fetch(self, *args, **kwargs):
    return RemoteObject.fetch(self, *args, meta_param='event_id', **kwargs)


class Genre(RemoteObject):
  """A Stubhub Genre object."""


class Geo(RemoteObject):
  """A Stubhub Geo object."""

  def fetch(self, *args, **kwargs):
    return RemoteObject.fetch(self, *args, meta_param='geoId', **kwargs)


class Ticket(RemoteObject):
  """A Stubhub Ticket object."""


class Venue(RemoteObject):
  """A Stubhub Venue object."""

  def fetch(self, *args, **kwargs):
    return RemoteObject.fetch(self, *args, meta_param='venue_id', **kwargs)


class ClientBase(object):
  class ContentError(Exception): pass

  def __init__(self, credentials=None):
    self.credentials = credentials
    self._obj_cache = {}

  def resolve_query(self, query_params):
    """Resolve a search query for SOLR."""
    return ''.join(['+{0}:{1}\r\n'.format(x, y) for x, y in query_params.items()])

  def resolve_params(self, params):
    new_params = dict(start=0, rows=10, wt='json')
    new_params.update(params)
    return new_params

  def make_call(self, search_params, uri_params):
    """Make and return a requests call."""
    query = self.resolve_query(search_params)
    response = requests.get(self.BASE_URI, params=self.resolve_params(dict(q=query, **uri_params)))
    response.raise_for_status()
    try:
      return response.json()['response']['docs']
    except (KeyError, simplejson.scanner.JSONDecodeError) as e:
      raise self.ContentError(response=response, original_exc=e)

  def find_or_cache_obj(self, obj_type):
    if obj_type not in self._obj_cache:
      self._obj_cache[obj_type] = globals()[obj_type](parent=self)
    return self._obj_cache[obj_type]


class StubHubClient(ClientBase):
  BASE_URI = 'http://www.stubhub.com/listingCatalog/select'

  @property
  def Event(self):
    return self.find_or_cache_obj('Event')

  @property
  def Genre(self):
    return self.find_or_cache_obj('Genre')

  @property
  def Geo(self):
    return self.find_or_cache_obj('Geo')

  @property
  def Ticket(self):
    return self.find_or_cache_obj('Ticket')

  @property
  def Venue(self):
    return self.find_or_cache_obj('Venue')

