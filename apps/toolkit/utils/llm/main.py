import packages
import json, re, os, asyncio
from toolkit.utils import utils, typer as t

def process_raw_content(
    input_path: str,
    output_path: str,
    custom_replacements: t.List[t.Tuple[str, t.Union[str, t.Callable]]] = None,
    encoding: str = 'utf-8',
    max_line_length: int = None,
    remove_empty_lines: bool = False,
    case: str = None,
    backup: bool = False
) -> dict:
    """
    Process the content of a text file by applying various cleaning and formatting operations.

    Args:
        input_path (str): The file path of the input text file to be processed.
        output_path (str): The file path where the processed content will be saved.
        custom_replacements (List[Tuple[str, Union[str, Callable]]], optional): List of (pattern, replacement) 
                                                       tuples for additional text replacements.
        encoding (str, optional): The encoding to use for reading/writing files. Defaults to 'utf-8'.
        max_line_length (int, optional): Maximum allowed line length. Lines exceeding this will be wrapped.
        remove_empty_lines (bool, optional): If True, removes all empty lines from the content.
        case (str, optional): Change the case of the text. Options: 'lower', 'upper', 'title', or None.
        backup (bool, optional): If True, creates a backup of the original file before processing.

    Returns:
        dict: A dictionary containing statistics about the processing:
              - 'input_lines': Number of lines in the input file
              - 'output_lines': Number of lines in the output file
              - 'characters_removed': Number of characters removed
              - 'lines_wrapped': Number of lines that were wrapped

    Raises:
        FileNotFoundError: If the input file does not exist.
        PermissionError: If there are insufficient permissions to read the input file
                         or write to the output file.
        IOError: If there's an error reading from the input file or writing to the output file.
        ValueError: If an invalid value is provided for the 'case' parameter.

    Example:
        >>> custom_replacements = [
        ...     (r'\d+', 'NUM'),  # Replace all numbers with 'NUM'
        ...     (r'[A-Z]+', lambda m: m.group(0).lower()),  # Convert all-caps words to lowercase
        ... ]
        >>> stats = process_raw_content('input.txt', 'output.txt', custom_replacements, 
        ...                             max_line_length=80, remove_empty_lines=True, case='lower')
        >>> print(f"Processed {stats['input_lines']} input lines to {stats['output_lines']} output lines.")
        >>> print(f"Removed {stats['characters_removed']} characters and wrapped {stats['lines_wrapped']} lines.")
    """
    def wrap_text(text: str, max_length: int) -> t.List[str]:
        """Wrap text to a maximum line length."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if current_length + len(word) + len(current_line) <= max_length:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    try:
        if backup and os.path.exists(input_path):
            backup_path = input_path + '.bak'
            os.replace(input_path, backup_path)
            print(f"Backup created: {backup_path}")

        with open(input_path, 'r', encoding=encoding) as file:
            content = file.read()

        original_length = len(content)
        original_lines = content.count('\n') + 1

        # Replace ".." with "." until no ".." remains
        content = re.sub(r'\.{2,}', '.', content)
        
        # Replace multiple newlines with a single newline
        content = re.sub(r'\n{2,}', '\n', content)
        
        # Replace double spaces with single spaces
        content = re.sub(r' {2,}', ' ', content)
        
        # Apply custom replacements
        if custom_replacements:
            for pattern, replacement in custom_replacements:
                content = re.sub(pattern, replacement, content)
        
        # Process lines
        lines = content.split('\n')
        processed_lines = []
        lines_wrapped = 0

        for line in lines:
            line = line.strip()
            if remove_empty_lines and not line:
                continue
            if max_line_length and len(line) > max_line_length:
                wrapped = wrap_text(line, max_line_length)
                processed_lines.extend(wrapped)
                lines_wrapped += len(wrapped) - 1
            else:
                processed_lines.append(line)

        # Apply case changes
        if case:
            if case == 'lower':
                processed_lines = [line.lower() for line in processed_lines]
            elif case == 'upper':
                processed_lines = [line.upper() for line in processed_lines]
            elif case == 'title':
                processed_lines = [line.title() for line in processed_lines]
            else:
                raise ValueError("Invalid case option. Choose 'lower', 'upper', or 'title'.")

        content = '\n'.join(processed_lines)
        
        with open(output_path, 'w', encoding=encoding) as file:
            file.write(content)
        
        return {
            'input_lines': original_lines,
            'output_lines': len(processed_lines),
            'characters_removed': original_length - len(content),
            'lines_wrapped': lines_wrapped
        }

    except FileNotFoundError:
        print(f"Error: The file {input_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to access {input_path} or {output_path}.")
    except IOError as e:
        print(f"Error: An I/O error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

async def parse_json(input_string):
    def clean_string(s):
        # Make this a regular function since string operations are relatively fast
        # Remove literal '\n' sequences and normalize actual newlines
        s = s.replace('\\n', '\n').strip()
        # Remove any leading/trailing whitespace from each line
        s = '\n'.join(line.strip() for line in s.split('\n'))
        return s
    
    def extract_code_block(s):
        try:
            start = s.index('```') + 3
            end = s.rindex('```')
            code_block = s[start:end].strip()
            
            # Remove the language identifier if present
            if '\n' in code_block:
                code_block = code_block.split('\n', 1)[1]
            else:
                code_block = code_block.split(None, 1)[-1]
            
            return code_block
        except ValueError:
            return s

    try:
        # Clean the input string first - now running synchronously
        cleaned_input = clean_string(input_string)
        
        # First attempt: try parsing the cleaned input directly
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None,
                json.loads,
                cleaned_input
            )
        except json.JSONDecodeError:
            # If direct parsing fails, try handling code blocks
            code_block = extract_code_block(cleaned_input)
            cleaned_code_block = clean_string(code_block)
            
            return await asyncio.get_event_loop().run_in_executor(
                None,
                json.loads,
                cleaned_code_block
            )
            
    except (ValueError, json.JSONDecodeError) as e:
        # Log the error asynchronously
        print(f"Failed to parse JSON: {input_string}")
        print(f"Error: {str(e)}")
        raise ValueError("Unable to parse input into a dictionary")
                    
async def convert_examples_to_string(examples: list[dict]):
    result = []
    for example in examples:
        if "User" in example:
            user_input = f'input: "{example["User"]}"'
        elif "Input" in example:
            user_input = f'input: "{example["Input"]}"'
        elif "input" in example:
            user_input = f'input: "{example["input"]}"'
            
        output = example.get("Output") or example.get("output")
        output_json = json.dumps(output, separators=(',', ':'))
        output_line = f'output: {output_json}'
        
        result.extend([user_input, output_line, ''])
    return '\n'.join(result).strip()

#*==============================================================================

import re
from typing import Union, Any, Literal, List

# Define valid modes
ProcessingMode = Literal[
    "remove_quotes",
    "remove_brackets", 
    "remove_special_characters",
    "remove_tokens" 
]

def post_process_deepseek_output(text: str) -> str:
    """
    Remove <think> tags and all content between them, handling any possible content.
    
    Args:
        text (str): Input text containing think tags
        
    Returns:
        str: Text with all think tags and their content removed
        
    Examples:
        >>> text1 = "Before\n<think>\nthinking content\n</think>\nAfter"
        >>> print(remove_think_tags(text1))
        'Before\nAfter'
        
        >>> text2 = "Start<think>one line</think>End"
        >>> print(remove_think_tags(text2))
        'StartEnd'
        
        >>> text3 = "<think>nested <think>tags</think> test</think>text"
        >>> print(remove_think_tags(text3))
        'text'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Handle nested tags first (if any)
    while re.search(r'<think>.*<think>.*?</think>.*?</think>', text, re.DOTALL):
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Remove any remaining think tags and their content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Clean up any extra newlines that might have been created
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

async def post_process_llm_output(
    text: Union[str, Any],
    mode: Union[ProcessingMode, List[ProcessingMode]] = "remove_quotes",
) -> str:
    """
    Post-process LLM output by removing specified characters.
    
    Args:
        text: Input text to process
        mode: Single mode string or list of modes. Valid modes:
            - "remove_quotes": Remove single and double quotes
            - "remove_brackets": Remove square and curly brackets
            - "remove_special_characters": Remove special characters while preserving
              basic punctuation (.,!?), spaces, and alphanumeric characters
            - "remove_tokens": Remove special tokens like <|eot_id|>, <|endoftext|>, etc.
            
    Returns:
        Processed text string with specified characters removed
            
    Raises:
        TypeError: If input text is not a string
        ValueError: If an invalid mode is provided
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Convert single mode to list for consistent processing
    modes = [mode] if isinstance(mode, str) else mode
    
    # Validate modes
    valid_modes = {"remove_quotes", "remove_brackets", "remove_special_characters", "remove_tokens"}
    invalid_modes = [m for m in modes if m not in valid_modes]
    if invalid_modes:
        raise ValueError(f"Invalid mode(s): {invalid_modes}. Valid modes are: {valid_modes}")
    
    # Define special characters pattern
    # Preserves: alphanumeric, basic punctuation (.,!?), spaces
    special_chars_pattern = r'[^a-zA-Z0-9\s.,!?]'
    
    # Define pattern for special tokens
    # Matches anything between <| and |>, including the delimiters
    token_pattern = r'<\|.*?\|>'
    
    for m in modes:
        if m == "remove_quotes":
            text = text.replace('"', '').replace("'", '')
        elif m == "remove_brackets":
            text = text.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
        elif m == "remove_special_characters":
            text = re.sub(special_chars_pattern, '', text)
        elif m == "remove_tokens":
            text = re.sub(token_pattern, '', text)
            
    return text

async def get_special_characters(text: str) -> set:
    """
    Get a set of all special characters in the input text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Set of special characters found in the text
    """
    return set(re.findall(r'[^a-zA-Z0-9\s]', text))

async def custom_character_removal(
    text: str,
    characters: Union[str, List[str]],
    preserve_chars: str = ".,!?"
) -> str:
    """
    Remove specific characters from text while preserving specified characters.
    
    Args:
        text: Input text to process
        characters: Single character or list of characters to remove
        preserve_chars: String of characters to preserve (default: basic punctuation)
        
    Returns:
        Processed text with specified characters removed
    """
    chars_to_remove = set(characters if isinstance(characters, list) else [characters])
    return ''.join(c for c in text if c not in chars_to_remove or c in preserve_chars)

#*==============================================================================
