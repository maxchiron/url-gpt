import gradio as gr
import requests
from bs4 import BeautifulSoup
import time
import random
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def crawl_url(url, max_retries=3, proxy=None):
    session = requests.Session()
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    
    for _ in range(max_retries):
        try:
            # Random delay between requests
            time.sleep(random.uniform(1, 3))
            
            # Rotate user agents
            headers = {'User-Agent': random.choice(user_agents)}
            
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 403:
                print(f"Access forbidden for {url}. The server may be blocking our requests.")
                continue
            elif response.status_code == 418:
                print(f"The server thinks we're a bot for {url}. Trying again with a different user agent.")
                continue
            
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")
    return f"Failed to crawl {url} after {max_retries} attempts."

def get_gpt_response(system_prompt, context):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def process_input(urls, prompt, proxy):
    # Crawl URLs
    url_contents = {}
    for url in urls.split():
        url = url.strip()
        content = crawl_url(url, proxy=proxy)
        url_contents[url] = content

    # Combine contexts
    combined_context = "\n\n".join(url_contents.values())
    
    # Get GPT's response
    response = get_gpt_response(prompt, combined_context)
    
    return response, url_contents, combined_context

def create_interface():
    with gr.Blocks() as iface:
        gr.Markdown("# URL Content Analyzer with GPT")
        gr.Markdown("""
        Enter URLs and a prompt. The app will crawl the URLs, use the content as context, and generate a response using GPT. It will also display a summary of the content fetched from each URL.
        
        Before running the app, make sure to install the required packages:
        1. Open a command prompt in the project directory.
        2. Run the following command:
           ```
           pip install -U -r requirements.txt
           ```
        3. Set your OpenAI API key as an environment variable:
           ```
           set OPENAI_API_KEY=your_openai_api_key_here
           ```
        """)
        
        with gr.Row():
            urls_input = gr.Textbox(lines=5, label="Enter URLs (one per line)")
            prompt_input = gr.Textbox(lines=3, label="Enter your prompt")
        
        proxy_input = gr.Textbox(label="HTTP/HTTPS Proxy (optional, e.g., http://127.0.0.1:7897)", value="http://127.0.0.1:7897")
        
        submit_btn = gr.Button("Submit")
        
        gpt_response = gr.Textbox(label="GPT's Response")
        regenerate_btn = gr.Button("Regenerate Response")
        
        crawled_content = gr.Markdown(label="Crawled Content")
        
        # Hidden state to store the combined context
        combined_context_state = gr.State()
        
        def on_submit(urls, prompt, proxy):
            response, url_contents, combined_context = process_input(urls, prompt, proxy)
            
            # Format crawled content as a string
            content_summary = ""
            for url, content in url_contents.items():
                content_summary += f"### {url}\n"
                content_summary += content[:1000] + "...\n\n" if len(content) > 1000 else content + "\n\n"
            
            return response, content_summary, combined_context
        
        def on_regenerate(prompt, combined_context):
            new_response = get_gpt_response(prompt, combined_context)
            return new_response
        
        submit_btn.click(on_submit, inputs=[urls_input, prompt_input, proxy_input], outputs=[gpt_response, crawled_content, combined_context_state])
        regenerate_btn.click(on_regenerate, inputs=[prompt_input, combined_context_state], outputs=gpt_response)
    
    return iface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch(share=True)