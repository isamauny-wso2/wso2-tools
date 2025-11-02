# WSO2 Security & Development Tools

A comprehensive collection of security and development tools specifically designed for WSO2 API Manager deployments and configuration management.

## 🛠️ Tools Overview

This repository contains two specialized tool suites:

### 1. 🔒 [TOML Security Tools](tomlTools/)
**Prevent accidental exposure of sensitive data in TOML configuration files**

- **Automatic Detection**: Identifies passwords, API keys, tokens, and other sensitive data
- **Smart Redaction**: Preserves file structure while securing sensitive values
- **Git Integration**: Pre-commit hooks to prevent commits with unredacted secrets
- **CI/CD Ready**: Easy integration into automated pipelines

**Quick Start:**
```bash
cd tomlTools
./toml_redactor.py deployment.toml --report
```

### 2. 🔐 [Certificate Generator](certsGenerator/)
**Generate SSL/TLS certificates for WSO2 deployments**

- **RSA Certificate Generation**: Creates server certificates and keystores
- **Client Truststore Setup**: Automatically configures client trust relationships
- **WSO2 Compatible**: Generates certificates in formats expected by WSO2 products
- **Development Ready**: Pre-configured for local development environments

**Quick Start:**
```bash
cd certsGenerator
./generate-certs.sh
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6+ (for TOML tools)
- Java 8+ with keytool (for certificate generation)
- Git (for pre-commit integration)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/wso2-tools.git
cd wso2-tools
```

2. **Choose your tool:**
   - For TOML security: `cd tomlTools`
   - For certificate generation: `cd certsGenerator`

3. **Follow tool-specific instructions** in each directory's README

## 📁 Repository Structure

```
wso2-tools/
├── README.md                 # This file
├── LICENSE                   # Apache License 2.0
├── tomlTools/               # TOML Security Tools
│   ├── TOML_TOOLS_README.md # Detailed TOML tools documentation
│   └── toml_redactor.py     # Main redaction script
└── certsGenerator/          # Certificate Generation Tools
    ├── generate-certs.sh    # Certificate generation script
    └── certs/              # Generated certificates directory
```

## 🔧 Common Use Cases

### 🛡️ Secure Configuration Management
```bash
# Check TOML files for sensitive data before deployment
cd tomlTools
./toml_redactor.py ../deployment.toml --report

# Generate development certificates
cd certsGenerator
./generate-certs.sh
```

### 🔄 CI/CD Integration
```yaml
# Example GitHub Actions workflow
- name: Security Check TOML Files
  run: |
    python3 tomlTools/toml_redactor.py config/*.toml --report
    if [ $? -ne 0 ]; then
      echo "❌ Sensitive data found in TOML files"
      exit 1
    fi
```

### 🔗 Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/your-org/wso2-tools
    rev: main
    hooks:
      - id: toml-security-check
        files: \.toml$
```

## 🎯 Key Features

### TOML Security Tools
- ✅ **Smart Pattern Recognition**: Detects passwords, keys, tokens, credentials
- ✅ **Value Analysis**: Identifies JWT tokens, Base64 strings, API keys
- ✅ **Configuration Aware**: Excludes false positives (timeouts, booleans, etc.)
- ✅ **Flexible Output**: Console reports, file redaction, custom replacement text
- ✅ **Git Integration**: Pre-commit hooks and CI/CD pipeline support

### Certificate Generator
- ✅ **RSA Certificate Generation**: 2048-bit RSA with SHA256 signing
- ✅ **SAN Support**: Multiple Subject Alternative Names for localhost/IP access
- ✅ **Keystore Creation**: JKS format keystores with configurable passwords
- ✅ **Truststore Setup**: Automatic client truststore configuration
- ✅ **WSO2 Optimized**: Default settings compatible with WSO2 products

## 🔐 Security Best Practices

### For TOML Files
1. **Always run security checks** before committing configuration files
2. **Use redacted versions** for documentation and examples
3. **Set up pre-commit hooks** to prevent accidental exposure
4. **Regular audits** of existing configuration files

### For Certificates
1. **Change default passwords** in production environments
2. **Use proper certificate chains** for production deployments
3. **Regular certificate rotation** (default validity: 365 days)
4. **Secure storage** of private keys and keystores

## 📚 Documentation

- **TOML Tools**: Detailed documentation in [tomlTools/TOML_TOOLS_README.md](tomlTools/TOML_TOOLS_README.md)
- **Certificate Generator**: Usage examples and configuration options in the certsGenerator directory
- **WSO2 Integration**: Best practices for WSO2 API Manager deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure security checks pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines
- **Security First**: All tools must prioritize security and safety
- **WSO2 Compatibility**: Ensure compatibility with WSO2 product requirements
- **Documentation**: Update relevant README files with changes
- **Testing**: Include examples and test cases for new features

## 📞 Support & Resources

- 🐛 **Issues**: [Report bugs and request features](https://github.com/your-org/wso2-tools/issues)
- 💬 **Discussions**: [Community discussions and Q&A](https://github.com/your-org/wso2-tools/discussions)
- 📖 **Wiki**: [Additional documentation and tutorials](https://github.com/your-org/wso2-tools/wiki)
- 🔗 **WSO2 Documentation**: [Official WSO2 API Manager docs](https://apim.docs.wso2.com/)

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

## 🎯 Related Projects

- [WSO2 API Manager](https://wso2.com/api-manager/) - Enterprise API Management
- [Pre-commit Framework](https://pre-commit.com/) - Git hook scripts
- [TOML Specification](https://toml.io/) - Tom's Obvious, Minimal Language

---

**⚠️ Security Note**: These tools are designed to enhance security but should be part of a comprehensive security strategy. Always review outputs and follow your organization's security policies.

**🚀 Quick Links**: [TOML Tools](tomlTools/) | [Certificate Generator](certsGenerator/) | [License](LICENSE) | [Contributing](#-contributing)