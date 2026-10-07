import math
import re

REGEX_PATTERNS = {
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Access Key": r"([^A-Za-z0-9/+=])([A-Za-z0-9/+=]{40})([^A-Za-z0-9/+=])",
    "Google Cloud API Key": r"AIzaSy[A-Za-z0-9-_]{35}",
    "Yandex Cloud OAuth Token": r"y[0-1]_AgAAAA[A-Za-z0-9_-]{31}",
    "Telegram Bot Token": r"[0-9]{9,10}:[a-zA-Z0-9_-]{35}",
    "Slack Bot Token": r"xoxb-[0-9]{11,13}-[a-zA-Z0-9-]{24}",
    "Discord Bot Token": r"[MN][A-Za-z0-9]{23}\.[A-Za-z0-9-_]{6}\.[A-Za-z0-9-_]{27}",
    "GitHub Personal Access Token (Classic)": r"ghp_[a-zA-Z0-9]{36}",
    "GitHub Fine-Grained Token": r"github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}",
    "GitLab Personal Access Token": r"glpat-[a-zA-Z0-9\-]{20}",
    "OpenAI API Key": r"sk-proj-[a-zA-Z0-9]{40}T3BlbkZK[a-zA-Z0-9]{20}",
    "Stripe Secret Key": r"sk_live_[0-9a-zA-Z]{24}",
    "Connection String (PostgreSQL)": r"postgres(ql)?://[a-zA-Z0-9-_]+:[a-zA-Z0-9-_]+@[a-zA-Z0-9.-]+:[0-9]+/[a-zA-Z0-9-_]+",
    "Generic Secret Keyword": r"(password|secret|passwd|api_key|private_key|token)\s*=\s*['\"][a-zA-Z0-9-_=!@#$%^&*()]{8,}['\"]"
}

def calculate_entropy(text: str) -> float:
    '''calculates entropy of text'''
    if not text:
        return 0.0
    entropy = 0.0
    frequencies = {char: text.count(char) / len(text) for char in set(text)}
    for frequency in frequencies.values():
        entropy -= frequency * math.log2(frequency)
    return entropy

def scan_line(line: str) -> dict | None:
    '''scans line for secrets'''
    for name, pattern in REGEX_PATTERNS.items():
        if re.search(pattern, line, re.I):
            return {'type': 'Regex Match', 'reason': f'Found pattern: {name}'}

    words = re.findall(r"['\"]([a-zA-Z0-9-_=]{12,})['\"]", line)
    for word in words:
        entropy = calculate_entropy(word)
        if entropy > 4.5:
            return {'type': 'High entropy', 'reason': f'Suspicious string with entropy: {entropy}'}
    
    return None