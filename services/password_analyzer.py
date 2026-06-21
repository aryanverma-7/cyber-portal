import re
import math
import random
import string
from services.ai_service import CyberShieldAI

class PasswordAnalyzer:
    """Password strength analysis and generation engine"""
    
    def __init__(self):
        self.common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            '111111', '123456789', '1234', 'password1', 'password123',
            'admin', 'letmein', 'welcome', 'monkey', 'login'
        ]
    
    def analyze_password(self, password):
        """Analyze password strength and provide recommendations"""
        if not password:
            return {
                'strength': 'Invalid',
                'score': 0,
                'entropy': 0,
                'crack_time': 'Instant',
                'issues': ['Password is empty'],
                'suggestions': ['Enter a password to analyze']
            }
        
        score = 0
        issues = []
        suggestions = []
        
        # Length check (0-25 points)
        length = len(password)
        length_score = min(length * 2, 25)
        score += length_score
        
        if length < 8:
            issues.append('Password is too short (minimum 8 characters)')
            suggestions.append('Increase length to at least 12 characters')
        elif length < 12:
            suggestions.append('Consider using 16+ characters for better security')
        
        # Character variety check (0-40 points)
        variety = 0
        if re.search(r'[a-z]', password):
            variety += 1
        if re.search(r'[A-Z]', password):
            variety += 1
        if re.search(r'[0-9]', password):
            variety += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>_+=\[\]\\;\'`-]', password):
            variety += 1
        
        variety_score = variety * 10
        score += variety_score
        
        if variety < 2:
            issues.append('Password lacks character variety')
            suggestions.append('Mix uppercase, lowercase, numbers, and special characters')
        elif variety < 3:
            suggestions.append('Add more character types for stronger security')
        
        # Pattern check (0-20 points)
        pattern_score = 20
        
        # Check for sequences
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            pattern_score -= 10
            issues.append('Contains alphabetic sequence')
            suggestions.append('Avoid sequential letters like abc, xyz')
        
        if re.search(r'(123|234|345|456|567|678|789|890)', password):
            pattern_score -= 10
            issues.append('Contains numeric sequence')
            suggestions.append('Avoid sequential numbers like 123, 789')
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            pattern_score -= 5
            issues.append('Contains repeated characters')
            suggestions.append('Avoid repeating the same character multiple times')
        
        score += pattern_score
        
        # Common password check (0-15 points)
        if password.lower() in self.common_passwords:
            score -= 15
            issues.append('This is a commonly used password')
            suggestions.append('Use a unique password not found in common password lists')
        else:
            score += 15
        
        # Calculate entropy
        entropy = self.calculate_entropy(password)
        
        # Calculate crack time
        crack_time = self.estimate_crack_time(entropy)
        
        # Determine strength
        if score >= 80:
            strength = 'Very Strong'
        elif score >= 60:
            strength = 'Strong'
        elif score >= 40:
            strength = 'Medium'
        elif score >= 20:
            strength = 'Weak'
        else:
            strength = 'Very Weak'
        
        score = max(0, min(100, score))
        
        if not suggestions:
            suggestions.append('Password meets security requirements')
        
        return {
            'strength': strength,
            'score': score,
            'entropy': entropy,
            'crack_time': crack_time,
            'issues': issues,
            'suggestions': suggestions,
            'length': length,
            'variety': variety
        }
    
    def calculate_entropy(self, password):
        """Calculate password entropy using Shannon entropy formula"""
        if not password:
            return 0
        
        # Calculate character set size
        char_set_size = 0
        if re.search(r'[a-z]', password):
            char_set_size += 26
        if re.search(r'[A-Z]', password):
            char_set_size += 26
        if re.search(r'[0-9]', password):
            char_set_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            char_set_size += 32
        
        if char_set_size == 0:
            return 0
        
        # Entropy = length * log2(charset_size)
        entropy = len(password) * math.log2(char_set_size)
        
        return round(entropy, 2)
    
    def estimate_crack_time(self, entropy):
        """Estimate time to crack password based on entropy"""
        if entropy == 0:
            return 'Instant'
        
        # Assumptions: 1 billion guesses per second (modern GPU)
        guesses_per_second = 10**9
        total_combinations = 2 ** entropy
        
        seconds = total_combinations / guesses_per_second / 2  # Average case
        
        if seconds < 1:
            return 'Instant'
        elif seconds < 60:
            return f'{seconds:.1f} seconds'
        elif seconds < 3600:
            return f'{seconds/60:.1f} minutes'
        elif seconds < 86400:
            return f'{seconds/3600:.1f} hours'
        elif seconds < 31536000:
            return f'{seconds/86400:.1f} days'
        elif seconds < 3153600000:
            return f'{seconds/31536000:.1f} years'
        elif seconds < 315360000000:
            return f'{seconds/31536000:.1f} centuries'
        else:
            return 'Billions of years'
    
    def generate_password(self, length=16, use_upper=True, use_lower=True, 
                         use_numbers=True, use_special=True):
        """Generate a strong random password"""
        characters = ''
        
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        if use_numbers:
            characters += string.digits
        if use_special:
            characters += '!@#$%^&*(),.?":{}|<>_-+=\[\]\\;\'`'
        
        if not characters:
            characters = string.ascii_lowercase
        
        # Generate password
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # Ensure variety
        if use_upper and not re.search(r'[A-Z]', password):
            password += random.choice(string.ascii_uppercase)
        if use_numbers and not re.search(r'[0-9]', password):
            password += random.choice(string.digits)
        if use_special and not re.search(r'[!@#$%^&*]', password):
            password += random.choice('!@#$%^&*')
        
        return password[:length] if len(password) > length else password