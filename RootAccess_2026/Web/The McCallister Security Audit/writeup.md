# Challenge Name  
*The McCallister Security Audit*

---

## Approach  

A multi-stage steganography and metadata extraction challenge requiring careful analysis of web content, image metadata, and embedded archives. The solution involved discovering hidden data in image files and combining three flag fragments through various decryption techniques.

### Step 1: Initial Analysis  
- Accessed the webpage which returned a 403 Forbidden error.
- Inspected the HTML source and discovered a crucial hint in the comments: "Tip: Kevin always leaves a trail in the metadata of his photos."
- Downloaded the image `kevin_hallway.jpeg` from the website and analyzed it using `exiftool`.
- Found a page parameter in the image metadata: `page_id=0h_n0_i_f0rg0t`.

### Step 2: Core Technique  
- **Steganography and Metadata Extraction**: Used `exiftool` to read JPEG metadata revealing hidden information.
- **Image Steganalysis**: Employed `steghide` to extract password-protected hidden data from JPEG files.
- **Binary Analysis**: Used `binwalk` to identify and extract embedded ZIP archives from image files.
- **Cryptographic Decoding**: Applied Base64 decoding (via CyberChef) and ROT13 cipher to recover encrypted flag fragments.
- The multi-layered approach was necessary because the flag was split into three parts, each protected by different steganographic and cryptographic methods.

### Step 3: Implementation  
- Accessed the URL with the discovered page parameter: `https://homealone.fwh.is/?page_id=0h_n0_i_f0rg0t`
- Retrieved a Base64-encoded secret key: `Um9hZCBSdW5uZXIg`
- Decoded the Base64 string using CyberChef to obtain: `Road Runner`
- Downloaded two additional images: `worried_siblings.jpeg` and `buzz_final.jpeg`
- **Part 2 Extraction**: Executed `steghide -sf worried_siblings.jpeg` with password "Road Runner" to extract: `1606611d3e343e41000056000d5d51566708`
- **Part 1 Extraction**: Executed `binwalk -e buzz_final.jpeg` to extract embedded ZIP archive; used password "KevinMcAllister" to obtain: `370d0303293e5d18541c0d5e123b662a235a`
- Followed hints in the extracted `key_hint.txt` file which indicated ROT13 decryption for the final step.

### Step 4: Extraction  
- **Part 1** (from buzz_final.jpeg via binwalk): `370d0303293e5d18541c0d5e123b662a235a` (hex-encoded, decoded via key hints)
- **Part 2** (from worried_siblings.jpeg via steghide): `st3r_Pl4nn3r_2025}`
- **Part 3** (from key_hint.txt hints): Applied ROT13 to initial flag fragment to get `root{K3v1n_1s_4_M4`
- Combined all parts: `root{K3v1n_1s_4_M4` + `st3r_Pl4nn3r_2025}` = complete flag.

---

## Flag  

```
root{K3v1n_1s_4_M4st3r_Pl4nn3r_2025}
```

---

## Tools Used  

- exiftool – JPEG metadata extraction
- steghide – Steganography password-protected data extraction
- binwalk – Binary file analysis and embedded archive extraction
- CyberChef – Base64 decoding
- ROT13 Cipher – Flag fragment decryption