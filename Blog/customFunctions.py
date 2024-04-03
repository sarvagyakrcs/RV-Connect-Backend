import json
from django.core.serializers import serialize
from django.http import JsonResponse


# Serialize the query result (model instance) to JSON
def jsonify_query_result(query_result):
    serialized_data = serialize('json', [query_result])
    data_dict = json.loads(serialized_data)[0]['fields']
    return JsonResponse(data_dict)
