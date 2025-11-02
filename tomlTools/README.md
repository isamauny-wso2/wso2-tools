# TOML Security Tools

A collection of security tools for TOML configuration files, designed to prevent accidental exposure of sensitive data in version control systems.

## 🔒 Features

- **Automatic Detection**: Identifies sensitive data in TOML files based on key names and value patterns
- **Smart Redaction**: Preserves file structure while redacting only sensitive values
- **Git Integration**: Pre-commit hooks to prevent commits with unredacted secrets
- **Configurable**: Customizable redaction text and sensitivity patterns
- **Backup Support**: Optional backup creation before redaction

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/wso2-tools/tomlTools.git
cd tomlTools

# Make the script executable
chmod +x toml_redactor.py
```

### Basic Usage

```bash
# Redact a file and print to stdout
./toml_redactor.py deployment.toml

# Redact and save to a new file
./toml_redactor.py deployment.toml -o deployment.redacted.toml

# Redact in-place (overwrites original)
./toml_redactor.py deployment.toml -o deployment.toml

# Use custom redaction text
./toml_redactor.py deployment.toml -r "[HIDDEN]"

# Get detailed report
./toml_redactor.py deployment.toml --report
```

## 🔧 Pre-commit Integration

Automatically check TOML files before commits to prevent sensitive data leaks:

### Setup

1. Add to your project's `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/wso2-tools/tomlTools
    rev: main  # or specific tag/commit
    hooks:
      - id: toml-security-check
        name: TOML Security Check
        entry: python3 toml_redactor.py
        language: system
        files: \.toml$
        args: [--report, --no-output]
        pass_filenames: true
```

2. Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

### What It Does

- ✅ **Scans** all TOML files before each commit
- 🛑 **Blocks** commits containing sensitive data
- 📋 **Reports** exactly which files and lines need attention
- 🔧 **Provides** commands to fix issues

## 📝 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output file path | stdout |
| `-r, --redaction-text` | Text to replace sensitive values | `***REDACTED***` |
| `--no-check-values` | Only check key names, not values | false |
| `--include-comments` | Also redact commented lines | false |
| `--remove-comments` | Remove all comments | false |
| `--report` | Show detailed redaction report | false |

## 🎯 What Gets Detected

### Sensitive Key Patterns
- Passwords: `password`, `passwd`, `pwd`
- Keys: `key`, `apikey`, `api_key`, `secret`
- Tokens: `token`, `auth_token`, `access_token`, `bearer_token`
- Credentials: `credential`, `credentials`

### Value Patterns
- JWT tokens (starts with `eyJ`)
- Base64 encoded strings (40+ characters)
- API keys with common prefixes (`sk-`, long alphanumeric)

### Smart Exclusions
Configuration keys that contain sensitive terms but aren't actually sensitive:
- Boolean settings: `allow_*`, `enable_*`, `show_*`
- Time settings: `*_timeout`, `*_ttl`, `*_period`
- Size settings: `*_size`, `max_*`, `min_*`

## 📖 Examples

### Before Redaction
```toml
[database]
host = "localhost"
password = "super_secret_password"
api_key = "sk-1234567890abcdef"
timeout = 30

[security]
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
enable_auth = true
```

### After Redaction
```toml
[database]
host = "localhost"
password = "***REDACTED***"
api_key = "***REDACTED***"
timeout = 30

[security]
jwt_token = "***REDACTED***"
enable_auth = true
```

## 🔄 Integration Examples

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Check TOML Security
  run: |
    python3 toml_redactor.py config/*.toml --report
    if [ $? -ne 0 ]; then
      echo "❌ Sensitive data found in TOML files"
      exit 1
    fi
```

### Makefile Integration

```makefile
check-toml:
	@python3 tools/toml_redactor.py deployment.toml --report
	@if [ $$? -ne 0 ]; then \
		echo "Run: make redact-toml"; \
		exit 1; \
	fi

redact-toml:
	@python3 tools/toml_redactor.py deployment.toml -o deployment.toml
```

## 🛠️ Development

### Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

### Testing
```bash
# Test with sample files
python3 toml_redactor.py test/sample.toml --report

# Run with different configurations
python3 toml_redactor.py test/sample.toml --no-check-values
python3 toml_redactor.py test/sample.toml --remove-comments
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📜 License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## 🔗 Related Projects

- [WSO2 Migration Tools](https://github.com/wso2-tools/migrationTools) - Tools for migrating WSO2 configurations
- [Pre-commit Hooks](https://pre-commit.com/) - Git hook framework

## 📞 Support

- 🐛 [Report Issues](https://github.com/wso2-tools/tomlTools/issues)
- 💬 [Discussions](https://github.com/wso2-tools/tomlTools/discussions)
- 📖 [Wiki](https://github.com/wso2-tools/tomlTools/wiki)

---

**⚠️ Security Note**: Always review redacted files before committing to ensure all sensitive data has been properly handled.