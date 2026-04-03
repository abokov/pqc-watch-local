# pqc-watch-local 🛡️⚛️

**pqc-watch-local** is a lightweight, cross-platform security agent designed to monitor Post-Quantum Cryptography (PQC) readiness on endpoints and cloud VMs. It focuses on "Pillar 1" of the PQC migration: **Cryptographic Inventory.**

With Google accelerating its PQC migration deadline to 2029 and NIST finalizing FIPS 203 (ML-KEM), visibility into legacy crypto usage is no longer optional—it's a compliance necessity.

## 🚀 Overview

This PoC addresses the "Harvest Now, Decrypt Later" (HNDL) threat by providing real-time visibility into:
1.  **Network Traffic:** Identifying whether TLS 1.3 handshakes are utilizing modern **ML-KEM (Kyber)** or falling back to quantum-vulnerable **RSA/ECC**.
2.  **System Binaries:** Scanning running processes for dynamically linked legacy libraries (OpenSSL < 3.0, older NSS) that lack native PQC support.

## 🏗️ Architecture: Pillar 1

The agent operates as a modular Python daemon with two primary engines:

### 1. Traffic Analysis Engine
* **Technology:** Pyshark / Scapy wrapper.
* **Function:** Monitors port 443 for `Client Hello` and `Server Hello` packets.
* **Logic:** Extracts `supported_groups` and `ciphersuites` to flag non-hybrid or non-PQC exchanges.

### 2. App Analysis Engine
* **Technology:** `psutil` + `ldd` (Linux) / `otool` (macOS).
* **Function:** Iterates through active PIDs to map memory-linked `.so` and `.dylib` files.
* **Logic:** Flags processes using versions of `libcrypto` or `libssl` that haven't been patched for the post-quantum era.

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.9+**
* **TShark / Wireshark:** The `pyshark` library requires the underlying TShark engine.
  * **macOS:** `brew install wireshark`
  * **Linux:** `sudo apt install tshark`

### Quick Start

1. **Clone the repo:**

```bash
   git clone [https://github.com/](https://github.com/)<your-username>/pqc-watch-local.git
   cd pqc-watch-local
```

2. **Run the setup script:**
Create virtual environment (venv) and install dependencies.

```Bash
chmod +x scripts/*.sh
./scripts/setup_env.sh
```
Then activate virtual environment

```Bash
source venv/bin/activate
``

3. **Launch the Agent:**

Note: Traffic analysis requires elevated privileges aka `sudo`  to bind to the network interfaces.

On Mac
```Bash
sudo ./scripts/run_agent_mac.sh
```

On Linux / your cloud virtual machine
```Bash
sudo ./scripts/run_agent_linux.sh
```

Sample of output 
```Plain
============================================================
PQC WATCH: SYSTEM SCAN REPORT (LEGACY CRYPTO DETECTED)
============================================================

[PID 120] Process: accessoryupdaterd
Patyh: /System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/accessoryupdaterd
--------------------
  - libcrypto: /usr/lib/libcrypto.35.dylib [PQC-READY]

[PID 1443] Process: ssh-agent
Path: /usr/bin/ssh-agent
--------------------
  - libcrypto: /usr/lib/libcrypto.46.dylib [PQC-READY]

[PID 3135] Process: node
Path: /usr/local/Cellar/node/25.6.1/bin/node
--------------------
  - libcrypto: /usr/local/opt/openssl@3/lib/libcrypto.3.dylib [PQC-READY]
  - libssl: /usr/local/opt/openssl@3/lib/libssl.3.dylib [PQC-READY]

[PID 3151] Process: node
Path: /usr/local/Cellar/node/25.6.1/bin/node
--------------------
  - libcrypto: /usr/local/opt/openssl@3/lib/libcrypto.3.dylib [PQC-READY]
  - libssl: /usr/local/opt/openssl@3/lib/libssl.3.dylib [PQC-READY]

============================================================
```


## ⚠️Todos 

While **pqc-watch-local** is PoC, whenever it provides essential endpoint visibility, it is important to note:
* **TLS 1.3 Encryption:** Since server certificates are encrypted in TLS 1.3, this agent identifies the **Key Exchange** (ML-KEM vs RSA), but it cannot verify the **Certificate Signature Algorithm** without an enterprise MITM proxy. 
* **Static vs. Dynamic:** This version focuses on *running* processes. A full inventory should complement this with static filesystem scans.

## 📈 Roadmap 
- [ ] Windows support via ETW (Event Tracing for Windows).
- [ ] Integration with centralized SIEM/Splunk via JSON logging.
- [ ] Hybrid-mode detection for IKEv2/IPsec.
- [ ] Automated alerting for legacy TLS 1.2 fallback.

---
*Created as a Proof of Concept for Post-Quantum visibility in the 2026 threat landscape.*

