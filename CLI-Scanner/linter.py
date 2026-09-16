import json
from datetime import datetime, timezone
import requests
from colorama import Fore, init
from rich.console import Console
from rich.table import Table

console = Console()

init(autoreset=True)

def save_issue(type, severity, line, message):
    issue = {
        "type": type,
        "severity": severity,
        "line": line,
        "message": message
    }
    return issue

def make_scan_meta(target_file, status, issues):
    scan_meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "target_file": str(target_file),
        "status": status,
        "total_issues": str(issues)
    }
    return scan_meta

def write_json_report(scan_meta, issues):
    report_data = {"scan_meta": scan_meta, "issues": issues}
    with open('report.json', 'w', encoding='utf-8') as file:
        json.dump(report_data, file, ensure_ascii=False, indent=2)

def check_dockerfile(file_path):
    issues = []
    has_user = False
    status = "FAILED"

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line_num, line in enumerate(lines, 1):
        if line.startswith('FROM'):
            if ':latest' in line:
                message = "Base image uses :latest tag."
                issue = save_issue("INSECURE_TAG", "WARNING", line_num, message)
                issues.append(issue)
                print(f'{Fore.YELLOW}[WARNING] Line {line_num}: {message}')
            elif ':' not in line:
                message = "Base image does not use any tag."
                issue = save_issue("MISSING_TAG", "WARNING", line_num, message)
                issues.append(issue)
                print(f'{Fore.YELLOW}[WARNING] Line {line_num}: {message}')
        elif line.startswith('ENV') or line.startswith('ARG'):
            has_sensitive_data = any(word in line.lower() for word in ['password', 'secret', 'token', 'key'])
            if has_sensitive_data:
                message = "Hardcoded sensitive data found."
                issue = save_issue("SECRET_LEAK", "CRITICAL", line_num, message)
                issues.append(issue)
                print(f'{Fore.RED}[CRITICAL] Line {line_num}: {message}')
        elif line.startswith('USER'):
            has_user = True

    if not has_user:
        message = "No USER instruction found. Container runs as root."
        issue = save_issue("MISSING_USER", "WARNING", None, message)
        issues.append(issue)
        print(f'{Fore.YELLOW}[WARNING] Global: {message}')

    if not issues:
        status = "SUCCEED"

    scan_meta = make_scan_meta(file_path, status, len(issues))
    write_json_report(scan_meta, issues)

    print(f'{Fore.GREEN}[SUCCESS] Scan finished. {len(issues)} issues found. Report saved to report.json.')


def check_requirements(file_path):
    packages = []
    issues = []
    status = "FAILED"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            line = line.split('\\')[0].split('--hash')[0].strip()

            if '==' in line:
                name, version = line.split('==')
                packages.append({'name': name.strip(), 'version': version.strip()})

    if not packages:
        print(f'{Fore.YELLOW}[WARNING] No packages found.')
        scan_meta = make_scan_meta(file_path, "SUCCEED", 0)
        write_json_report(scan_meta, [])
        return

    queries = [
        {'package': {'name': package['name'], 'ecosystem': 'PyPI'}, 'version': package['version']}
        for package in packages
    ]

    url = 'https://api.osv.dev/v1/querybatch'
    headers = {'Content-Type': 'application/json'}

    print(f'{Fore.BLUE}[INFO] Sending a request to OSV API...')

    try:
        response = requests.post(url, headers=headers, json={'queries': queries}, timeout=15)
        response.raise_for_status()
        results = response.json().get('results', [])
    except requests.RequestException as e:
        print(f'{Fore.RED}[ERROR] Network or API error: {e}')
        return

    table = Table(title='Python vulnerability check results')
    table.add_column('Library', style='cyan')
    table.add_column('Vulnerability ID (CVE)', style='magenta')
    table.add_column('Description', style='white')

    for index, result in enumerate(results):
        name = packages[index]['name']
        version = packages[index]['version']

        if 'vulns' in result:
            vulns = result['vulns']
            for vuln in vulns:

                vuln_id = vuln.get('id', 'N/A')
                aliases = vuln.get('aliases', [])
                cve_ids = [a for a in aliases if a.startswith('CVE-')]

                display_id = (f'{cve_ids[0]} ({vuln_id})' if cve_ids else vuln_id)

                summary = vuln.get('summary') or vuln.get('details', 'No description available')
                short_summary = summary[:57] + '...' if len(summary) > 60 else summary

                table.add_row(f'{name} ({version})', display_id, summary)

                issue = save_issue("VULNERABILITY", "HIGH", line=f"{name}=={version}",message=f"Found vulnerability {display_id}: {short_summary}")
                issues.append(issue)

    print(f'{Fore.BLUE}[INFO] Scan finished.')
    
    if issues:
        console.print(table)
        print(f'{Fore.YELLOW}[WARNING] Vulnerabilies found: {len(issues)}.')
    else:
        status = "SUCCEED"
        print(f'{Fore.GREEN}[OK] No vulnerabilities found.')

    scan_meta = make_scan_meta(file_path, status, len(issues))
    write_json_report(scan_meta, issues)
    print(f'{Fore.GREEN}[SUCCESS] Report saved to report.json.')