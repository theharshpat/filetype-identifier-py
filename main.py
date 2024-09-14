import base64
import binascii

def pad_base64(s):
    return s + b'=' * (-len(s) % 4)

BASE64HEADER_TYPES = {
    pad_base64(b"TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA+AAAAA4fug"): "exe",
    pad_base64(b"TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8AAAAA4fug"): "dll",
    pad_base64(b"TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6AAAAA4fug"): "sys",
    pad_base64(b"UEsDBBQAAAAIA"): "zip",
    pad_base64(b"UEsDBBQAAQAIA"): "zip (pwd protected)",
    pad_base64(b"H4sI"): "gz",
    pad_base64(b"N3q8ryccAAR"): "7z",
    pad_base64(b"UmFyIRoHAM"): "rar",
    pad_base64(b"JVBERi0xLjcNC"): "pdf",
    pad_base64(b"0M8R4KGxGuE"): "msi",
    pad_base64(b"TVNXSU0AAADQ"): "wim",
    pad_base64(b"UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA"): "apk",
    pad_base64(b"IyMjIw"): "tar",
    pad_base64(b"U29tZSBjb250ZW50"): "txt",
    pad_base64(b"Q0FJREZOT1JT"): "csv",
    pad_base64(b"PD94bWwgdmVyc2lvbj0"): "xml",
    pad_base64(b"dGV4dC9jc3M"): "css",
    pad_base64(b"ewogICAgIg"): "json",
    pad_base64(b"UEsDBBQAAQAIAA"): "docx",
    pad_base64(b"UEsDBBQAAAAIAA"): "xlsx",
    pad_base64(b"UEsDBBQAAAAIAI"): "pptx",
    pad_base64(b"PCFET0NUWVBFIGh0bWw+"): "html",
    pad_base64(b"UEsDBAoAAAAAAIAA"): "epub",
}

def get_file_type(filepath, num_bytes=50):
    try:
        # Read the first `num_bytes` bytes of the binary file
        with open(filepath, 'rb') as file:
            file_start = file.read(num_bytes)
        
        # Try to match with known binary headers
        for header, file_type in BASE64HEADER_TYPES.items():
            try:
                if file_start.startswith(base64.b64decode(header)):
                    return file_type
            except binascii.Error:
                continue  # Skip invalid base64 strings
        
        # If no match found, try to decode as base64
        try:
            decoded = base64.b64decode(file_start)
            # Check if the decoded content matches any known headers
            for header, file_type in BASE64HEADER_TYPES.items():
                try:
                    if decoded.startswith(base64.b64decode(header)):
                        return file_type
                except binascii.Error:
                    continue  # Skip invalid base64 strings
        except binascii.Error:
            pass  # Not a valid base64 string, continue to next check
        
        # If still no match, check for text-based files
        try:
            content = file_start.decode('utf-8').lower()
            if content.startswith('<?xml'):
                return 'xml'
            elif content.startswith('<!doctype html') or content.startswith('<html'):
                return 'html'
            elif content.startswith('{') and content.strip().endswith('}'):
                return 'json'
            elif content.startswith('@import') or content.startswith('.') or content.startswith('#'):
                return 'css'
        except UnicodeDecodeError:
            pass  # Not a text file, continue to next check
        
        # If all else fails, try to guess based on file extension
        file_extension = filepath.split('.')[-1].lower()
        if file_extension in ['txt', 'csv', 'json', 'xml', 'html', 'css']:
            return file_extension
    
    except IOError:
        return "Error: Unable to read file"
    
    return "Unknown file type"

# Example usage
file_path = '1jpg'
file_type = get_file_type(file_path)
print(f"The detected file type is: {file_type}")