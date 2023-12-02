import json
import logging
from django.http.request import HttpRequest
from django.http import HttpResponseBadRequest, JsonResponse

from agent.models import Agent
from .models import Conversation
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Debug.
# import pdb
# pdb.set_trace()

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.


@login_required()
def create_conversation(request):
    '''
    View to handle ajax request to create conversations
    '''
    print("in create_conversation")
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print(is_ajax)
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            print(type(data))
            print(data)
            print(data["agentId"])
            # payload = data.get('payload')
            # header = data.get('header')

            try:
                agent = Agent.objects.get(id=data["agentId"])
            except Exception as e:
                print(str(e))
            else:
                print(agent)
                conversation = Conversation(created_by=request.user,
                                            url="",
                                            context_data={'header': ""},
                                            with_agent=agent)
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
