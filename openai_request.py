import os
import json
import json5
import traceback
import glob
import re
import csv
from datetime import datetime
from openai import OpenAI


class JSONValidationError(Exception):
    def __init__(self, message, json_string=None):
        super().__init__(message)
        self.message = message
        self.json_string = json_string

class JSONParsingError(Exception):
    def __init__(self, message, json_string, text):
        super().__init__(message)

        print("The failed JSON string: \n\n")
        print(json_string)

        self.message = message
        self.json_string = json_string
        self.text = text

class OpenAIRequestBase:
    def __init__(self, use_cache=True, max_retries=3, cache_dir='cache'):
        self.client = OpenAI()  # Assume correct initialization with API key
        self.max_retries = max_retries
        self.use_cache = use_cache
        self.cache_dir = cache_dir
        self.ensure_dir_exists(self.cache_dir)

    def ensure_dir_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_cache_file_path(self, prompt, filename=None):
        if filename is None:

            filename = f"{abs(hash(prompt))}.json"
    
        cache_path = os.path.join(self.cache_dir, filename)
        print("cache_path: ", cache_path)
        cache_dir = os.path.dirname(cache_path)
        print("cache_dir: ", cache_dir)
        os.makedirs(cache_dir, exist_ok=True)
        return cache_path

    def save_to_cache(self, prompt, response, filename=None):
        file_path = self.get_cache_file_path(prompt, filename=filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({"prompt": prompt, "response": response}, file, ensure_ascii=False, indent=4)

    def load_from_cache(self, prompt, filename=None):
        file_path = self.get_cache_file_path(prompt, filename=filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                cached_data = json.load(file)
                return cached_data["response"]
        return None
    
    def validate_json(self, json_data, sample_json):
        if type(json_data) != type(sample_json):
            raise JSONValidationError("JSON data type does not match the sample JSON type.")

        if isinstance(sample_json, dict):
            for key, sample_value in sample_json.items():
                if key not in json_data:
                    raise JSONValidationError(f"Key '{key}' is missing.")
                self.validate_json(json_data[key], sample_value)
        elif isinstance(sample_json, list):
            if len(sample_json) > 0:
                sample_item = sample_json[0]
                for item in json_data:
                    self.validate_json(item, sample_item)

    def parse_response(self, response):
        first_dict_index = response.find('{')
        first_list_index = response.find('[')
        if first_dict_index == -1 and first_list_index == -1:
            raise JSONParsingError("No JSON structure found.", response, response)
        
        if (first_dict_index != -1 and first_dict_index < first_list_index) or (first_list_index == -1):
            parse_pattern = r'\{.*\}'
        else:
            parse_pattern = r'\[.*\]'

        matches = re.findall(parse_pattern, response, re.DOTALL)
        if not matches:
            raise JSONParsingError("No matching JSON structure found.", response, response)

        json_string = matches[0]
        try:
            return json5.loads(json_string)
        except json.JSONDecodeError as e:
            print("json_string: ", json_string)
            raise JSONParsingError("Failed to decode JSON.", json_string, response)

    def send_request_with_retry(self, prompt, system_content="You are an AI.", sample_json=None, filename=None):
        

        retries = 0
        # messages = [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}]
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]

        print("self.use_cache: ", self.use_cache)

        if self.use_cache:
            cached_response = self.load_from_cache(prompt, filename=filename)
            if cached_response:
                print("OpenAI cache found. ")
                return cached_response

        while retries < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=os.environ.get("OPENAI_MODEL", "gpt-4-0125-preview"),
                    messages=messages
                )
                ai_response = response.choices[0].message.content.strip()
                parsed_response = self.parse_response(ai_response)

                if sample_json:
                    self.validate_json(parsed_response, sample_json)

                self.save_to_cache(prompt, parsed_response, filename=filename)
                return parsed_response
            except Exception as e:
                traceback.print_exc()
                retries += 1
                messages.append({"role": "system", "content": ai_response})
                try:
                    messages.append({"role": "system", "content": e.message})
                except:
                    messages.append({"role": "system", "content": str(e)})

        raise Exception("Maximum retries reached without success.")
