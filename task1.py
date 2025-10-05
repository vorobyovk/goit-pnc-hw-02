def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def vigenere_cipher(text, key, mode='encrypt'):    
    result = []
    key_len = len(key)
    for i, char in enumerate(text):
        key_char = key[i % key_len]
        key_shift = ord(key_char.lower()) - ord('a')

        if 'encrypt' == mode:
            shifted_char = chr(((ord(char.lower()) - ord('a') + key_shift) % 26) + ord('a'))
        elif 'decrypt' == mode:
             shifted_char = chr(((ord(char.lower()) - ord('a') - key_shift + 26) % 26) + ord('a'))
        else:
            raise ValueError("Invalid mode. Choose 'encrypt' or 'decrypt'.")
        
        # Keep the original case
        if char.isupper():
            shifted_char = shifted_char.upper()
        
        result.append(shifted_char)
    return ''.join(result)


def main():    
    text_file_path = "text.txt"
    config_file_path = "config.txt"

    text = read_file_content(text_file_path)
    if text is None:
        return

    config_content = read_file_content(config_file_path)
    if config_content is None:
        return

    # Extract key from config content
    key_prefix = "KEY-VEGINER=\""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: KEY-VEGINER not found in config file.")
        return
    
    # Encrypt the text
    encrypted_text = vigenere_cipher(text, key, 'encrypt')
    print("Encrypted text:", encrypted_text)

if __name__ == "__main__":
    main()
