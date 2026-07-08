# 🛡️ Password Strength Analyzer 

A sleek, lightweight web-based cybersecurity utility that evaluates user-entered passwords against cryptographic metrics, estimates brute-force vulnerability, and generates unguessable alternatives. 

This project was built to explore the interface between responsive web layouts and backend security primitives without relying on massive full-stack frameworks.

---

## ✨ Key Features

* **Structural Evaluation:** Scans inputs for basic rules (uppercase, lowercase, numbers, special characters) while flagging weak sequences or repeating patterns.
* **Cryptographic Metrics:** Calculates true mathematical randomness (**Entropy**) in bits and maps it to an overall strength score.
* **Threat Simulation:** Estimates an offline brute-force "Crack Time" against modern parallel-processing hardware executing 1 Billion guesses per second.
* **Secure Alternative Generator:** Generates high-chaos credentials utilizing cryptographically secure logic, complete with a fast, one-click clipboard copy utility.
* **Anti-Reuse Database Shield:** Features an history check that flags previous entries to prevent dangerous password reuse.

---

## 🧠 Core Security Concepts Learned & Applied

### 1. Information Entropy (Shannon's Formula)
Instead of just checking for arbitrary symbol swapping, the backend calculates entropy in bits using a variant of Shannon's formula:
$$E = L \times \log_2(R)$$
*(Where $L$ is length and $R$ is the character pool size).* 
This mathematically demonstrates why expanding password **length** increases security exponentially faster than adding complex characters.

### 2. One-Way Cryptographic Hashing (SHA-256)
Storing plain-text passwords is a massive security hazard. To build the history check safely, an SQLite database integration was used to store entries as irreversible 64-character hexadecimal signatures (**Pre-image Resistance**). If the database is ever leaked, the actual passwords cannot be reverse-engineered.

### 3. OS-Level Randomness (CSPRNG)
Standard random number generators are deterministic and guessable. The generator module leverages Python's `secrets` module (Cryptographically Secure Pseudo-Random Number Generation) to pull pure entropy from the host operating system, ensuring absolute forward secrecy.

---

## 🛠️ Built With

### Frontend (The Interface)
* **HTML5:** App architecture and layout mapping.
* **CSS3:** Custom responsive dark-mode styling utilizing Flexbox grid systems that adapt fluidly to desktop and mobile phone screens.
* **JavaScript (Vanilla):** Client-side interactivity (live password visibility toggles, text clears, and clipboard actions).

### Backend (The Brain)
* **Python:** Core computational engine handling data validation, regex parsing, and cryptographic algorithms.
* **Flask:** Lightweight micro-framework acting as the routing layer between the frontend and backend.
* **SQLite:** Local storage mechanism handling history token tracking.

---

## Screenshots

screenshot_1.png

screenshot_2.png

screenshot_3.png

Automatically_generrated_password.png

![Home Page](screenshot_1.png)
