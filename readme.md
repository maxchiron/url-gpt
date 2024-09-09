# url-gpt

url-gpt is a web application that allows users to analyze the content of multiple URLs using OpenAI's GPT model. It crawls the specified URLs, extracts their content, and uses it as context for generating responses based on user-provided prompts.

## Features

- Web crawling of multiple URLs
- Content extraction and cleaning
- Integration with OpenAI's GPT model for text generation
- User-friendly interface built with Gradio
- Proxy support for web requests
- User agent rotation to avoid blocking
- Regeneration of responses with the same context

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/maxchiron/url-gpt.git
   cd url-gpt
   ```

2. Install the required packages:
   ```
   pip install -U -r requirements.txt
   ```

3. Set your OpenAI API key as an environment variable:
   ```
   set OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```
   or use the provided batch file:
   (add key to .bat file first)
   ```
   run_app.bat
   ```

2. Open the provided URL in your web browser.

3. Enter the URLs you want to analyze (one per line. **Edit in notepad and than past all to urls textbox.**) in the "Enter URLs" text box.

4. Enter your prompt in the "Enter your prompt" text box.

5. (Optional) Enter a proxy server address if needed.

6. Click the "Submit" button to process the URLs and generate a response.

7. To regenerate a response using the same context, click the "Regenerate Response" button.

## Dependencies

- gradio
- requests
- beautifulsoup4
- openai

## Configuration

- The application uses the OpenAI API. Make sure to set your API key as an environment variable before running the app.
- You can modify the `user_agents` list in `app.py` to add or change the user agents used for web crawling.
- The default proxy is set to `http://127.0.0.1:7897`. You can change this in the web interface when running the app.

---

For any issues or questions, please open an issue on the GitHub repository.