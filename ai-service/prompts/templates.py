SYSTEM_PROMPT = """You are a seasoned penetration testing expert AI. Your goal is to analyze vulnerabilities and provide actionable insights.
Always respond in valid JSON format. Do not include markdown formatting like ```json in your response. Just the JSON object.
"""

DESCRIBE_PROMPT = """Analyze the following vulnerability and provide a structured description.
Vulnerability: {vulnerability}

Return a JSON object with this exact schema:
{{
    "title": "Clear title (e.g. SQL Injection in Login)",
    "details": "Detailed description of the vulnerability"
}}
"""

RECOMMEND_PROMPT = """Analyze the following vulnerability.
Vulnerability: {vulnerability}

Return a JSON object with this exact schema:
{{
    "title": "Clear title (e.g. SQL Injection in Login)",
    "severity": "LOW|MEDIUM|HIGH|CRITICAL"
}}
"""

REPORT_PROMPT = """Generate a report finding from the provided input. If a project name is mentioned, extract it. Otherwise use 'Unknown Project'.
Input: {input_data}

Return a JSON object with this exact schema:
{{
    "project_name": "Project Name (e.g. Banking Application)",
    "finding": "Detailed finding description"
}}
"""
