
# OpenAIRequestBase Usage Guide

## Overview
This repository hosts the `OpenAIRequestBase` class, which provides a structured approach for making requests to the OpenAI API and handling JSON responses. It enables functionality for caching, validating JSON structures based on a sample format, and retrying requests upon failures. This guide will demonstrate how to extend the `OpenAIRequestBase` class and utilize it for specific requests.

## Requirements
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

## Installation
To ensure the necessary Python packages are installed:
```bash
pip install openai json5
```

## Usage

### Extending OpenAIRequestBase
Create a subclass of `OpenAIRequestBase`. This subclass can override existing methods or introduce new functionalities specific to your needs.

#### Example: WeatherInfoRequest
Below is an example class that inherits from `OpenAIRequestBase` to fetch weather information. The JSON structure used for validation is passed directly in the prompt.

```python
from openai_request_base import OpenAIRequestBase

class WeatherInfoRequest(OpenAIRequestBase):
    def __init__(self):
        super().__init__(use_cache=True, max_retries=5, cache_dir='weather_cache')
    
    def get_weather_info(self, location):
        sample_json = {"temperature": "", "condition": ""}
        sample_json_str = json.dumps(sample_json)
        prompt = f"What is the current weather in {location}? Expected format: {sample_json_str}"
        return self.send_request_with_retry(prompt, sample_json=sample_json)
```

### Making Requests
Utilize the derived class to perform API requests. Here is how you can use `WeatherInfoRequest` to retrieve weather data:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

## Contributing
Feel free to contribute to this project by submitting pull requests or opening issues to enhance functionalities or fix bugs.

## About
The project is managed by Lachlan Chen and is part of the "The Art of Lazying" channel initiatives.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

