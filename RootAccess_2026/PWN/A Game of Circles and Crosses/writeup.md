# Challenge Name  
A Game of Circles and Crosses

---

## Approach  

The challenge provides a buggy Tic-Tac-Toe game. Instead of fighting through client-side bugs, the solution involves understanding the verification protocol and directly submitting winning moves to the server.

### Step 1: Initial Analysis  
- Provided file: `bugs.py` – A Python Tkinter Tic-Tac-Toe game
- Ran static analysis on the code to understand game logic
- Key findings:
  - Game sends move proofs to `https://rootaccess.pythonanywhere.com/verify`
  - Board uses mixed data types (string `"3"` initial, integer `0` for player, `1` for computer)
  - Multiple bugs in win detection and cell occupancy validation
  - Moves are recorded as `{"x": column, "y": row}` coordinates

### Step 2: Core Technique  
- **Technique**: API Bypass / Direct Server Verification
- The client-side game has many bugs that cause incorrect win/loss detection
- Key observation: The verification happens server-side via HTTP POST request
- The server validates move sequences independently of the buggy client logic
- By crafting a valid winning move sequence and sending it directly to the API, we bypass all client bugs

### Step 3: Implementation  
- Analyzed how the game constructs the proof payload:
  ```python
  payload = {"v": 1, "nonce": random_hex, "human": moves_array}
  proof = base64_urlsafe_encode(json.dumps(payload))
  ```
- Crafted a winning move sequence (3 moves in a line)
- Sent POST request directly to verification endpoint with the proof

### Step 4: Extraction  
- Submitted winning moves for first column: `(0,0), (0,1), (0,2)`
- Server responded with `{"ok": true, "result": "player", "flag": "..."}`
- Multiple winning patterns work: rows, columns, and diagonals all return the flag

---

## Flag  

```
root{M@yb3_4he_r3@!_tr3@5ur3_w@$_th3_bug$_w3_m@d3_@l0ng_4h3_w@y}
```

---

## Tools Used  

- Python 3 – Script to craft and send verification payload
