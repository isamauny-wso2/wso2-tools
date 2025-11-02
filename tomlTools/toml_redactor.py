#!/usr/bin/env python3
"""
TOML Redactor Utility
Redacts sensitive data (passwords, keys, tokens) from TOML configuration files.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Set


class TOMLRedactor:
    """Redacts sensitive information from TOML files."""

    # Sensitive field patterns to redact
    SENSITIVE_PATTERNS = {
        'password', 'passwd', 'pwd',
        'key', 'apikey', 'api_key', 'secret',
        'auth_token', 'access_token', 'refresh_token', 'bearer_token',
        'credential', 'credentials',
        'key_password',
        'moesifkey', 'embedding_endpoint_key'
    }

    # More specific token patterns (must match exactly or be at word boundaries)
    TOKEN_PATTERNS = [
        r'\btoken\b',  # standalone 'token'
        r'_token$',    # ending with '_token'
        r'^token_',    # starting with 'token_'
    ]

    # Configuration key patterns that should NOT be redacted (even if they contain sensitive terms)
    CONFIG_EXCLUDE_PATTERNS = [
        # Boolean/toggle settings
        r'^allow_',
        r'^enable_',
        r'^disable_',
        r'^show_',
        r'^display_',
        r'^retain_',

        # Time/duration settings
        r'_time$',
        r'_period$',
        r'_expiry$',
        r'_timeout$',
        r'_ttl$',
        r'_validity_period$',

        # Size/count settings
        r'_size$',
        r'_count$',
        r'_length$',
        r'^max_',
        r'^min_',

        # Other configuration patterns
        r'_threads$',
        r'_pool_size$',
        r'_interval$',
    ]

    # Additional patterns for values that look sensitive
    VALUE_PATTERNS = [
        # JWT tokens
        r'eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*',
        # Base64 encoded credentials (long strings)
        r'^[A-Za-z0-9+/]{40,}={0,2}$',
        # API keys starting with common prefixes
        r'^sk-[A-Za-z0-9_-]{20,}',  # OpenAI style
        r'^[A-Za-z0-9]{32,}$',  # Generic long alphanumeric
    ]

    def __init__(self, redaction_text: str = "***REDACTED***",
                 check_values: bool = True,
                 preserve_commented: bool = True,
                 remove_comments: bool = False):
        """
        Initialize the redactor.

        Args:
            redaction_text: Text to replace sensitive values with
            check_values: Also check value patterns for potential secrets
            preserve_commented: Keep commented lines as-is
            remove_comments: Remove all comments from the output
        """
        self.redaction_text = redaction_text
        self.check_values = check_values
        self.preserve_commented = preserve_commented
        self.remove_comments = remove_comments
        self.redacted_count = 0
        self.redacted_lines: Set[int] = set()

    def is_sensitive_key(self, key: str) -> bool:
        """Check if a key name indicates sensitive data."""
        # Remove quotes from dotted keys like properties."moesifKey"
        key_clean = re.sub(r'["\']', '', key).lower()

        # First check if this key matches configuration exclude patterns
        for pattern in self.CONFIG_EXCLUDE_PATTERNS:
            if re.search(pattern, key_clean):
                return False

        # Check simple patterns
        if any(pattern in key_clean for pattern in self.SENSITIVE_PATTERNS):
            return True

        # Check specific token patterns
        for pattern in self.TOKEN_PATTERNS:
            if re.search(pattern, key_clean):
                return True

        return False

    def is_sensitive_value(self, value: str) -> bool:
        """Check if a value appears to contain sensitive data."""
        if not self.check_values:
            return False

        # Remove quotes if present
        clean_value = value.strip().strip('"\'')

        # Skip if it's a variable reference
        if clean_value.startswith('$') or clean_value.startswith('${'):
            return False

        # Skip boolean values
        if clean_value.lower() in ('true', 'false'):
            return False

        # Skip numeric values
        try:
            float(clean_value)
            return False
        except ValueError:
            pass

        # Check against value patterns
        for pattern in self.VALUE_PATTERNS:
            if re.search(pattern, clean_value):
                return True

        return False

    def redact_line(self, line: str, line_num: int) -> str:
        """
        Redact sensitive data from a single line.

        Args:
            line: The line to process
            line_num: Line number for tracking

        Returns:
            Redacted line
        """
        # Handle empty lines and comments
        stripped = line.lstrip()
        if not stripped:
            return line

        # Remove comments if configured
        if stripped.startswith('#'):
            if self.remove_comments:
                return ''  # Remove the entire comment line
            elif self.preserve_commented:
                return line  # Keep comment as-is
            # If preserve_commented is False but remove_comments is also False,
            # we still keep the comment (preserve_commented only affects redaction of commented lines)
            return line

        # Match TOML key-value pairs
        # Pattern: key = "value" or key = 'value' or key = value
        # Also handles dotted keys with quotes like: properties."moesifKey"
        match = re.match(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_.-]*(?:\."[^"]*")*)\s*=\s*(.+)$', line)

        if not match:
            return line

        indent, key, value = match.groups()

        # Check if key or value is sensitive
        if self.is_sensitive_key(key) or self.is_sensitive_value(value):
            # Preserve the quote style if present
            value_stripped = value.strip()
            if value_stripped.startswith('"') and value_stripped.endswith('"'):
                redacted_value = f'"{self.redaction_text}"'
            elif value_stripped.startswith("'") and value_stripped.endswith("'"):
                redacted_value = f"'{self.redaction_text}'"
            else:
                redacted_value = f'"{self.redaction_text}"'

            self.redacted_count += 1
            self.redacted_lines.add(line_num)
            return f'{indent}{key} = {redacted_value}\n'

        return line

    def redact_file(self, input_path: Path, output_path: Path = None) -> bool:
        """
        Redact sensitive data from a TOML file.

        Args:
            input_path: Path to input TOML file
            output_path: Path to output file (if None, prints to stdout)

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            redacted_lines = []
            for line_num, line in enumerate(lines, start=1):
                redacted_line = self.redact_line(line, line_num)
                redacted_lines.append(redacted_line)

            output_content = ''.join(redacted_lines)

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                print(f"Redacted {self.redacted_count} sensitive fields")
                print(f"Output written to: {output_path}")
            else:
                print(output_content)
                print(f"\n# Redacted {self.redacted_count} sensitive fields", file=sys.stderr)

            return True

        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            return False

    def get_report(self) -> str:
        """Generate a redaction report."""
        if not self.redacted_lines:
            return "No sensitive data found."

        lines_str = ', '.join(map(str, sorted(self.redacted_lines)))
        return (f"Redacted {self.redacted_count} sensitive fields\n"
                f"Lines modified: {lines_str}")


def main():
    parser = argparse.ArgumentParser(
        description='Redact sensitive data from TOML configuration files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Redact and print to stdout
  %(prog)s deployment.toml

  # Redact and save to new file
  %(prog)s deployment.toml -o deployment.redacted.toml

  # Use custom redaction text
  %(prog)s deployment.toml -o output.toml -r "[HIDDEN]"

  # Only redact based on key names, not value patterns
  %(prog)s deployment.toml --no-check-values
        """
    )

    parser.add_argument('input', type=str, help='Input TOML file path')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file path (default: stdout)')
    parser.add_argument('-r', '--redaction-text', type=str,
                       default='***REDACTED***',
                       help='Text to replace sensitive values with (default: ***REDACTED***)')
    parser.add_argument('--no-check-values', action='store_true',
                       help='Only redact based on key names, not value patterns')
    parser.add_argument('--include-comments', action='store_true',
                       help='Also redact commented lines')
    parser.add_argument('--remove-comments', action='store_true',
                       help='Remove all comment lines from output')
    parser.add_argument('--report', action='store_true',
                       help='Print detailed redaction report')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else None

    redactor = TOMLRedactor(
        redaction_text=args.redaction_text,
        check_values=not args.no_check_values,
        preserve_commented=not args.include_comments,
        remove_comments=args.remove_comments
    )

    success = redactor.redact_file(input_path, output_path)

    if args.report:
        print("\n" + redactor.get_report(), file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
