# ObscuraCheck

A powerful Python tool for analyzing HTTP security headers with detailed reporting and visualization capabilities.

## Features

- Real-time HTTP header analysis from URLs or raw header input
- Concurrent processing of multiple URLs
- Comprehensive security header validation
- Risk assessment based on industry best practices
- Support for authentication (OAuth, API Key, Basic Auth)
- Multiple report formats (JSON, Text, PDF)
- Interactive command-line interface with colorful output
- Progress tracking and loading animations
- Visual diagrams of header relationships
- Detailed recommendations for security improvements

## Installation

```bash
# Clone the repository
git clone https://github.com/vedantkulkarni1234/ObscuraCheck.git

# Navigate to the project directory
cd obscuracheck

# Install required dependencies
pip install -r requirements.txt
```

Required dependencies:
- requests
- argparse
- pyfiglet
- colorama
- tqdm
- matplotlib
- networkx
- Flask
- reportlab

## Usage

### Basic Usage

```bash
python ObscuraCheck.py
```

The tool will present an interactive interface where you can choose between:
1. URL analysis
2. Raw header analysis

### Input Methods

#### URL Analysis
Enter one or multiple URLs (comma-separated) to analyze their security headers:
```bash
Enter URLs (comma-separated): https://example.com, https://test.com
```

#### Raw Headers Analysis
Input raw headers directly in the format "Header: Value" (one per line):
```
Content-Security-Policy: default-src 'self';
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Authentication Support

The tool supports multiple authentication methods:
- OAuth
- API Key
- Basic Authentication

When analyzing URLs that require authentication, you'll be prompted to:
1. Choose the authentication type
2. Provide necessary credentials

## Security Headers Analyzed

The tool checks for the presence and configuration of critical security headers:

- X-Frame-Options
- Content-Security-Policy
- X-XSS-Protection
- X-Content-Type-Options
- Strict-Transport-Security

### Risk Assessment

Headers are evaluated based on:
- Presence/absence of required headers
- Compliance with security best practices
- Use of deprecated headers
- Value configuration

Risk levels:
- Low: Properly configured headers
- Medium: Present but potentially misconfigured headers
- High: Missing or improperly configured critical headers

## Output Formats

### Console Output
- Colorized terminal output with detailed analysis
- Progress indicators and loading animations
- Clear categorization of findings

### Report Formats
1. JSON
   - Structured data format
   - Ideal for programmatic analysis
   
2. Text
   - Human-readable format
   - Includes all analysis details
   
3. PDF
   - Professional report format
   - Includes tables and visual elements
   - Suitable for documentation and sharing

## Recommendations

The tool provides:
- Specific recommendations for missing headers
- Best practice values for existing headers
- Suggested fixes for deprecated headers
- Security score assessment

## Development

### Project Structure
```
obscuracheck/
├── ObscuraCheck.py
├── requirements.txt
├── README.md
└── Output/
    ├── reports/
    └── visualizations/
```

### Constants and Configurations

Security headers are configured in the constants section:
```python
SECURITY_HEADERS = [
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Strict-Transport-Security"
]
```

Risk profiles can be customized:
```python
DEFAULT_RISK_PROFILE = {
    "low": 20,
    "medium": 10,
    "high": 0
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python 3.x
- Uses various open-source libraries for enhanced functionality
- Inspired by security best practices and OWASP guidelines

## Support

For support, please:
1. Check existing issues
2. Create a new issue with detailed description
3. Include sample headers or URLs (without sensitive information)

## Disclaimer

This tool is for security analysis purposes only. Always verify findings and consult with security professionals for critical implementations.
