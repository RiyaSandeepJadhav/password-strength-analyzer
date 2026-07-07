/**
 * Password Strength Analyzer - Flask API Integration Layer
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const generateBtn = document.getElementById('generateBtn');
    const generatedInput = document.getElementById('generatedPassword');
    const copyBtn = document.getElementById('copyBtn');
    
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    const scoreDisplay = document.getElementById('score');
    const lengthDisplay = document.getElementById('length');
    const entropyDisplay = document.getElementById('entropy');
    const entropyLevelDisplay = document.getElementById('entropyLevel');
    const crackTimeDisplay = document.getElementById('crackTime');
    
    // Checklist Items
    const checkUpper = document.getElementById('upper');
    const checkLower = document.getElementById('lower');
    const checkNumber = document.getElementById('number');
    const checkSpecial = document.getElementById('special');
    const checkCommon = document.getElementById('common');
    const checkRepeat = document.getElementById('repeat');
    const checkSequence = document.getElementById('sequence');
    
    const reuseWarning = document.getElementById('reuseWarning');
    const suggestionList = document.getElementById('suggestionList');

    // Debounce timer for real-time keystroke scanning
    let debounceTimer;

    // 1. Toggle Password Visibility
    togglePasswordBtn.addEventListener('click', () => {
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';
        togglePasswordBtn.innerHTML = isPassword ? '<i class="fa-solid fa-eye-slash"></i>' : '<i class="fa-solid fa-eye"></i>';
    });

// Locate the clear button element
const clearBtn = document.getElementById('clearBtn');

if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        // 1. Wipe out any text inside the password input fields
        passwordInput.value = '';
        if (typeof generatedInput !== 'undefined' && generatedInput) {
            generatedInput.value = '';
        }
        
        // 2. Fire your reset engine to restore all cards back to zero/waiting states
        resetAnalyzer();
    });
}
   
    // Manual Trigger Button
    analyzeBtn.addEventListener('click', () => {
        const value = passwordInput.value.trim();
        if (value) fetchAnalysis(value);
    });

    // 3. Connect to Flask Password Generator Endpoint
    generateBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/generate');
            const data = await response.json();
            
            if (data.password) {
                generatedInput.value = data.password;
                passwordInput.value = data.password;
                // Instantly pass generated item through analyzer pipeline
                fetchAnalysis(data.password);
            }
        } catch (error) {
            console.error('Error contacting generation server:', error);
        }
    });

    // 4. Clipboard Copy Helper with Visual Feedback State
    copyBtn.addEventListener('click', () => {
        if (!generatedInput.value) return;
        
        navigator.clipboard.writeText(generatedInput.value).then(() => {
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fa-solid fa-check" style="color: #16a34a;"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        }).catch(err => console.error('Failed to copy text: ', err));
    });

    // 5. API Fetch Wrapper targeting analyzer.py core logic
    async function fetchAnalysis(password) {
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password: password })
            });

            const data = await response.json();
            
            if (data.success) {
                updateUI(data);
            }
        } catch (error) {
            console.error('Error analyzing password properties:', error);
        }
    }

    // 6. Global UI Compiler Engine
    function updateUI(data) {
        // Core metrics display
        scoreDisplay.textContent = `${data.score} / 100`;
        lengthDisplay.textContent = data.length;
        entropyDisplay.textContent = `${data.entropy} bits`;
        entropyLevelDisplay.textContent = data.entropy_level;
        crackTimeDisplay.textContent = data.crack_time;
        
        // Bar Graphic Manipulation mapping to python output properties
        strengthFill.style.width = `${data.score}%`;
        strengthFill.style.backgroundColor = data.color;
        strengthText.textContent = data.strength;
        strengthText.style.color = data.color;

        // Map checklist nodes against data.checks object payload
        setCheckState(checkUpper, data.checks.uppercase, "Uppercase Letter");
        setCheckState(checkLower, data.checks.lowercase, "Lowercase Letter");
        setCheckState(checkNumber, data.checks.number, "Number");
        setCheckState(checkSpecial, data.checks.special, "Special Character");
        setCheckState(checkCommon, !data.checks.common_password, "Not Common Password");
        setCheckState(checkRepeat, !data.checks.repeated, "No Repeated Characters");
        setCheckState(checkSequence, !data.checks.sequential, "No Sequential Pattern");

        // Database reuse visibility panel toggle
        if (data.reuse) {
            reuseWarning.classList.remove('hidden');
        } else {
            reuseWarning.classList.add('hidden');
        }

        // Render Suggestions Advice Block
        renderSuggestions(data.suggestions);
    }

    // Helper: Build structured item lists dynamically
    function setCheckState(element, isSuccess, baseText) {
        if (isSuccess) {
            element.innerHTML = `✅ ${baseText}`;
            element.style.color = '#e2e8f0';
        } else {
            element.innerHTML = `❌ ${baseText}`;
            element.style.color = '#94a3b8';
        }
    }

    // Helper: Dynamic Advice Box Composer
    function renderSuggestions(suggestionsArray) {
        suggestionList.innerHTML = '';
        if (suggestionsArray.length === 0) {
            const li = document.createElement('li');
            li.textContent = "No warning flags flagged. Structurally secure entry matrix.";
            suggestionList.appendChild(li);
            return;
        }

        suggestionsArray.forEach(text => {
            const li = document.createElement('li');
            li.textContent = text;
            suggestionList.appendChild(li);
        });
    }

    // Helper: Revert UI states back to waiting when fields clear
    function resetAnalyzer() {
        strengthFill.style.width = '0%';
        strengthText.textContent = 'Waiting...';
        strengthText.style.color = '#cbd5e1';
        scoreDisplay.textContent = '0 / 100';
        lengthDisplay.textContent = '0';
        entropyDisplay.textContent = '0 bits';
        entropyLevelDisplay.textContent = '-';
        crackTimeDisplay.textContent = '-';
        reuseWarning.classList.add('hidden');
        suggestionList.innerHTML = '<li>Enter a password to begin analysis.</li>';
        
        setCheckState(checkUpper, false, "Uppercase Letter");
        setCheckState(checkLower, false, "Lowercase Letter");
        setCheckState(checkNumber, false, "Number");
        setCheckState(checkSpecial, false, "Special Character");
        setCheckState(checkCommon, true, "Not Common Password");
        setCheckState(checkRepeat, true, "No Repeated Characters");
        setCheckState(checkSequence, true, "No Sequential Pattern");
    }
});