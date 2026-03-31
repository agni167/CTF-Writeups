# Challenge Name 
The Library Code

---

## Approach  

This challenge combines cryptanalysis with a clever encoding hint. The encrypted message must be decrypted using a Caesar cipher, but the shift key is hidden within the challenge description itself.

### Step 1: Initial Analysis  
- An encrypted message was provided in `encrypted_note.txt`: "Dro pvkq sc ss3cd5_vslbkbi"  
- The challenge description mentioned "IIEST Library Question Bank" with a specific IP address: **10.11.1.6**  
- The clue "Sum all the essence within" suggested aggregating numerical values.  
- The encrypted text contained both letters and numbers, indicating a substitution cipher that preserves non-alphabetic characters.

### Step 2: Key Derivation  
- The IP address 10.11.1.6 held the crucial hint for the decryption key.  
- Following the instruction to "sum all the essence within," all individual digits of the IP address were summed:  
  **1 + 0 + 1 + 1 + 1 + 6 = 10**  
- This derived value **10** became the Caesar cipher shift key.  
- The path to "access the treasure" was the key derivation process itself.

### Step 3: Core Technique  
- **Caesar Cipher Decryption** was identified as the appropriate method.  
- Each alphabetic character is shifted back by the derived key (10 positions) within the 26-letter alphabet.  
- The formula applied: `chr((ord(char) - shift - key) % 26 + shift)` where `shift` is the ASCII offset (65 for uppercase, 97 for lowercase).  
- The modulo 26 wrapping ensures characters cycle through the alphabet correctly.

### Step 4: Implementation  
- A Python script was written to:
  1. Iterate through each character in the encrypted text  
  2. For alphabetic characters, apply the Caesar cipher decryption with key=10  
  3. Preserve all non-alphabetic characters (numbers, special characters) unchanged  
- The decryption process systematically reversed the cipher applied during encoding.

### Step 5: Extraction  
- Decrypting the message revealed: **"The flag is ii3st5_library"**  
- The plaintext directly contained the flag within its message.  
- The words "ss3cd5_vslbkbi" decrypted to "ii3st5_library," representing the IIEST Library Question Bank.

---

## Flag  

```
root{ii3st5_library}
```

---

## Tools Used  

- Python – For implementing the Caesar cipher decryption algorithm