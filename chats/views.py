from django.shortcuts import render

from django.http import JsonResponse
import requests
import json
import tiktoken

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
        num_token = num_tokens_from_messages(data['messages'], data['model'])


        if response.status_code == 200:
            response_data = response.json()
            assistant_response = response_data['choices'][0]['message']['content']

            # API 응답을 JSON 형식으로 반환합니다.
            return JsonResponse({'data':response_data,
                                 'num_token':num_token})

        else:
            return JsonResponse({'error': 'API 요청이 실패했습니다.'}, status=500)

    return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)


##for health check
def print_hello(request):
    if request.method == "GET":
        return JsonResponse({
            "result":"hello"
        })
    
import tiktoken

def num_tokens_from_messages(messages, model):

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens_per_message, tokens_per_name = get_tokens_per_message(model)
    
    num_tokens = calculate_num_tokens(messages, encoding, tokens_per_message, tokens_per_name)
    return num_tokens

def get_tokens_per_message(model):
    token_mappings = {
        "gpt-3.5-turbo-0613": (3, 1),
        "gpt-3.5-turbo-16k-0613": (3, 1),
        "gpt-4-0314": (3, 1),
        "gpt-4-32k-0314": (3, 1),
        "gpt-4-0613": (3, 1),
        "gpt-4-32k-0613": (3, 1),
        "gpt-3.5-turbo-0301": (4, -1),
    }
    
    if model in token_mappings:
        return token_mappings[model]
    
    if "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return token_mappings["gpt-3.5-turbo-0613"]
    
    if "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return token_mappings["gpt-4-0613"]
    
    raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")

def calculate_num_tokens(messages, encoding, tokens_per_message, tokens_per_name):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with assistant
    return num_tokens
