console.warn('SkyHack QuantumShield AI: Client-side WAF enabled. All activity is monitored.');

function blockMaliciousInput(input) {
    if (input.includes('<script>') || input.includes('SELECT * FROM')) {
        alert('Potential threat detected and blocked by QuantumShield AI!');
        return true;
    }
    return false;
}

document.addEventListener('DOMContentLoaded', function() {
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var inputs = form.querySelectorAll('input, textarea');
            for (var i = 0; i < inputs.length; i++) {
                if (blockMaliciousInput(inputs[i].value)) {
                    e.preventDefault();
                    console.warn('Blocked malicious input by QuantumShield AI.');
                    return false;
                }
            }
        });
    });
});

const CTF_FLAG = "flag{js_hidden_flag_2024}";

const feedMessages = [
    '<div class="text-success"><i class="fas fa-check-circle"></i> No threats detected</div>',
    '<div class="text-info"><i class="fas fa-user-shield"></i> Suspicious login blocked</div>',
    '<div class="text-warning"><i class="fas fa-exclamation-triangle"></i> All systems operational</div>',
    '<div class="text-danger"><i class="fas fa-bug"></i> Malicious payload blocked</div>',
    '<div class="text-primary"><i class="fas fa-shield-alt"></i> QuantumShield AI scan complete</div>',
    '<div class="text-warning"><i class="fas fa-user-secret"></i> Decoy admin login attempt detected</div>',
    '<div class="text-danger"><i class="fas fa-flag"></i> Honeypot endpoint accessed</div>',
    '<div class="text-info"><i class="fas fa-clipboard-list"></i> SIEM log downloaded by admin</div>',
    '<div class="text-warning"><i class="fas fa-fingerprint"></i> Biometric authentication failed</div>',
    '<div class="text-success"><i class="fas fa-rocket"></i> All flights on schedule</div>'
];
setInterval(function() {
    const idx = Math.floor(Math.random() * feedMessages.length);
    const feed = document.getElementById('security-feed-body');
    if (feed) feed.innerHTML = feedMessages[idx];
}, 4000); 