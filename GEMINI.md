# Project Concept: pqc-watch-local
*(Note: Initially conceptualized as pqc-watched-desktop, renamed to support cloud VMs and local endpoints)*

## Pillar 1: The Local Agent (Traffic & Apps)

**The Concept:** A lightweight daemon that sits on endpoints, monitors outbound TLS handshakes, and scans local binaries for legacy crypto libraries.

**The PoC (Network Sniffing + Basic Binary Grep):**

* **Traffic Analysis:** Don't write a packet sniffer from scratch. Use a Python script wrapping pyshark (tshark under the hood) or scapy. Have it listen strictly to port 443. You are looking for the Client Hello and Server Hello packets to see if the negotiated cipher suites include ML-KEM (Kyber) or if they fall back to vulnerable RSA/ECC suites.
* **App Analysis:** For the PoC, stick to Linux (and Mac). Write a bash/Python script that uses `ldd` (or `otool`) to check dynamically linked libraries on running processes, flagging older versions of OpenSSL or NSS that pre-date PQC support.

**The Critical Gap:** Cross-platform agents are a nightmare. Windows requires different APIs (like ETW) than Mac or Linux. Furthermore, with TLS 1.3, the server certificate is encrypted. You can see the key exchange algorithms in the clear, but identifying the exact certificate signature algorithm requires deeper interception (like an enterprise MITM proxy), which a simple local agent can't do without breaking end-to-end encryption.
