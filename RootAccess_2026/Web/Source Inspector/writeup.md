# Source Inspector

---

## Approach

Opened the site and immediately got hit with an anti-bot challenge. After getting past that, found a PHP file viewer with a blacklist filter on the `?page=` parameter. The trick was that the blacklist was case-sensitive but PHP stream wrappers aren't — so uppercase `PHP://FILTER` slipped right through and leaked the source of `flag.php`.

### Step 1: Initial Analysis
- Went to `https://evil.lovestoblog.com/` and got redirected by some anti-bot JS challenge. Checked the page source — it was setting an `__test` cookie using AES-128-CBC decryption with a `toNumbers()` function.
- Found the key (`f655ba9d09a112d4968c63579db590b4`) and IV (`98344c2eee86c3994890592585b49f80`) hardcoded in the JS. The ciphertext changes every request though. Had to solve this twice (two cookie challenges back-to-back) before the actual app loaded. 
- Once past the bot check, the app was basically a file viewer with `?page=` parameter. Had `hello.txt` and `about.txt` available.
- Poked around and found some useful hints:
  - HTML comment said: *"I tried including flag.php directly, but the screen was blank. Where did the text go?"*
  - `about.txt` mentioned: *"Sometimes we hide secrets in variables, but we forget how to read them back."*
  - Also found `/README.md` sitting right there on the server — confirmed the flag is in `flag.php` and there's a filter blocking "specific PHP keywords".

### Step 2: Core Technique
- Classic LFI with `php://filter` — tried `?page=flag.php` first but got a blank page. Makes sense, the file probably just defines `$flag` without printing it. So I needed the raw source code instead.
- Tried the usual `php://filter/read=convert.base64-encode/resource=flag.php` but it got blocked. The filter was catching lowercase `php`, `filter`, `://`, etc.
- Then it clicked — PHP stream wrappers are case-insensitive. The blacklist was only matching lowercase strings. So `PHP://FILTER` would work exactly the same way but wouldn't match the blocklist. Classic oversight.

### Step 3: Implementation
- For the anti-bot cookie: opened DevTools, grabbed the ciphertext hex from the 3rd `toNumbers()` call, took it to CyberChef, decrypted it with AES-128-CBC using the key/IV from the source, and set the result as the `__test` cookie in the browser. Did this twice to get past both challenges.
- For the actual exploit, just put this in the URL bar:
  ```
  https://evil.lovestoblog.com/?page=PHP://FILTER/read=convert.base64-encode/resource=flag.php
  ```
- Got back a base64 string on the page. Copied it and decoded it:
  ```bash
  echo "PD9waHAKJGZsYWcgPSAicm9vdHtwaHBfd3JhcHBlcnNfcjN2M2FsX3MzY3IzdHN9IjsKPz4K" | base64 -d
  ```

### Step 4: Extraction
- The decoded output was the PHP source:
  ```php
  <?php
  $flag = "root{php_wrappers_r3v3al_s3cr3ts}";
  ?>
  ```
- Flag was right there in the variable. The whole challenge boiled down to the blacklist being case-sensitive while PHP itself doesn't care about case for stream wrappers.

---

## Flag

```
root{php_wrappers_r3v3al_s3cr3ts}
```

---

## Tools Used

- Browser DevTools – Inspecting JS source, extracting AES ciphertext, setting cookies
- CyberChef – AES-128-CBC decryption for anti-bot bypass, Base64 decoding
- base64 (CLI) – Decoding the leaked PHP source
