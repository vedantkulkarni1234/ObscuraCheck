import requests
import argparse
import json
import pyfiglet
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import time
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
import networkx as nx
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify, render_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Initialize colorama
init(autoreset=True)

# Constants for Security Headers
SECURITY_HEADERS = [
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Strict-Transport-Security"
]

# List of deprecated or obsolete headers and their modern alternatives
DEPRECATED_HEADERS = {
    "X-XSS-Protection": "Content-Security-Policy",
    "X-Content-Type-Options": "Content-Type"
}

# Best practices for header values
HEADER_RECOMMENDATIONS = {
    "X-Frame-Options": ["DENY", "SAMEORIGIN"],
    "Content-Security-Policy": ["default-src 'self';"],
    "Strict-Transport-Security": ["max-age=31536000; includeSubDomains"],
    "X-XSS-Protection": ["1; mode=block"],
    "X-Content-Type-Options": ["nosniff"]
}

# Default risk assessment profile
DEFAULT_RISK_PROFILE = {
    "low": 20,
    "medium": 10,
    "high": 0
}

# New features:
def print_loading_animation():
    """Print a fun loading animation"""
    animation = "|/-\\"
    for i in range(20):
        time.sleep(0.1)
        print(Fore.CYAN + "\r" + animation[i % len(animation)], end="")
    print(Style.RESET_ALL)
def show_progress_bar(total_steps):
    """Display a progress bar for analysis"""
    for i in tqdm(range(total_steps), desc="Analyzing headers", ncols=100, ascii=True):
        time.sleep(0.1)  # Simulate work being done
def random_motivational_quote():
    """Print a random motivational quote"""
    quotes = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ]
    print(Fore.MAGENTA + random.choice(quotes))
def display_report(report):
    """Display the analysis report with colorful header results"""
    print(Fore.CYAN + "\n[+] Header Analysis Report:")

    print(Fore.CYAN + "\n[+] Present Headers:")
    for header in report["present_headers"]:
        print(Fore.GREEN + f"  {header}")

    print(Fore.CYAN + "\n[+] Missing Headers:")
    for header in report["missing_headers"]:
        print(Fore.RED + f"  {header}")

    print(Fore.CYAN + "\n[+] Header Values:")
    for header, value in report["header_values"].items():
        print(Fore.YELLOW + f"  {header}: {value}")

    print(Fore.CYAN + "\n[+] Recommendations for Improvement:")
    for header, recommendation in report["recommendations"].items():
        print(Fore.YELLOW + f"  {header}: Recommended values: {', '.join(recommendation)}")

    print(Fore.CYAN + "\n[+] Risk Assessment:")
    for header, risk in report["risk_assessment"].items():
        print(Fore.RED + f"  {header}: {risk}")

    print(Fore.CYAN + "\n[+] Deprecated Headers:")
    for header, alternative in report["deprecated_headers"]:
        print(Fore.MAGENTA + f"  {header}: Deprecated, use {alternative}")

    print(Fore.CYAN + "\n[+] Suggested Fixes:")
    for header, fix in report["suggested_fixes"].items():
        print(Fore.GREEN + f"  {header}: {fix}")

def real_time_header_fetch_simulation(url, auth=None):
    """Simulate real-time fetching of headers from a URL with optional authentication"""
    print(Fore.GREEN + "Starting real-time header fetch simulation...")
    for i in range(5):
        print(Fore.CYAN + f"Fetching headers... {i*20}% complete")
        time.sleep(1)  # Simulate time delay for fetching headers
    headers = fetch_headers_from_url(url, auth)
    print(Fore.GREEN + "Headers fetched successfully!")
    return headers
def detailed_risk_analysis(headers, risk_profile=DEFAULT_RISK_PROFILE):
    """Perform a detailed risk analysis based on header content and user-defined risk profile"""
    risk_assessment = {}
    
    for header, value in headers.items():
        if header in SECURITY_HEADERS:
            if header == "Content-Security-Policy":
                if re.match(r"default-src 'self';", value):
                    risk_assessment[header] = "Low risk"
                else:
                    risk_assessment[header] = f"High risk - Recommended value: default-src 'self'; (Score: {risk_profile['high']})"
            elif header == "Strict-Transport-Security":
                if "max-age=" in value and "includeSubDomains" in value:
                    risk_assessment[header] = "Low risk"
                else:
                    risk_assessment[header] = f"High risk - Recommended value: max-age=31536000; includeSubDomains (Score: {risk_profile['high']})"
            elif value in HEADER_RECOMMENDATIONS.get(header, []):
                risk_assessment[header] = "Low risk"
            else:
                risk_assessment[header] = f"High risk - Recommended value: " + ", ".join(HEADER_RECOMMENDATIONS[header]) + f" (Score: {risk_profile['high']})"
        else:
            risk_assessment[header] = f"Unknown risk - Header not in security recommendations (Score: {risk_profile['medium']})"
    
    return risk_assessment
def display_report(report):
    """Display the analysis report with colorful header results and emoji indicators"""
    print(Fore.CYAN + "\n[+] Header Analysis Report:")

    print(Fore.CYAN + "\n[+] Present Headers:")
    for header in report["present_headers"]:
        print(Fore.GREEN + f"  {header} ✅")

    print(Fore.CYAN + "\n[+] Missing Headers:")
    for header in report["missing_headers"]:
        print(Fore.RED + f"  {header} ❌")

    print(Fore.CYAN + "\n[+] Header Values:")
    for header, value in report["header_values"].items():
        print(Fore.YELLOW + f"  {header}: {value}")

    print(Fore.CYAN + "\n[+] Recommendations for Improvement:")
    for header, recommendation in report["recommendations"].items():
        print(Fore.YELLOW + f"  {header}: Recommended values: {', '.join(recommendation)}")

    print(Fore.CYAN + "\n[+] Risk Assessment:")
    for header, risk in report["risk_assessment"].items():
        risk_emoji = "⚠️" if "High risk" in risk else "✅"
        print(Fore.RED + f"  {header}: {risk} {risk_emoji}")

    print(Fore.CYAN + "\n[+] Deprecated Headers:")
    for header, alternative in report["deprecated_headers"]:
        print(Fore.MAGENTA + f"  {header}: Deprecated, use {alternative} ⚠️")

    print(Fore.CYAN + "\n[+] Suggested Fixes:")
    for header, fix in report["suggested_fixes"].items():
        print(Fore.GREEN + f"  {header}: {fix} 📋")

# 8. Special characters for separating sections
def print_section_separator():
    """Print special characters to separate sections in the output"""
    print(Fore.MAGENTA + "\n" + "="*40 + "\n" + Style.RESET_ALL)
def get_headers_input():
    """Interactive prompt to choose between URL or raw header input"""
    while True:
        choice = input("Choose input method (1 for URL, 2 for raw headers): ")
        if choice == '1':
            urls = input("Enter the URLs (comma-separated): ").split(',')
            auth_choice = input("Do you need authentication? (yes/no): ").strip().lower()
            auth = None
            if auth_choice == 'yes':
                auth_type = input("Choose authentication type (1 for OAuth, 2 for API key, 3 for Basic Auth): ").strip()
                if auth_type == '1':
                    token = input("Enter OAuth token: ").strip()
                    auth = {"Authorization": f"Bearer {token}"}
                elif auth_type == '2':
                    api_key = input("Enter API key: ").strip()
                    auth = {"Authorization": f"ApiKey {api_key}"}
                elif auth_type == '3':
                    username = input("Enter username: ").strip()
                    password = input("Enter password: ").strip()
                    auth = HTTPBasicAuth(username, password)
            headers_list = fetch_headers_from_urls(urls, auth)
            return headers_list
        elif choice == '2':
            raw_headers = input("Enter the raw headers (format: 'Header: Value' per line): ")
            headers = parse_raw_headers(raw_headers)
            return [headers]
        else:
            print("Invalid choice. Please enter 1 or 2.")
# 10. Save analysis as JSON, text, or PDF
import json

def save_analysis(report, filename_base, file_format):
    """Save the analysis report as JSON, text, or PDF file based on user choice"""
    output_dir = os.path.join(os.path.dirname(__file__), "Output")
    os.makedirs(output_dir, exist_ok=True)
    
    if file_format == "json":
        json_filename = os.path.join(output_dir, f"{filename_base}.json")
        with open(json_filename, 'w') as json_file:
            json.dump(report, json_file, indent=4)
        print(Fore.GREEN + f"Analysis report saved as JSON: {json_filename}")
    elif file_format == "text":
        text_filename = os.path.join(output_dir, f"{filename_base}.txt")
        with open(text_filename, 'w') as text_file:
            text_file.write("Header Analysis Report:\n\n")

            text_file.write("Present Headers:\n")
            for header in report["present_headers"]:
                text_file.write(f"  {header} ✅\n")

            text_file.write("\nMissing Headers:\n")
            for header in report["missing_headers"]:
                text_file.write(f"  {header} ❌\n")

            text_file.write("\nHeader Values:\n")
            for header, value in report["header_values"].items():
                text_file.write(f"  {header}: {value}\n")

            text_file.write("\nRecommendations for Improvement:\n")
            for header, recommendation in report["recommendations"].items():
                text_file.write(f"  {header}: Recommended values: {', '.join(recommendation)}\n")

            text_file.write("\nRisk Assessment:\n")
            for header, risk in report["risk_assessment"].items():
                risk_emoji = "⚠️" if "High risk" in risk else "✅"
                text_file.write(f"  {header}: {risk} {risk_emoji}\n")

            text_file.write("\nDeprecated Headers:\n")
            for header, alternative in report["deprecated_headers"]:
                text_file.write(f"  {header}: Deprecated, use {alternative} ⚠️\n")

            text_file.write("\nSuggested Fixes:\n")
            for header, fix in report["suggested_fixes"].items():
                text_file.write(f"  {header}: {fix} 📋\n")

        print(Fore.GREEN + f"Analysis report saved as text: {text_filename}")
    elif file_format == "pdf":
        pdf_filename = os.path.join(output_dir, f"{filename_base}.pdf")
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Header Analysis Report", styles['Title'])
        elements.append(title)

        elements.append(Paragraph("Present Headers:", styles['Heading2']))
        present_headers_data = [[header, "✅"] for header in report["present_headers"]]
        present_headers_table = Table(present_headers_data)
        present_headers_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.green),
                                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(present_headers_table)

        elements.append(Paragraph("Missing Headers:", styles['Heading2']))
        missing_headers_data = [[header, "❌"] for header in report["missing_headers"]]
        missing_headers_table = Table(missing_headers_data)
        missing_headers_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(missing_headers_table)

        elements.append(Paragraph("Header Values:", styles['Heading2']))
        header_values_data = [[header, value] for header, value in report["header_values"].items()]
        header_values_table = Table(header_values_data)
        header_values_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
                                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                 ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(header_values_table)

        elements.append(Paragraph("Recommendations for Improvement:", styles['Heading2']))
        recommendations_data = [[header, ', '.join(recommendation)] for header, recommendation in report["recommendations"].items()]
        recommendations_table = Table(recommendations_data)
        recommendations_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
                                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(recommendations_table)

        elements.append(Paragraph("Risk Assessment:", styles['Heading2']))
        risk_assessment_data = [[header, risk] for header, risk in report["risk_assessment"].items()]
        risk_assessment_table = Table(risk_assessment_data)
        risk_assessment_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(risk_assessment_table)

        elements.append(Paragraph("Deprecated Headers:", styles['Heading2']))
        deprecated_headers_data = [[header, alternative] for header, alternative in report["deprecated_headers"]]
        deprecated_headers_table = Table(deprecated_headers_data)
        deprecated_headers_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.magenta),
                                                      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                      ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                                      ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(deprecated_headers_table)

        elements.append(Paragraph("Suggested Fixes:", styles['Heading2']))
        suggested_fixes_data = [[header, fix] for header, fix in report["suggested_fixes"].items()]
def print_banner():
    """Print ASCII banner for the tool"""
    ascii_banner = pyfiglet.figlet_format("Header Analyzer", font="slant")
    print(Fore.CYAN + ascii_banner)
    print(Fore.YELLOW + "Analyze and secure your HTTP headers effortlessly!")
    print(Style.RESET_ALL)

def fetch_headers_from_url(url, auth=None):
    """Fetch HTTP headers from a given URL with optional authentication"""
    print(Fore.GREEN + f"Fetching headers from the URL: {url}")
    time.sleep(1)  # Simulate loading
    try:
        if auth:
            response = requests.head(url, headers=auth, timeout=10)
        else:
            response = requests.head(url, timeout=10)
        return response.headers
    except requests.exceptions.RequestException as e:
        raise ValueError(f"{Fore.RED}Error fetching headers from URL: {e}")

def fetch_headers_from_urls(urls, auth=None):
    """Fetch HTTP headers from multiple URLs concurrently with optional authentication"""
    headers_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_headers_from_url, url, auth): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                headers = future.result()
                headers_list.append(headers)
            except Exception as e:
                print(f"{Fore.RED}Error fetching headers from {url}: {e}")
    return headers_list

def parse_raw_headers(raw_headers):
    """Parse raw header text into a dictionary"""
    headers = {}
    for line in raw_headers.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.strip()] = value.strip()
    return headers

def analyze_headers(headers, risk_profile=DEFAULT_RISK_PROFILE):
    """Analyze HTTP headers for security-related issues based on user-defined risk profile"""
    analysis_report = {
        "present_headers": [],
        "missing_headers": [],
        "header_values": {},
        "recommendations": {},
        "risk_assessment": {},
        "deprecated_headers": [],
        "security_score": 0,
        "suggested_fixes": {}
    }

    # Check for presence of security headers
    for header in SECURITY_HEADERS:
        if header in headers:
            analysis_report["present_headers"].append(header)
            analysis_report["header_values"][header] = headers[header]
            # Check header value against recommendations
            if header == "Content-Security-Policy":
                if re.match(r"default-src 'self';", headers[header]):
                    analysis_report["risk_assessment"][header] = "Low"
                    analysis_report["security_score"] += risk_profile["low"]
                else:
                    analysis_report["recommendations"][header] = HEADER_RECOMMENDATIONS[header]
                    analysis_report["risk_assessment"][header] = "High"
                    analysis_report["suggested_fixes"][header] = "Content-Security-Policy: default-src 'self';"
            elif header == "Strict-Transport-Security":
                if "max-age=" in headers[header] and "includeSubDomains" in headers[header]:
                    analysis_report["risk_assessment"][header] = "Low"
                    analysis_report["security_score"] += risk_profile["low"]
                else:
                    analysis_report["recommendations"][header] = HEADER_RECOMMENDATIONS[header]
                    analysis_report["risk_assessment"][header] = "High"
                    analysis_report["suggested_fixes"][header] = "Strict-Transport-Security: max-age=31536000; includeSubDomains"
            elif headers[header] not in HEADER_RECOMMENDATIONS.get(header, []):
                analysis_report["recommendations"][header] = HEADER_RECOMMENDATIONS[header]
                analysis_report["risk_assessment"][header] = "High"
                analysis_report["suggested_fixes"][header] = f"{header}: {', '.join(HEADER_RECOMMENDATIONS[header])}"
            else:
                analysis_report["risk_assessment"][header] = "Low"
                analysis_report["security_score"] += risk_profile["low"]
        else:
            analysis_report["missing_headers"].append(header)
            analysis_report["risk_assessment"][header] = "High"  # High risk if header is missing
            analysis_report["suggested_fixes"][header] = f"{header}: {', '.join(HEADER_RECOMMENDATIONS[header])}"

    # Check for deprecated or obsolete headers
    for header in headers:
        if header in DEPRECATED_HEADERS:
            analysis_report["deprecated_headers"].append((header, DEPRECATED_HEADERS[header]))
            analysis_report["suggested_fixes"][header] = f"Remove {header} and use {DEPRECATED_HEADERS[header]} instead"

    return analysis_report

def generate_report(analysis_report):
    """Generate a detailed report of the analysis"""
    report = {}
    
    # Present and Missing Headers
    report["present_headers"] = analysis_report["present_headers"]
    report["missing_headers"] = analysis_report["missing_headers"]
    
    # Header Values and Recommendations
    report["header_values"] = analysis_report["header_values"]
    report["recommendations"] = analysis_report["recommendations"]
    
    # Risk Level Assessment
    report["risk_assessment"] = analysis_report["risk_assessment"]
    
    # Deprecated Headers
    report["deprecated_headers"] = analysis_report["deprecated_headers"]
    
    # Security Score
    report["security_score"] = analysis_report["security_score"]
    
    # Suggested Fixes
    report["suggested_fixes"] = analysis_report["suggested_fixes"]
    
    return json.dumps(report, indent=4)

def validate_input(input_value, is_url=False):
    """Validate input (URL or raw header text)"""
    if is_url:
        # Validate URL format
        if not input_value.startswith("http://") and not input_value.startswith("https://"):
            raise ValueError(f"{Fore.RED}Invalid URL. URL must start with http:// or https://")
        return True
    else:
        # Validate raw header format
        if "\n" not in input_value:
            raise ValueError(f"{Fore.RED}Raw header text must contain newline-separated headers")
        return True

def print_loading_animation():
    """Display a loading animation"""
    print(Fore.CYAN + "Analyzing headers, please wait...")
    for _ in tqdm(range(100), desc="Loading", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        time.sleep(0.05)

def random_motivational_quote():
    """Display a random motivational quote"""
    quotes = [
        "Security is a process, not a product!",
        "The best way to predict the future is to secure it.",
        "Privacy is not a luxury; it’s a right.",
        "Do it right or don’t do it at all!",
        "An ounce of prevention is worth a pound of cure."
    ]
    print(Fore.MAGENTA + random.choice(quotes))

def display_report(report):
    """Display the analysis report in a user-friendly format"""
    print(Fore.GREEN + "\n[+] Analysis Complete!")
    print(Fore.CYAN + "\n[+] Present Security Headers:")
    for header in report["present_headers"]:
        print(Fore.GREEN + f"  {header} ✅")
    
    print(Fore.CYAN + "\n[+] Missing Security Headers:")
    for header in report["missing_headers"]:
        print(Fore.RED + f"  {header} ❌")
    
    print(Fore.CYAN + "\n[+] Header Values:")
    for header, value in report["header_values"].items():
        print(Fore.YELLOW + f"  {header}: {value}")

    print(Fore.CYAN + "\n[+] Recommendations for Improvement:")
    for header, recommendation in report["recommendations"].items():
        print(Fore.YELLOW + f"  {header}: Recommended values: {', '.join(recommendation)}")

    print(Fore.CYAN + "\n[+] Risk Assessment:")
    for header, risk in report["risk_assessment"].items():
        print(Fore.RED + f"  {header}: {risk}")

    print(Fore.CYAN + "\n[+] Deprecated Headers:")
    for header, alternative in report["deprecated_headers"]:
        print(Fore.MAGENTA + f"  {header}: Deprecated, use {alternative}")

    print(Fore.CYAN + f"\n[+] Security Score: {report['security_score']} / 100")

def save_report(analysis_report, filename="report.json"):
    """Save the analysis report to a file"""
    report = generate_report(analysis_report)
    with open(filename, "w") as file:
        file.write(report)
    print(Fore.GREEN + f"\n[+] Analysis report saved to {filename}")

def interactive_prompt():
    """Prompt user to select input method"""
    print(Fore.YELLOW + "\n[+] Choose input method:")
    print(Fore.CYAN + "1. Provide a URL")
    print(Fore.CYAN + "2. Provide raw headers")
    choice = input(Fore.YELLOW + "Enter your choice (1 or 2): ").strip()

    if choice == "1":
        urls = input(Fore.YELLOW + "Enter URLs (comma-separated): ").split(',')
        if all(validate_input(url.strip(), is_url=True) for url in urls):
            headers_list = fetch_headers_from_urls([url.strip() for url in urls])
            return headers_list
    elif choice == "2":
        raw_headers = input(Fore.YELLOW + "Enter raw headers (separate by newlines): ")
        if validate_input(raw_headers, is_url=False):
            headers = parse_raw_headers(raw_headers)
            return [headers]
    else:
        print(Fore.RED + "Invalid choice, try again.")
        return interactive_prompt()

def generate_visual_diagram(report):
    """Generate a visual diagram showing the relationship between headers and their implications"""
    G = nx.DiGraph()

    # Add nodes and edges for present headers
    for header in report["present_headers"]:
        G.add_node(header, color='green')
        G.add_edge("Headers", header)

    # Add nodes and edges for missing headers
    for header in report["missing_headers"]:
        G.add_node(header, color='red')
        G.add_edge("Headers", header)

    # Add nodes and edges for deprecated headers
def main():
    """Main function for command-line interface"""
    print_banner()
    random_motivational_quote()

    # Interactive prompt to choose input
    headers_list = interactive_prompt()

    # Display loading animation
    print_loading_animation()

    # Analyze headers
    for headers in headers_list:
        analysis_report = analyze_headers(headers)
    
        # Display the analysis results
        display_report(analysis_report)
    
        # Ask user if they want to save the report
        save_report_choice = input(Fore.YELLOW + "Do you want to save the report? (yes/no): ").strip().lower()
    # Ask user if they want to save the report
    save_report_choice = input(Fore.YELLOW + "Do you want to save the report? (yes/no): ").strip().lower()
    if save_report_choice == "yes":
        file_format = input(Fore.YELLOW + "Enter the file format (json/text): ").strip().lower()
        if file_format in ["json", "text"]:
            save_analysis(analysis_report, "report", file_format)
        else:
            print(Fore.RED + "Invalid file format. Report not saved.")
    
    print(Fore.GREEN + f"\n[+] All tasks completed successfully!")

if __name__ == "__main__":
    main()
