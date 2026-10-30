"""Minimal fixed-vendor HTTPS transports. Credentials never enter records."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderError('Provider redirect refused')


def call(provider, model, system, user, max_tokens, timeout=60, response_schema=None):
    if provider == 'openai':
        key = os.environ.get('OPENAI_API_KEY')
        url = 'https://api.openai.com/v1/responses'
        headers = {'Authorization': 'Bearer ' + (key or ''), 'Content-Type': 'application/json'}
        body = {'model': model, 'instructions': system, 'input': user, 'max_output_tokens': max_tokens,
                'temperature': .2, 'store': False}
        if response_schema is not None:
            body['text']={'format':{'type':'json_schema','name':'task_response','strict':True,'schema':response_schema}}
    elif provider == 'anthropic':
        key = os.environ.get('ANTHROPIC_API_KEY')
        url = 'https://api.anthropic.com/v1/messages'
        headers = {'x-api-key': key or '', 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json'}
        body = {'model': model, 'system': system, 'messages': [{'role': 'user', 'content': user}],
                'max_tokens': max_tokens, 'temperature': 0}
        if response_schema is not None:
            body['output_config']={'format':{'type':'json_schema','schema':response_schema}}
    else:
        raise ProviderError('Unsupported provider')
    if not key:
        raise ProviderError('Missing ' + ('OPENAI_API_KEY' if provider == 'openai' else 'ANTHROPIC_API_KEY'))
    start = time.monotonic()
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        # Do not retain error bodies, URLs with queries, auth headers or request objects.
        raise ProviderError('Provider HTTP ' + str(e.code)) from None
    except (urllib.error.URLError, TimeoutError):
        raise ProviderError('Provider transport failure') from None
    if provider == 'openai':
        text = ''.join(c.get('text', '') for item in data.get('output', []) for c in item.get('content', []) if c.get('type') == 'output_text')
        usage = data.get('usage', {})
        inputs, outputs = usage.get('input_tokens'), usage.get('output_tokens')
        stop = data.get('status')
        complete=stop=='completed'
    else:
        text = ''.join(c.get('text', '') for c in data.get('content', []) if c.get('type') == 'text')
        usage = data.get('usage', {})
        inputs, outputs = usage.get('input_tokens'), usage.get('output_tokens')
        stop = data.get('stop_reason')
        complete=stop=='end_turn'
    return {'text': text, 'model': data['model'], 'response_id': data.get('id'), 'input_tokens': inputs,
            'output_tokens': outputs, 'seconds': time.monotonic() - start, 'finish_reason': stop,
            'complete':complete,'requested_model_match':data.get('model')==model,
            'temperature': .2 if provider == 'openai' else 0, 'max_output_tokens': max_tokens,
            'seed': None, 'seed_support': 'No seed requested; repeat indices are scheduling labels only.'}
