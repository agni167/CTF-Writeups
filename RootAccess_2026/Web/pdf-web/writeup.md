# Challenge Name  
.pdf

---

## Approach  

A multi-stage challenge combining source code analysis, version control forensics, and cryptographic decoding. The solution involved inspecting page source, discovering a hidden GitHub repository, analyzing commit history for encoded data, and combining multiple decoding techniques to retrieve a remote resource containing the flag.

### Step 1: Initial Analysis  
- Inspected the HTML source code of the main challenge page.
- Discovered a GitHub repository link: `https://github.com/Asif-Tanvir-2006/rootaccess_web_chal_pdf/tree/main`
- Read the README.md file which contained a deliberate hint: *"ignore commit histories in your github repos before doing git push --force"*
- The hint explicitly pointed toward examining git commit history as the key to solving the challenge.
- This observation was crucial: the challenge instructed to examine what developers typically ignore (commit history), suggesting critical data was hidden in previous commits.

### Step 2: Core Technique  
- **Git Forensics**: Analyzed commit history to discover encoded data left in commit messages.
- **Base64 Decoding**: Decoded obfuscated URLs hidden in commit messages using Base64 encoding.
- **ROT13 Cipher**: Applied ROT13 decryption to further obscured decoded URLs.
- **Remote Resource Extraction**: Downloaded and analyzed a font file to extract embedded data.
- Why this approach: The challenge layered multiple obfuscation techniques—commit history, Base64, and ROT13—to hide a URL that pointed to a resource containing the flag. Each technique built upon the previous layer.

### Step 3: Implementation  
- Cloned the repository: `git clone https://github.com/Asif-Tanvir-2006/rootaccess_web_chal_pdf.git`
- Examined commit history: `git log --oneline`
- Identified Base64-encoded strings in commit messages:
  ```
  1725e55 dWdnY2Y6Ly9lbmoudHZndWhvaGZyZXBiYWcucGJ6L05mdnMtR25haXZlLTIwMDYvc2JhZ2Yvem52YS9zYmFnLmdncw==
  8622249 dWdnY2Y6Ly9lbmoudHZndWhvaGZyZXBiYWcucGJ6L05mdnMtR25haXZlLTIwMDYvc2JhZ2Yvem52YS9zYmFnLmdncw==
  ```
- Decoded Base64 using CyberChef: `dWdnY2Y6Ly9lbmoudHZndWhvaGZyZXBiYWcucGJ6L05mdnMtR25haXZlLTIwMDYvc2JhZ2Yvem52YS9zYmFnLmdncw==` → `uggcf://enj.tvguhohfrepbagrag.pbz/Nfvs-Gnaive-2006/sbagf/znva/sbag.ggs`
- Applied ROT13 cipher to the decoded result: `uggcf://enj.tvguhohfrepbagrag.pbz/Nfvs-Gnaive-2006/sbagf/znva/sbag.ggs` → `https://raw.githubusercontent.com/Asif-Tanvir-2006/fonts/main/font.ttf`
- Downloaded the font file from the decoded and decrypted URL.

### Step 4: Extraction  
- Extracted strings from the font file: `strings font.ttf`
- The flag was present in the font file metadata: `root{easy_if_u_follow}`
- The multi-layered obfuscation (commit history → Base64 → ROT13 → remote file) was designed to obscure the direct path to the flag, requiring understanding of both cryptographic encoding and git repository structure.

---

## Flag  

```
root{easy_if_u_follow}
```

---

## Tools Used  

- Git – Version control and commit history analysis
- CyberChef – Base64 and ROT13 decoding
- strings – String extraction from binary files
