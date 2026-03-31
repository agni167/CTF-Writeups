# Challenge Name
mid_aah_finguh
---
## Approach

Got a PNG image of Sukuna's cursed finger from JJK. The file was way too fat for a tiny image — 63 KB for 100x159 pixels. Tagged as reverse engineering, so obviously something's buried inside.

### Step 1: Initial Analysis

- Started with the usual checks:
  ```bash
  $ file middle_fingu.png
  middle_fingu.png: PNG image data, 100 x 159, 8-bit/color RGBA, non-interlaced

  $ ls -la middle_fingu.png
  -rw-r--r-- 1 krishna krishna 63488 middle_fingu.png
  ```
  63 KB for a 100x159 image is way too much. Something's definitely packed in here.

- Ran `strings` to see what's inside:
  ```bash
  $ strings middle_fingu.png
  ...
  WU9VX0NBTl9PTkxZX1VOTE9DS19NRV9XSEVOX0lfQU1fQVRfTVlfRlVMTF9QT1dFUg==
  ...
  /lib64/ld-linux-x86-64.so.2
  __cxa_finalize
  __libc_start_main
  ...
  noh this ain't the string dawg
  THE MIDDLE ONE IS THE BEST
  ...
  ```
  C++ symbols and Linux library references — there's an ELF binary hiding in the image. Also spotted that Base64 string.

- Decoded it:
  ```bash
  $ echo "WU9VX0NBTl9PTkxZX1VOTE9DS19NRV9XSEVOX0lfQU1fQVRfTVlfRlVMTF9QT1dFUg==" | base64 -d
  YOU_CAN_ONLY_UNLOCK_ME_WHEN_I_AM_AT_MY_FULL_POWER
  ```

- Did a `binwalk` to map out everything embedded:
  ```bash
  $ binwalk middle_fingu.png

  DECIMAL       HEXADECIMAL     DESCRIPTION
  -------------------------------------------------------
  0             0x0             PNG image
  0x6D0C        0x6D0C          ELF 64-bit LSB executable
  0xCA9C        0xCA9C          PDF document, version 1.7
  ```
  Three things hiding in one PNG: the image itself, an ELF binary, and a PDF.

### Step 2: Core Technique

- Extracted the ELF binary first and messed around with it:
  ```bash
  $ dd if=middle_fingu.png of=hidden.elf bs=1 skip=$((0x6D0C)) count=$((0xCA9C - 0x6D0C))
  $ chmod +x hidden.elf
  $ ./hidden.elf
  ```
  Found a `solve()` function that XORs `"noh this ain't the string dawg"` with user input, and a `kitne_fingers()` function that prints `"THE MIDDLE ONE IS THE BEST"`. Tried a bunch of XOR keys but nothing gave a valid flag. **Turns out it's a red herring.**

- The real target was the PDF. That Base64 hint — "YOU CAN ONLY UNLOCK ME WHEN I AM AT MY FULL POWER" — is a Jujutsu Kaisen reference. Sukuna reaches full power when all **20** cursed fingers are consumed. So the password had to be `20`.

### Step 3: Implementation

- Extracted the PDF:
  ```bash
  $ dd if=middle_fingu.png of=hidden.pdf bs=1 skip=$((0xCA9C))
  11964 bytes copied
  ```

- Tried opening it with PDF using password `20`:
  It worked.

- Pulled out the page content stream:
  ```python
  >>> page = pdf.pages[0]
  >>> content = page['/Contents'].read_bytes()
  >>> print(content.decode())
  BT
  /F1 24 Tf
  100 700 Td
  <37 2a 2a 31 3e 2f 2f 2e 37 76 23 76 37 76 2b 26 76 70 71 37 76 23 30 2b 38> Tj
  ET
  ```
  The text is rendered with Font F1 (UbuntuMonoNF) using hex-encoded glyph indices — not direct ASCII characters.

- Had to parse the ToUnicode CMap from the font to figure out the actual character mapping:
  ```python
  >>> font = page['/Resources']['/Font']['/F1']
  >>> cmap_stream = font['/ToUnicode'].read_bytes().decode()
  # parsed the beginbfchar mappings from the CMap
  ```
  After applying the mapping, the glyph string decoded to:
  ```
  7**1>//.7v#v7v+&vpq7v#0+8
  ```

- Knew the flag starts with `root{`, so XOR'd the first 5 chars against it to find the key:
  ```python
  >>> encoded = "7**1>//.7v#v7v+&vpq7v#0+8"
  >>> known = "root{"
  >>> for i in range(5):
  ...     print(f"{encoded[i]} ^ {known[i]} = {ord(encoded[i]) ^ ord(known[i])}")
  7 ^ r = 69 (0x45, 'E')
  * ^ o = 69
  * ^ o = 69
  1 ^ t = 69
  > ^ { = 69
  ```
  All 5 gave `0x45` — consistent single-byte XOR key.

- Applied XOR `0x45` to the whole string:
  ```python
  >>> flag = ''.join(chr(ord(c) ^ 0x45) for c in encoded)
  >>> print(flag)
  root{jjkr3f3r3nc354r3fun}
  ```

### Step 4: Extraction

- The ELF binary was a total rabbit hole — burned some time on it before pivoting to the PDF.
- Password `20` (Sukuna's 20 fingers = full power) unlocked the encrypted PDF.
- Font CMap decoding gave us the glyph-encoded string `7**1>//.7v#v7v+&vpq7v#0+8`.
- Single-byte XOR with key `0x45` cracked it: `root{jjkr3f3r3nc354r3fun}` — "JJK references are fun".

---

## Flag

```
root{jjkr3f3r3nc354r3fun}
```

---

## Tools Used

- file, strings, binwalk – Initial file analysis and embedded signature scanning
- dd – Extracting the ELF binary and PDF from the PNG
- Python – XOR key recovery
