from django.shortcuts import render

from django.http import JsonResponse
import requests
import json

# Create your views here.
from config.settings import OPEN_API_KEY

def openai_chat(request):
    if request.method == 'POST':
        openai_api_key = OPEN_API_KEY  # OpenAI API 키를 여기에 입력하세요.

        # 요청할 데이터를 설정합니다.
        data = {
            'model':"gpt-3.5-turbo",
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant.'
                },
                {
                    'role': 'user',
                    'content': request.POST.get('user_input', '')
                }
            ]
        }

        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }

        # OpenAI API로 POST 요청을 보냅니다.
        response = requests.post('https://api.openai.com/v1/chat/completions', data=json.dumps(data), headers=headers)
        print(response.json())
        if response.status_code == 200:
            response_data = response.json()
            assistant_response = response_data['choices'][0]['message']['content']

            # API 응답을 JSON 형식으로 반환합니다.
            return JsonResponse({'assistant_response': response_data})

        else:
            return JsonResponse({'error': 'API 요청이 실패했습니다.'}, status=500)

    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)

def print_hello(request):
    if request.method == "GET":
        return JsonResponse({
            "result":"hello"
        })