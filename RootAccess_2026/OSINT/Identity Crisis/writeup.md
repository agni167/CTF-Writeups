# Challenge Name  
The Identity Crisis

---

## Approach  

This OSINT + web client-side challenge revolved around identifying the real person behind the handle "daemonized.u", finding their portfolio, and then reversing a hidden JavaScript check that only reveals the flag to the "true daemon".

### Step 1: Initial Analysis  
- From the description, we were given:
  - Target username: "daemonized.u".
  - Affiliation: Academic Society of Computer Engineers (ASCE), IIEST Shibpur.
  - Quote: "I am who I am".
  - The website treats everyone as "guest".
  - There is a dormant function in the client-side code waiting for the true daemon.
- This suggested two main directions:
  - Do OSINT on the username (and its variants) in the context of IIEST/ASCE.
  - Once the portfolio is found, examine its client-side JavaScript for any privilege/role checks and hardcoded secrets.

### Step 2: Core Technique  
- **Core Concept 1 – OSINT on usernames and college communities**  
  - Since the user was said to be an ASCE member at IIEST Shibpur, I first located the official ASCE IIEST Instagram: `asce.iiests`.
  - Then I looked for usernames similar to `daemonized.u` on Instagram (common place for portfolios and bios), trying variations like `daemonized_u`, `daemonizedu`, etc.
  - The key hit was `daemonized_u`, whose bio was exactly: "I am who I am." and whose profile linked to a portfolio site.

- **Core Concept 2 – Client-side JavaScript logic & base64 flag**  
  - The challenge line about “treats everyone as guest” and "true daemon" strongly hinted at some kind of role/identity logic implemented in JavaScript.
  - Once the portfolio site was found, I pulled its main JS bundle and searched it for keywords like `daemon`, `guest`, `flag`, and `atob`.
  - The presence of `atob()` and a conditional branch on a value equal to "daemon" indicated a base64-encoded flag only revealed when the client is recognized as the daemon.

### Step 3: Implementation  
- **Finding the portfolio and identity**
  - Using Instagram tooling (e.g., `instaloader`), I queried for various usernames including `daemonized_u`.
  - The `daemonized_u` profile contained:
    - Bio: "I am who I am."
    - External URL: `https://uttamm.web.app/`.
  - Visiting that URL revealed the portfolio of **Uttam Mahata**, B.Tech CST student at IIEST Shibpur, matching the ASCE/college clue.

- **Locating and analyzing the JavaScript bundle**
  - I fetched the main page HTML of `https://uttamm.web.app/` and extracted script tags to find the bundle, for example:
    - `/assets/index-CtPivjS7.js`.
  - I downloaded the JS file and searched for relevant patterns:
    - `daemon`
    - `guest`
    - `flag`
    - `atob`
  - Inside the bundle, I found logic structurally similar to:

    - Default identity token:
      - `localStorage.getItem("identity_token") || localStorage.setItem("identity_token", "guest");`
    - Conditional role check:
      - If some variable `m === "daemon"`, then the code calls `atob(d)` and sets a flag field:
        - `flag: atob(d)`.

- **Extracting the base64 value**
  - Nearby in the code, variable `d` was assigned a base64-looking string, e.g.:
    - `d = "cm9vdHsxXzRtX1doMF8xXzRtXzIwMjV9"`.
  - This string was clearly intended to be decoded using `atob()` (i.e., base64) to produce the secret flag for the daemon.

### Step 4: Extraction  
- I decoded the base64 string:
  - Base64 input: `cm9vdHsxXzRtX1doMF8xXzRtXzIwMjV9`.
  - Decoding it (via any base64 decoder) yielded:
    - `root{1_4m_Wh0_1_4m_2025}`.
- The resulting string clearly matches the CTF flag format.
- The middle segment `1_4m_Wh0_1_4m` is leetspeak for "I am who I am", tying back perfectly to the challenge’s text and the target’s Instagram bio.

---

## Flag  

```
root{1_4m_Wh0_1_4m_2025}
```

---

## Tools Used    
- **Cyber Chef** – To decode base64
