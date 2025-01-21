from flask import Flask, render_template, request
import string

app = Flask(__name__)

class PlayfairCipher:
    def __init__(self):
        self.grid = []  # Grid will be set dynamically

    def create_grid(self, key):
        # Remove duplicate letters and replace 'J' with 'I'
        key = key.upper().replace("J", "I")
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        grid = []
        for char in key:
            if char not in grid and char in alphabet:
                grid.append(char)
        for char in alphabet:
            if char not in grid:
                grid.append(char)
        return grid

    def prepare_text(self, text):
        # Remove non-alphabetical characters and replace 'J' with 'I'
        text = text.upper().replace("J", "I")
        text = ''.join([char for char in text if char.isalpha()])
        
        # Split the text into pairs of two letters
        if len(text) % 2 != 0:
            text += 'X'  # Add an 'X' if the length is odd
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]
        return pairs

    def find_position(self, char):
        index = self.grid.index(char)
        return divmod(index, 5)

    def encrypt(self, plaintext, key):
        self.grid = self.create_grid(key)
        pairs = self.prepare_text(plaintext)
        encrypted_text = []
        
        for pair in pairs:
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])

            if row1 == row2:
                # Same row: shift columns
                encrypted_text.append(self.grid[row1 * 5 + (col1 + 1) % 5])
                encrypted_text.append(self.grid[row2 * 5 + (col2 + 1) % 5])
            elif col1 == col2:
                # Same column: shift rows
                encrypted_text.append(self.grid[((row1 + 1) % 5) * 5 + col1])
                encrypted_text.append(self.grid[((row2 + 1) % 5) * 5 + col2])
            else:
                # Rectangle: swap corners
                encrypted_text.append(self.grid[row1 * 5 + col2])
                encrypted_text.append(self.grid[row2 * 5 + col1])

        return ''.join(encrypted_text)

    def decrypt(self, ciphertext, key):
        self.grid = self.create_grid(key)
        pairs = self.prepare_text(ciphertext)
        decrypted_text = []

        for pair in pairs:
            row1, col1 = self.find_position(pair[0])
            row2, col2 = self.find_position(pair[1])

            if row1 == row2:
                # Same row: shift columns
                decrypted_text.append(self.grid[row1 * 5 + (col1 - 1) % 5])
                decrypted_text.append(self.grid[row2 * 5 + (col2 - 1) % 5])
            elif col1 == col2:
                # Same column: shift rows
                decrypted_text.append(self.grid[((row1 - 1) % 5) * 5 + col1])
                decrypted_text.append(self.grid[((row2 - 1) % 5) * 5 + col2])
            else:
                # Rectangle: swap corners
                decrypted_text.append(self.grid[row1 * 5 + col2])
                decrypted_text.append(self.grid[row2 * 5 + col1])

        # Remove trailing 'X' (if present) that was added for padding during encryption
        if decrypted_text[-1] == 'X':
            decrypted_text = decrypted_text[:-1]

        return ''.join(decrypted_text)


# Initialize the Playfair cipher class
cipher = PlayfairCipher()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        action = request.form.get('action')
        key = request.form.get('key')  # Get the key from the user

        if not key or len(key.strip()) == 0:
            result = "Error: Please provide a valid key."
        elif action == 'Encrypt':
            result = cipher.encrypt(text, key)
        elif action == 'Decrypt':
            result = cipher.decrypt(text, key)
        else:
            result = "Invalid action!"

        return render_template('index.html', result=result)

    return render_template('index.html', result='')


if __name__ == "__main__":
    app.run(debug=True)
