# Challenge Name  
[REDACTED]

---

## Approach  

A straightforward steganography challenge using graphical obfuscation. The solution involved opening a redacted PDF in a vector graphics editor and removing visual elements that concealed the flag.

### Step 1: Initial Analysis  
- Received a PDF file with apparent redactions (black rectangles covering text).
- Opened the file in Inkscape to inspect its structure and contents.
- Immediately noticed that the black rectangles were graphical objects overlaying readable text beneath them.
- This suggested that the redaction was merely visual/graphical rather than true data obfuscation.

### Step 2: Core Technique  
- **Graphical Element Removal**: Used Inkscape's object selection and deletion tools to remove the black rectangle overlays.
- This technique was chosen because the redacted content appeared to be hidden by layered graphical elements rather than encrypted or encoded data.
- The key observation was that the rectangles were separate selectable objects, not part of the underlying text, making them easy to isolate and delete.

### Step 3: Implementation  
- Opened the PDF file `[REDACTED].pdf` in Inkscape.
- Identified the black rectangles covering the sensitive information.
- Selected each rectangle individually using Inkscape's selection tool.
- Deleted the selected rectangle objects, revealing the hidden text beneath.
- Repeated the process for all obstructing rectangles on the page.

### Step 4: Extraction  
- After removing all black rectangles, the complete flag was revealed: `root{EASY_2_UNREDACT}`
- The straightforward nature of the challenge emphasized that visual redaction alone is insufficient for true data security.

---

## Flag  

```
root{EASY_2_UNREDACT}
```

---

## Tools Used  

- Inkscape – PDF editing and graphical element manipulation
