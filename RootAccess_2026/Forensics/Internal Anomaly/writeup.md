# Challenge Name

Internal Anomaly

---

# Approach

The challenge involved analyzing a packet capture file (root.pcapng) to uncover what an attacker obtained through encrypted channels. The solution required multiple stages: identifying suspicious network traffic patterns, discovering TLS session keys hidden in plain sight, decrypting encrypted communications, and extracting the flag from the decrypted content.

## Step 1: Initial Analysis

**Provided Files:**
- `root.pcapng` – A network packet capture file containing traffic from an anomalous workstation

**Initial Checks Performed:**
1. Examined the packet capture using tshark to get protocol statistics
2. Generated TCP conversation summaries to identify key data flows
3. Analyzed protocol hierarchy to understand traffic patterns

**Suspicious Findings:**
- Large volume of SSH traffic (15,791 frames, 1.6 MB) between 10.31.43.117 and 10.31.42.201 on port 22 — indicative of an attacker's interactive session
- Unusual HTTP request for `/runtime_cache.dat` served via Python SimpleHTTP/0.6 on port 8000
- HTTPS traffic on port 8443 to 10.31.42.158 with encrypted content
- Multiple small HTTP GET requests to various external IPs (likely reconnaissance or beaconing)

**Key Observation:**
The attacker downloaded a file called `runtime_cache.dat` which appeared to be binary/encrypted data, but the server was unencrypted HTTP.

## Step 2: Core Technique

**Main Concept: TLS Keylog Decryption**

The attacker exposed TLS session keys (SSLKEYLOGFILE format) within the `runtime_cache.dat` file. This is a standard format used by TLS/SSL implementations (Firefox, Chrome, OpenSSL with SSLKEYLOGFILE environment variable) to log session secrets for debugging purposes.

**Why This Method:**
- TLS 1.3 and modern TLS versions use forward secrecy, making passive decryption impossible without the session keys
- The attacker carelessly left the TLS keys in an unencrypted HTTP file accessible to network observers
- Once the keys were available, tshark's `-o "tls.keylog_file"` option could decrypt the entire TLS stream

**Key Observation:**
The runtime_cache.dat file contained 55 lines of TLS secrets in the format:
```
SERVER_HANDSHAKE_TRAFFIC_SECRET <hash1> <secret1>
CLIENT_HANDSHAKE_TRAFFIC_SECRET <hash1> <secret2>
SERVER_TRAFFIC_SECRET_0 <hash1> <secret3>
CLIENT_TRAFFIC_SECRET_0 <hash1> <secret4>
...
```

These corresponded to different TLS sessions established during the attack, allowing decryption of all encrypted communications.

## Step 3: Implementation

**Solving Process:**

1. **Extract and Parse the HTTP Stream:**
   ```bash
   tshark -r root.pcapng -q -z "follow,tcp,ascii,3030"
   ```
   This followed TCP stream 3030 (the runtime_cache.dat download) and revealed the TLS keylog data wrapped in HTTP response.

2. **Fix Key Log Format:**
   - The keylog lines were wrapped across multiple display lines
   - Created a Python script to rejoin wrapped lines:
     ```python
     # Join all continuation lines that don't start with a keyword
     fixed = re.sub(r'\n(?!SERVER_|CLIENT_|EXPORTER_)', '', full_text)
     ```
   - Output: 55 properly formatted TLS secrets in `/tmp/sslkeylog.txt`

3. **Decrypt TLS Traffic:**
   ```bash
   tshark -r root.pcapng -o "tls.keylog_file:/tmp/sslkeylog.txt" \
     -Y "http2 || http" -T fields ...
   ```
   - This revealed previously encrypted HTTP requests:
     - `GET /sys_health_report.log` to 10.31.42.158:8443 (frame 22534)

4. **Extract the Decrypted Content:**
   ```bash
   tshark -r root.pcapng -o "tls.keylog_file:/tmp/sslkeylog.txt" \
     -q -z "follow,tls,ascii,3"
   ```
   - Followed TLS stream 3 to see the full decrypted HTTP exchange

**Key Transformations:**
- Hex-wrapped TLS keylog → Properly formatted SSLKEYLOGFILE format
- Encrypted TLS application data → Decrypted HTTP plaintext
- System report response → Flag extraction

## Step 4: Extraction

**What Was Extracted:**
The decrypted HTTPS response contained a fake "System Health Summary" report from the attacker's exfiltrated data:

```
===== System Health Summary =====
Node: srv-prod-02
Timestamp: 2026-02-06 02:11:43

CPU Status: Normal
Memory Utilization: 73%
Disk Integrity: Verified
I/O Latency: Within threshold

audit_maker= ROOT{P4cK3T_4n4L7515_55ucC355F0L}

Scheduler: Active
Auto-healing: Enabled

===== End of Report =====
```

**Path to Flag:**
The flag was hidden in the `audit_maker` field of the decrypted system report. The attacker had exfiltrated this sensitive configuration value through an encrypted channel (HTTPS), but the encryption keys were left exposed in the packet capture.

The flag (converted to lowercase as required): **`root{p4ck3t_4n4l7515_55ucc355f0l}`**

---

# Flag

`root{p4ck3t_4n4l7515_55ucc355f0l}`

---

# Tools Used

**tshark** – Network packet analyzer used to extract and follow TCP streams, convert to ASCII format, and decrypt TLS traffic using the keylog file

**Python 3** – Script language used to parse and fix the wrapped TLS keylog format (regex substitution, line joining)

**xxd** – Hexdecimal viewer/converter (used for initial binary data inspection)

---

# Programming Language

**Python 3** (for TLS keylog parsing and formatting)
**Bash** (for tshark commands and terminal automation)

---
