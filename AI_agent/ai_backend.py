#!/usr/bin/env python3
"""
AI Backend for SKARAB_BINGO project.
This module interacts with the DeepSeek API to answer user questions about the project.
"""

import os
import json
import requests
import traceback
import re
from pathlib import Path


class AIAssistant:
    def __init__(self, analysis_file='project_analysis.json', project_root='../'):
        self.analysis_file = Path(analysis_file)
        self.project_root = Path(project_root).resolve()
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        self.project_context = self._load_analysis()
        
    def _load_analysis(self):
        """Load the project analysis JSON file."""
        try:
            if self.analysis_file.exists():
                with open(self.analysis_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"Warning: Analysis file {self.analysis_file} not found.")
                return {}
        except Exception as e:
            print(f"Error loading analysis file: {e}")
            return {}
    
    def _read_file_content(self, relative_path, max_chars=2000):
        """Read the content of a file given its relative path."""
        try:
            file_path = self.project_root / relative_path
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Limit content size to prevent token overflow
                if len(content) > max_chars:
                    content = content[:max_chars] + "\n\n... (content truncated) ..."
                return content
            else:
                return f"File not found: {relative_path}"
        except Exception as e:
            return f"Error reading file {relative_path}: {str(e)}"
    
    def _find_relevant_file(self, query):
        """Find the most relevant file based on the user query."""
        # Simple keyword matching for now
        # In a more sophisticated implementation, this could use embeddings or other NLP techniques
        
        query_lower = query.lower()
        relevant_files = []
        
        def search_in_directory(directory_info, path_prefix=""):
            if 'files' in directory_info:
                for filename, file_info in directory_info['files'].items():
                    full_path = path_prefix + filename
                    
                    # Check if query keywords match file content or name
                    if any(keyword in full_path.lower() for keyword in query_lower.split()):
                        relevant_files.append((full_path, file_info))
                    
                    # Check in file info
                    file_str = json.dumps(file_info).lower()
                    if any(keyword in file_str for keyword in query_lower.split()):
                        relevant_files.append((full_path, file_info))
            
            # Recursively search subdirectories
            if 'subdirectories' in directory_info:
                for subdir_name, subdir_info in directory_info['subdirectories'].items():
                    search_in_directory(subdir_info, path_prefix + subdir_name + "/")
        
        if self.project_context and 'root_directory' in self.project_context:
            search_in_directory(self.project_context['root_directory'])
        
        return relevant_files[:3]  # Return top 3 matches
    
    def _prepare_context(self, query):
        """Prepare context for the AI model based on the query."""
        context = {
            "project_name": self.project_context.get("project_name", "SKARAB_BINGO"),
            "project_overview": "This is a radio astronomy project using SKARAB hardware platform with FPGA-based digital backends for processing astronomical signals.",
            "relevant_files": self._find_relevant_file(query)
        }
        return context
    
    def _build_prompt(self, query, context):
        """Build the prompt for the AI model."""
        prompt = f"""You are an AI assistant specialized in the SKARAB_BINGO radio astronomy project. 
This project involves FPGA-based digital backends for processing astronomical signals using SKARAB hardware.

Project Context:
- Project Name: {context.get('project_name')}
- Overview: {context.get('project_overview')}

"""
        
        # Add information about relevant files if found
        relevant_files = context.get('relevant_files', [])
        if relevant_files:
            prompt += "Relevant files related to the query:\n"
            for file_path, file_info in relevant_files:
                prompt += f"\nFile: {file_path}\n"
                if 'estimated_purpose' in file_info:
                    prompt += f"Purpose: {file_info['estimated_purpose']}\n"
                if 'docstring' in file_info and file_info['docstring']:
                    prompt += f"Description: {file_info['docstring'][:300]}...\n"
                
                # If we have the relative path, include the file content
                if 'relative_path' in file_info:
                    file_content = self._read_file_content(file_info['relative_path'])
                    prompt += f"File Content:\n```\n{file_content}\n```\n"
        
        prompt += f"""

User Question: {query}

Please provide a helpful and accurate response based on the project context. 
If the question relates to specific files, reference those files in your response.
Answer in the user's preferred language.
"""
        
        return prompt
    
    def query_ai_stream(self, user_question):
        """Query the AI model with a user question and return a streaming response."""
        if not self.api_key:
            yield "data: Error: DEEPSEEK_API_KEY environment variable not set.\n\n"
            return
        
        try:
            # Prepare context
            context = self._prepare_context(user_question)
            
            # Build prompt
            prompt = self._build_prompt(user_question, context)
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant specialized in radio astronomy and FPGA programming."},
                    {"role": "user", "content": prompt}
                ],
                "stream": True  # Enable streaming
            }
            
            # Send request with streaming
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=(10, 30),  # 连接超时10秒，读取超时30秒
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        # Handle SSE format
                        if decoded_line.startswith('data: '):
                            data_str = decoded_line[6:]  # Remove 'data: ' prefix
                            if data_str.strip() == '[DONE]':
                                yield 'data: [DONE]\n\n'
                            else:
                                yield decoded_line + '\n\n'
                        else:
                            yield decoded_line + '\n'
            else:
                yield f"data: Error: API request failed with status code {response.status_code}. Response: {response.text}\n\n"
                
        except requests.exceptions.Timeout:
            yield "data: Error: Request to DeepSeek API timed out. Please check your network connection or try again later.\n\n"
        except requests.exceptions.ConnectionError:
            yield "data: Error: Failed to connect to DeepSeek API. Please check your network connection.\n\n"
        except Exception as e:
            error_traceback = traceback.format_exc()
            yield f"data: Error querying AI model: {str(e)}\nTraceback:\n{error_traceback}\n\n"
    
    def query_ai(self, user_question):
        """Query the AI model with a user question."""
        if not self.api_key:
            return "Error: DEEPSEEK_API_KEY environment variable not set."
        
        try:
            # Prepare context
            context = self._prepare_context(user_question)
            
            # Build prompt
            prompt = self._build_prompt(user_question, context)
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant specialized in radio astronomy and FPGA programming."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            # 发送请求并设置合理的超时时间
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=(10, 30)  # 连接超时10秒，读取超时30秒
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: API request failed with status code {response.status_code}. Response: {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: Request to DeepSeek API timed out. Please check your network connection or try again later."
        except requests.exceptions.ConnectionError:
            return "Error: Failed to connect to DeepSeek API. Please check your network connection."
        except Exception as e:
            error_traceback = traceback.format_exc()
            return f"Error querying AI model: {str(e)}\nTraceback:\n{error_traceback}"


def main():
    """Main function for testing the AI backend."""
    assistant = AIAssistant()
    
    # Test query
    test_query = "What does the pulsar_23mhz_conplot.py script do?"
    print("Testing with query:", test_query)
    response = assistant.query_ai(test_query)
    print("Response:")
    print(response)


if __name__ == '__main__':
    main()