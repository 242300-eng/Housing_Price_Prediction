// Enhanced JavaScript for Housing Price Prediction

// Show loading animation on form submit
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function () {
            showLoading();
        });
    }

    // Add smooth scroll to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add hover effect to all buttons
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animate stats on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-value, .feature-card').forEach(el => {
        observer.observe(el);
    });
});

// Loading Animation Functions
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        createLoadingOverlay();
    } else {
        overlay.classList.add('active');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

function createLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'active';
    overlay.innerHTML = `
        <div style="text-align: center;">
            <div class="loading-spinner"></div>
            <p style="color: white; font-size: 1.2rem; font-weight: 600;">Calculating Price...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// FAQ Toggle Function
function toggleFAQ(id) {
    const answer = document.getElementById('faq-answer-' + id);
    const icon = document.getElementById('faq-icon-' + id);

    if (answer && icon) {
        if (answer.style.display === 'none' || answer.style.display === '') {
            answer.style.display = 'block';
            icon.textContent = '−';
        } else {
            answer.style.display = 'none';
            icon.textContent = '+';
        }
    }
}

// Add tooltips to form fields
function addTooltips() {
    const tooltips = {
        'city': 'Select the city where the property is located',
        'property_type': 'Choose the type of property you want to evaluate',
        'bhk': 'Number of bedrooms, hall, and kitchen',
        'area_sqft': 'Total built-up area in square feet',
        'locality_tier': 'Premium, Mid-Range, or Budget locality',
        'age_of_property': 'How old is the property',
        'furnishing': 'Furnishing status of the property'
    };

    Object.keys(tooltips).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.setAttribute('data-tooltip', tooltips[id]);
        }
    });
}

// Initialize tooltips on page load
document.addEventListener('DOMContentLoaded', addTooltips);

// Smooth number counter animation
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Add pulse animation to important elements
function addPulseToImportant() {
    const importantElements = document.querySelectorAll('.stat-value, #btn');
    importantElements.forEach(el => {
        el.classList.add('pulse-animation');
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    // Add pulse to important elements after a delay
    setTimeout(addPulseToImportant, 1000);
});

// Form validation enhancement
function validateForm() {
    const city = document.getElementById('city').value;
    const area = document.getElementById('area_sqft').value;

    if (!city) {
        alert('Please select a city!');
        return false;
    }

    if (!area || area <= 0) {
        alert('Please enter a valid area!');
        return false;
    }

    return true;
}

// Add form validation on submit
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            if (!validateForm()) {
                e.preventDefault();
                hideLoading();
            }
        });
    }
});


// AI Chatbot Logic
function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
        chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    const messages = document.getElementById('chat-messages');
    messages.innerHTML += `<div class="message user">${msg}</div>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    });
    const data = await response.json();
    const reply = data.reply || "Sorry, I'm having trouble understanding that.";

    setTimeout(() => {
        messages.innerHTML += `<div class="message bot">${reply}</div>`;
        messages.scrollTop = messages.scrollHeight;
    }, 500);
}

// Real-time Prediction Logic
function updateRealTimePrice() {
    const areaInput = document.getElementById('area_sqft');
    const areaVal = document.getElementById('area-val');
    const city = document.getElementById('city').value;

    if (areaInput && areaVal) {
        const area = areaInput.value;
        areaVal.innerText = area + ' sq.ft';

        if (city) {
            // Simple client-side estimation for real-time feel
            // In a real app, this would be an AJAX call to the model
            const baseRates = {
                "Mumbai": 18000,
                "Delhi NCR": 9000,
                "Bangalore": 10000,
                "Hyderabad": 7300,
                "Chennai": 8000,
                "Pune": 7500,
                "Kolkata": 7200,
                "Ahmedabad": 6000
            };
            const rate = baseRates[city] || 5000;
            const estimated = area * rate;
            const display = document.getElementById('real-time-val');
            if (display) {
                if (estimated >= 10000000) {
                    display.innerText = '₹' + (estimated / 10000000).toFixed(2) + ' Crore (Est.)';
                } else {
                    display.innerText = '₹' + (estimated / 100000).toFixed(2) + ' Lakh (Est.)';
                }
            }
        }
    }
}

// Initialize Slider Listeners
document.addEventListener('DOMContentLoaded', () => {
    const areaInput = document.getElementById('area_sqft');
    if (areaInput) {
        areaInput.addEventListener('input', updateRealTimePrice);
    }

    // Add Chatbot to body
    const botContainer = document.createElement('div');
    botContainer.id = 'ai-chatbot-widget';
    botContainer.innerHTML = `
        <button class="chatbot-toggle" onclick="toggleChat()">🤖</button>
        <div class="chat-window" id="chat-window">
            <div class="chat-header">🏠 AI Assistant</div>
            <div class="chat-messages" id="chat-messages">
                <div class="message bot">Hello! Ask me any property questions.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" class="chat-input" placeholder="Ask something..." onkeyup="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()" style="border:none; background:none; cursor:pointer;">🚀</button>
            </div>
        </div>
    `;
    document.body.appendChild(botContainer);
});
