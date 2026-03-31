# Challenge Name  
Gatekeeper

---

## Approach

### Step 1: Initial Analysis
- Connected gatekeeperto `nc gatekeep.rtaccess.app 9999`. The service requested repeated log entries; input was printed back with a format string-like structure.
- Ran format string probes (`%p`, `%6$p`, `%7$s`) to map argument offsets and leaks. Noticed GOT entries (0x404018/0x404020/0x404028/0x404030) still pointed into .text, so I could read them without libc resolves.
- The buffer was 64 bytes (fgets limit), so every payload had to stay ≤63 bytes.

### Step 2: Core Technique
- Primary technique: **format string write** to redirect control flow. Instead of brute-forcing libc (ASLR + many candidates), I dumped .text via `%7$s` reads and found a built-in “win” routine at `0x4012b6` that loads `/bin/sh` and calls `system`.
- Key observation: uninitialized GOT slots pointed to nearby `.text` addresses (`0x401030`, `0x401040`, `0x401060`). Overwriting any of them with the win address would lead to `system("/bin/sh")` on the next call, bypassing libc completely.

### Step 3: Implementation
- Crafted a `%hn` payload writing `0x12b6` (low two bytes of win address) to `GOT[0x404018]`. The format string `%1$4790c%8$hn` plus padding and the target address fit within 63 bytes.
- Sent `exit` after the write; the exit path invoked the function whose GOT entry was overwritten, so execution jumped to the win routine.
- Verified the shell by sending `id`/`echo`/`cat /flag*` commands.

### Step 4: Extraction
- The overwritten GOT call launched `/bin/sh` via the win function, providing an interactive shell.
- Running `cat /flag*` produced the flag below.

## Flag

```
root{i_w4n+_t0_br34k_fr33}
```

## Tools Used

- pwntools – formatted payload crafting, remote interaction, draining output.
