# Meme Madness
*(Obfuscation layers with song-locked secrets)*

---

## Approach

Provided ciphertext across media files and a hidden key; combined them via XOR to reveal the flag.

### Step 1: Initial Analysis
- Found three files: `challenge_video.mp4`, `nahi.jpeg`, and `Krish_ka_gana_sunega.webm`.
- Ran basic inspection (file listing, lengths, tail/header checks) and noted that both the MP4 and JPEG had extra data appended to their ends.
- Extracted the trailing 38 bytes from each file and observed that they looked like binary blobs suitable for XOR manipulation.

### Step 2: Core Technique
- Used XOR decoding since the instruction hinted that both appended blobs needed to be XORed together, and XOR is a standard way to reverse simple obfuscation between paired byte sequences.
- The key observation was the identical byte length at the tails and the hint pointing toward XOR, which made the approach appropriate for recovering the intermediate ciphertext.

### Step 3: Implementation
- Grabbed the last 38 bytes of `challenge_video.mp4` and `nahi.jpeg` in Python, then XORed them byte-for-byte to derive an intermediate result.
- Analyzed the tail of `Krish_ka_gana_sunega.webm` and discovered `KEY=Krish42`, so extracted `Krish42` as the repeated XOR key.
- Repeated the key across the intermediate ciphertext, XORed byte-for-byte, and decoded the resulting plaintext.

### Step 4: Extraction
- Extracted the hidden key `Krish42` from the `Krish_ka_gana_sunega.webm` file.
- Used that key to XOR-decrypt the previously derived ciphertext, which revealed the final flag `root{chuttamalle_spidey_is_vibin_hard}`.

---

## Flag

```
root{chuttamalle_spidey_is_vibin_hard}
```

---

## Tools Used

- Python – Extracted binary tails and performed the XOR operations.
- Programming Language: Python
