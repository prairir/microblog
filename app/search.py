# Define functions for interacting with Elasticsearch index

def add_to_index(index, model):
    """Add the given model object to the Elasticsearch index."""
    # If Elasticsearch is not configured, return without indexing.
    if not current_app.elasticsearch:
        return
    # Create a payload containing searchable fields of the model object.
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    # Index the payload with the given index name and model ID.
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """Remove the given model object from the Elasticsearch index."""
    # If Elasticsearch is not configured, return without deleting.
    if not current_app.elasticsearch:
        return
    # Delete the document with the given index name and model ID.
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """Query the Elasticsearch index with the given query string."""
    # If Elasticsearch is not configured, return an empty result set.
    if not current_app.elasticsearch:
        return [], 0
    # Search the index with the given query string.
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    # Extract the IDs of matching documents from the search result.
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    # Return the IDs and total count of matching documents.
    return ids, search['hits']['total']['value']
