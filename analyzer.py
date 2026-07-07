import math
import re


# ------------------------------
# Load Common Passwords
# ------------------------------

try:
    with open("common_passwords.txt", "r") as file:
        COMMON_PASSWORDS = set(
            line.strip().lower()
            for line in file
            if line.strip()
        )
except FileNotFoundError:
    COMMON_PASSWORDS = set()


# ------------------------------
# Entropy Calculation
# ------------------------------

def calculate_entropy(password):

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# ------------------------------
# Crack Time Estimate
# ------------------------------

def estimate_crack_time(entropy):

    guesses = 2 ** entropy

    guesses_per_second = 1_000_000_000

    seconds = guesses / guesses_per_second

    minute = 60
    hour = minute * 60
    day = hour * 24
    year = day * 365

    if seconds < 1:
        return "Instantly"

    elif seconds < minute:
        return f"{int(seconds)} seconds"

    elif seconds < hour:
        return f"{int(seconds/minute)} minutes"

    elif seconds < day:
        return f"{int(seconds/hour)} hours"

    elif seconds < year:
        return f"{int(seconds/day)} days"

    elif seconds < year * 1000:
        return f"{int(seconds/year)} years"

    else:
        return "Centuries"


# ------------------------------
# Main Analyzer
# ------------------------------

def analyze_password(password):

    score = 0

    suggestions = []

    length = len(password)

    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    # --------------------------
    # Length
    # --------------------------

    if length >= 16:
        score += 30

    elif length >= 12:
        score += 25

    elif length >= 8:
        score += 15
        suggestions.append(
            "Increase password length to at least 12 characters."
        )

    else:
        score += 5
        suggestions.append(
            "Password is too short."
        )

    # --------------------------
    # Uppercase
    # --------------------------

    if has_upper:
        score += 15
    else:
        suggestions.append(
            "Add uppercase letters."
        )

    # --------------------------
    # Lowercase
    # --------------------------

    if has_lower:
        score += 15
    else:
        suggestions.append(
            "Add lowercase letters."
        )

    # --------------------------
    # Numbers
    # --------------------------

    if has_digit:
        score += 15
    else:
        suggestions.append(
            "Add numbers."
        )

    # --------------------------
    # Symbols
    # --------------------------

    if has_special:
        score += 15
    else:
        suggestions.append(
            "Add special characters."
        )

    # --------------------------
    # Common Password
    # --------------------------

    common = password.lower() in COMMON_PASSWORDS

    if common:
        score -= 20
        suggestions.append(
            "Avoid common passwords."
        )

    # --------------------------
    # Repeated Characters
    # --------------------------

    repeated = bool(re.search(r"(.)\1{2,}", password))

    if repeated:
        score -= 10
        suggestions.append(
            "Avoid repeating characters."
        )

    # --------------------------
    # Sequential Characters
    # --------------------------

    sequences = [
        "1234",
        "abcd",
        "qwerty",
        "password",
        "admin"
    ]

    sequential = False

    lower = password.lower()

    for seq in sequences:

        if seq in lower:

            sequential = True

            score -= 10

            suggestions.append(
                "Avoid predictable words or sequences."
            )

            break

    # --------------------------
    # Entropy
    # --------------------------

    entropy = calculate_entropy(password)

    if entropy >= 80:
        entropy_level = "Excellent"

    elif entropy >= 60:
        entropy_level = "Strong"

    elif entropy >= 40:
        entropy_level = "Moderate"

    else:
        entropy_level = "Weak"

    # --------------------------
    # Final Strength
    # --------------------------

    if score >= 90:
        strength = "Very Strong"

    elif score >= 70:
        strength = "Strong"

    elif score >= 50:
        strength = "Moderate"

    elif score >= 30:
        strength = "Weak"

    else:
        strength = "Very Weak"

    score = max(0, min(score, 100))

    if score >= 90:
        color = "#16a34a"

    elif score >= 70:
        color = "#22c55e"

    elif score >= 50:
        color = "#eab308"

    elif score >= 30:
        color = "#f97316"

    else:
        color = "#ef4444"

    if score == 100:
        suggestions.append(
            "Excellent password!"
        )

    return {

        "score": score,

        "strength": strength,

        "color": color,

        "length": length,

        "entropy": entropy,

        "entropy_level": entropy_level,

        "crack_time": estimate_crack_time(entropy),

        "checks": {

            "uppercase": has_upper,

            "lowercase": has_lower,

            "number": has_digit,

            "special": has_special,

            "common_password": common,

            "repeated": repeated,

            "sequential": sequential
        },

        "suggestions": suggestions
    }