#!/usr/bin/env python3
"""
Analyzer module for SKARAB_BINGO project.
This module analyzes .py, .tex, .txt and README files in the project directory
and creates a JSON file describing the functionality of each file and folder.
"""

import os
import json
import ast
import re
from pathlib import Path


class ProjectAnalyzer:
    def __init__(self, project_root='../'):
        self.project_root = Path(project_root).resolve()
        self.analysis_results = {}
        
    def analyze_python_file(self, file_path):
        """Analyze a Python file and extract key information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST to get function and class definitions
            tree = ast.parse(content)
            
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'line_count': node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else None
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
            
            # Try to extract main purpose from docstring or comments
            docstring = ast.get_docstring(tree)
            comments = re.findall(r'# *(.*)', content[:500])  # First 500 chars
            
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'python',
                'size': os.path.getsize(file_path),
                'functions': functions,
                'classes': classes,
                'docstring': docstring,
                'initial_comments': comments[:5],  # First 5 comments
                'estimated_purpose': self._estimate_purpose(content, docstring, comments),
                'relative_path': relative_path  # Add relative path
            }
        except Exception as e:
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'python',
                'error': str(e),
                'size': os.path.getsize(file_path),
                'relative_path': relative_path  # Add relative path
            }
    
    def analyze_tex_file(self, file_path):
        """Analyze a LaTeX file and extract key information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract sections
            sections = re.findall(r'\\section\{([^}]*)\}', content)
            subsections = re.findall(r'\\subsection\{([^}]*)\}', content)
            
            # Extract title
            title_match = re.search(r'\\title\{([^}]*)\}', content)
            title = title_match.group(1) if title_match else None
            
            # Extract abstract
            abstract_match = re.search(r'\\abstract\{([^}]*)\}', content)
            abstract = abstract_match.group(1) if abstract_match else None
            
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'latex',
                'size': os.path.getsize(file_path),
                'title': title,
                'abstract': abstract,
                'sections': sections,
                'subsections': subsections[:10],  # Limit to first 10
                'estimated_purpose': abstract or title or ('Technical documentation about ' + (sections[0] if sections else 'the project')),
                'relative_path': relative_path  # Add relative path
            }
        except Exception as e:
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'latex',
                'error': str(e),
                'size': os.path.getsize(file_path),
                'relative_path': relative_path  # Add relative path
            }
    
    def analyze_text_file(self, file_path):
        """Analyze a text file and extract key information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get first few lines as summary
            lines = content.split('\n')
            first_lines = lines[:10]
            
            # Try to determine purpose from filename and content
            filename = os.path.basename(file_path).lower()
            purpose = "Text documentation file"
            
            if 'readme' in filename:
                purpose = "Project README file with general information"
            elif 'license' in filename:
                purpose = "License file"
            elif 'install' in filename or 'setup' in filename:
                purpose = "Installation or setup instructions"
            
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'text',
                'size': os.path.getsize(file_path),
                'first_lines': first_lines,
                'estimated_purpose': purpose,
                'relative_path': relative_path  # Add relative path
            }
        except Exception as e:
            # Get relative path from project root
            relative_path = os.path.relpath(file_path, self.project_root)
            
            return {
                'type': 'text',
                'error': str(e),
                'size': os.path.getsize(file_path),
                'relative_path': relative_path  # Add relative path
            }
    
    def _estimate_purpose(self, content, docstring, comments):
        """Estimate the purpose of a file based on its content."""
        # Look for keywords in docstring and comments
        content_lower = (docstring or '') + ' ' + ' '.join(comments[:3])
        content_lower = content_lower.lower()
        
        if 'skarab' in content_lower and 'adc' in content_lower:
            if 'spectrometer' in content_lower or 'spectrum' in content_lower:
                return "Spectrometer control script for SKARAB ADC boards"
            elif 'capture' in content_lower or 'sample' in content_lower:
                return "Data capture script for SKARAB ADC boards"
            else:
                return "SKARAB FPGA control script"
        elif 'casperfpga' in content_lower:
            return "CASPER FPGA control utilities"
        elif 'fft' in content_lower or 'spectrum' in content_lower:
            return "Signal processing and spectral analysis tool"
        else:
            return "Support script for radio astronomy data processing"
    
    def analyze_directory(self, dir_path):
        """Recursively analyze a directory and its files."""
        dir_info = {
            'name': os.path.basename(dir_path),
            'type': 'directory',
            'files': {},
            'subdirectories': {}
        }
        
        try:
            # Get relative path from project root
            relative_path = os.path.relpath(dir_path, self.project_root)
            dir_info['relative_path'] = relative_path
            
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                
                if os.path.isfile(item_path):
                    if item.endswith('.py'):
                        dir_info['files'][item] = self.analyze_python_file(item_path)
                    elif item.endswith('.tex'):
                        dir_info['files'][item] = self.analyze_tex_file(item_path)
                    elif item.endswith('.txt') or item.lower() == 'readme' or item.lower() == 'readme.md':
                        dir_info['files'][item] = self.analyze_text_file(item_path)
                elif os.path.isdir(item_path) and not item.startswith('.') and item != '__pycache__':
                    # Recursively analyze subdirectories
                    subdir_analysis = self.analyze_directory(item_path)
                    if subdir_analysis:  # Only add non-empty directories
                        dir_info['subdirectories'][item] = subdir_analysis
                        
        except Exception as e:
            dir_info['error'] = str(e)
            
        return dir_info
    
    def analyze_project(self):
        """Analyze the entire project and generate structured results."""
        print("Starting project analysis...")
        
        # Analyze root directory
        root_analysis = self.analyze_directory(self.project_root)
        
        # Add special handling for specific directories
        self.analysis_results = {
            'project_name': 'SKARAB_BINGO',
            'root_directory': root_analysis,
            'analysis_timestamp': str(Path().stat().st_mtime) if Path().exists() else 'unknown'
        }
        
        print("Project analysis completed.")
        return self.analysis_results
    
    def save_analysis(self, output_file='project_analysis.json'):
        """Save the analysis results to a JSON file."""
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        print(f"Analysis saved to {output_file}")
        
    def load_analysis(self, input_file='project_analysis.json'):
        """Load previously saved analysis results."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                self.analysis_results = json.load(f)
            return self.analysis_results
        except FileNotFoundError:
            print(f"Analysis file {input_file} not found.")
            return None


def main():
    analyzer = ProjectAnalyzer()
    results = analyzer.analyze_project()
    analyzer.save_analysis('project_analysis.json')
    print("Analysis complete. Results saved to project_analysis.json")


if __name__ == '__main__':
    main()