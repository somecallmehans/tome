import json

from rest_framework.response import Response
from datetime import datetime

from rest_framework.decorators import api_view

@api_view(['POST'])
def make_sessions_and_rounds(request):
    body = json.loads(request.body.decode('utf-8'))
    session_id = body.get("session_id", None)

    if not session_id:
        today = datetime.today()
        mm_yy = today.strftime("%m-%y")
        
    return Response({"test": 1234})

