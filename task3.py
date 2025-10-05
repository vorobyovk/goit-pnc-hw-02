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

def polybius_square_cipher(text, key, mode='encrypt'):
    """Encrypts or decrypts the given text using a Polybius Square cipher."""
    key = key.upper()
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Note: 'J' is removed
    key_chars = "".join(sorted(set(key), key=key.index))  # Remove duplicates while preserving order
    grid_chars = key_chars + "".join(c for c in alphabet if c not in key_chars) 
    grid = [grid_chars[i:i + 5] for i in range(0, 25, 5)]
    char_map = {grid[i][j]: (i, j) for i in range(5) for j in range(5)}  # char to coordinates
    coord_map = {(i, j): grid[i][j] for i in range(5) for j in range(5)}

    # Create the Polybius Square grid
    if mode == 'encrypt':
        result = ''
        text = text.upper().replace('J', 'I')  # 'J' is treated as 'I'
        for char in text:
            if 'A' <= char <= 'Z':
                row, col = char_map[char]
                result += str(row + 1) + str(col + 1)  # 1-based indexing
            elif char == '\n':
                result += '\n'
            else:
                result += char  # Keep non-alphabetic characters unchanged
        return result
    elif mode == 'decrypt':
        result = ''
        text = text.upper()
        i = 0
        while i < len(text):
            if text[i].isdigit() and i + 1 < len(text) and text[i + 1].isdigit():
                row = int(text[i]) - 1
                col = int(text[i + 1]) - 1
                if 0 <= row < 5 and 0 <= col < 5:
                    result += coord_map[(row, col)]
                    i += 2
                else:
                    result += text[i]  # Append the digit if out of range
            else:
                result += text[i]  # Append the character if not a digit
            i += 1
        return result
    
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
    key_prefix = "TABLE_KEY = \""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: TABLE-KEY not found in config file.")
        return    
    table_key = key
    
    # Encrypt the text
    encrypted_text = polybius_square_cipher(text, table_key, 'encrypt')
    print("Encrypted text:", encrypted_text)
    print("Length of encrypted text:", len(encrypted_text))
    print("---------------------------------------------------------")
    # Decrypt the text      
    decrypted_text = polybius_square_cipher(encrypted_text, table_key, 'decrypt')
    print("Decrypted text:", decrypted_text)
    print("Length of decrypted text:", len(decrypted_text))

if __name__ == "__main__":
    main()