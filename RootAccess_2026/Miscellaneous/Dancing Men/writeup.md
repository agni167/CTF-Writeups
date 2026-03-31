# Challenge Name  
Dancing Men

---

## Approach  

A multi-stage challenge combining file forensics, image reconstruction, and archive extraction. The solution required identifying a polyglot file, extracting an embedded ZIP archive, reconstructing shredded images through edge matching algorithms, and using the reconstructed message as a password to unlock the final flag.

### Step 1: Initial Analysis  
- Examined the provided files including `notSoImportant` and `dancing_men.zip`.
- Recognized `notSoImportant` as a polyglot file containing both JPEG data and embedded ZIP archive.
- Performed hex dump analysis to locate the ZIP signature within the polyglot file.
- Discovered the ZIP archive begins at offset `0xAA204`, with 4 extra padding bytes (`89 1f ff d9`) between the JPEG EOF marker and the actual ZIP signature.
- This observation was critical: standard ZIP extraction would fail without accounting for the polyglot structure and embedded offset.

### Step 2: Core Technique  
- **Polyglot File Extraction**: Identified and extracted embedded ZIP from a JPEG-ZIP hybrid file by locating the ZIP signature and skipping intermediate bytes.
- **Image Reconstruction via Edge Matching**: Used computational image analysis to reconstruct shredded images by calculating pixel differences between strip edges and greedily matching strips with minimal edge discontinuity.
- **Algorithm Details**: Built a cost matrix using Flate compression edge differences (comparing right edge of one strip with left edge of another), applied greedy reconstruction to build continuous chains, and performed swap optimization to improve ordering.
- Why this approach: The challenge required both low-level file forensics (handling polyglot files) and algorithmic image reconstruction (matching individual strips without metadata).

### Step 3: Implementation  
- **ZIP Extraction**:
  ```
  # Using Python
  with open('notSoImportant', 'rb') as f:
      f.seek(0xAA204 + 4)  # Skip offset and 4 padding bytes
      zip_data = f.read()
  with open('fixed.zip', 'wb') as out:
      out.write(zip_data)
  ```
  Or using `dd`:
  ```
  dd if=notSoImportant of=fixed.zip bs=1 skip=$((0xAA204 + 4))
  ```

- **Image Reconstruction**:
  - Loaded all shredded image strips from the directory
  - Built a cost matrix by calculating edge pixel differences for each potential strip ordering
  - Applied greedy algorithm: connected strips with minimal edge cost, avoiding cycles
  - Performed swap optimization over neighborhoods to refine the reconstruction
  - Merged strips into a continuous image using PIL

- **Password Extraction**:
  - Decoded the merged image to obtain the message: `thats_some_nerdy_stuff`
  - Applied the hint to convert to uppercase: `THATS_SOME_NERDY_STUFF`
  - Used this as the password to extract `fixed.zip`

### Step 4: Extraction  
- Extracted the password-protected archive
- Retrieved the flag file from within the ZIP archive from flag.txt
- The multi-layer challenge (polyglot extraction → image reconstruction → password-protected archive) tested both forensic analysis and algorithmic problem-solving skills.

---

## Flag  

```
root{3l3m3n74ry_my_d34r_w47s0n}
```

---

## Tools Used  

- hexdump – Binary file analysis and ZIP signature location
- dd – Binary data extraction with offset specification
- Python (PIL/Pillow) – Image loading and merging
- NumPy – Numerical calculations for edge matching algorithms
- 7-Zip – Password-protected archive extraction
- Custom Python script – Image reconstruction via greedy edge-matching algorithm
