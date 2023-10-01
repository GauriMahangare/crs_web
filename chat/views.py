import json
import logging
from django.http.request import HttpRequest
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Conversation
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.


@login_required()
def create_conversation(request):
    '''
    View to handle ajax request to create conversations
    '''
    print("inside create_conversation")
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            payload = data.get('payload')
            header = data.get('header')
            print(payload)
            print(data)
            conversation = Conversation(created_by=request.user,
                                        url="",
                                        context_data={'header': header})
            try:
                conversation.save()
            except Exception as e:
                print(str(e))
                return JsonResponse({'message': 'Internal Error'}, status=500)
            else:
                data = {'id': conversation.id, 'status': conversation.status, }
            return JsonResponse(data)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)
