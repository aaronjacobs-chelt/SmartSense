# Security Policy

## Supported Versions

SmartSense takes security seriously. The following versions are currently supported with security updates:

| Version | Supported          |
| ------- | ----------------- |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We value the security of our users and take all security vulnerabilities seriously. If you believe you have found a security vulnerability in SmartSense, please follow these steps:

1. **DO NOT** disclose the vulnerability publicly until it has been addressed by our team.
2. Email your findings to git@happycaps.co.uk with the following information:
   - A clear description of the vulnerability
   - Steps to reproduce the issue
   - Your recommended fix (if any)
   - Any relevant logs, screenshots, or other supporting materials

### What to Expect

- **Initial Response**: We will acknowledge your report within 48 hours.
- **Updates**: We will keep you informed about the progress of addressing the vulnerability.
- **Resolution**: Once fixed, we will notify you and coordinate the public disclosure.
- **Credit**: We will acknowledge your contribution in our security advisory (unless you prefer to remain anonymous).

## Security Best Practices

When deploying SmartSense, we recommend following these security best practices:

1. **Access Control**:
   - Use strong authentication for all system access
   - Implement role-based access control
   - Regularly audit access permissions

2. **Network Security**:
   - Deploy behind a firewall
   - Use encrypted connections (HTTPS/SSL)
   - Regularly update SSL certificates
   - Monitor network traffic for unusual patterns

3. **System Configuration**:
   - Keep all system dependencies up to date
   - Regularly apply security patches
   - Use secure configuration settings
   - Implement logging and monitoring

4. **Data Protection**:
   - Encrypt sensitive data at rest
   - Use secure protocols for data transmission
   - Implement regular data backups
   - Follow data retention policies

## Security Features

SmartSense includes several built-in security features:

- End-to-end encryption for sensor data
- Secure authentication mechanisms
- Audit logging
- Input validation and sanitization
- Protection against common vulnerabilities
- Automated security testing in CI/CD pipeline

## Vulnerability Disclosure Policy

Our policy for handling vulnerability reports:

1. **Receipt**: Acknowledge receipt of vulnerability report
2. **Assessment**: Evaluate severity and impact
3. **Response**: Develop and test fix
4. **Deployment**: Roll out patches to affected versions
5. **Disclosure**: Public announcement after patch deployment

## Security Updates

Security updates are distributed through our regular release channels. We strongly recommend:

- Subscribing to our security advisories
- Following our release announcements
- Regularly checking for updates
- Implementing updates promptly

## Questions

For general security questions or concerns, please email git@happycaps.co.uk.

---

This security policy is regularly reviewed and updated. Last update: 2025-05-01
