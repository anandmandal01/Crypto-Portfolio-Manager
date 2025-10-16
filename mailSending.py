# mailSending.py
# Email + AI alert system

import os, json, ssl, smtplib
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path


def _load_config():
    """Load SMTP config from env vars or config.json"""
    cfg = {}
    # 1) Env vars
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASS')
    alert_to = os.getenv('ALERT_TO')

    if smtp_host and smtp_port and smtp_user and smtp_pass:
        cfg.update({
            'smtp_host': smtp_host,
            'smtp_port': int(smtp_port),
            'smtp_user': smtp_user,
            'smtp_pass': smtp_pass,
            'alert_to': alert_to,
        })
        return cfg

    # 2) config.json file
    cfg_path = Path('config.json')
    if cfg_path.exists():
        try:
            data = json.loads(cfg_path.read_text(encoding='utf-8'))
            smtp_user = data.get('email') or data.get('smtp_user')
            smtp_pass = data.get('password') or data.get('smtp_pass')
            smtp_host = data.get('smtp_host') or 'smtp.gmail.com'
            smtp_port = int(data.get('smtp_port') or 587)
            alert_to = data.get('alert_to') or os.getenv('ALERT_TO')
            if smtp_user and smtp_pass:
                cfg.update({
                    'smtp_host': smtp_host,
                    'smtp_port': smtp_port,
                    'smtp_user': smtp_user,
                    'smtp_pass': smtp_pass,
                    'alert_to': alert_to,
                })
                return cfg
        except Exception:
            pass

    return {}


def send_alert(subject, body, to_addr=None):
    """Send an email alert. Returns True if sent, False if simulated."""
    cfg = _load_config()
    recipients = []
    if to_addr:
        recipients = [to_addr]
    elif cfg.get('alert_to'):
        recipients = [a.strip() for a in str(cfg['alert_to']).split(',') if a.strip()]

    if cfg:
        smtp_host = cfg['smtp_host']
        smtp_port = cfg['smtp_port']
        smtp_user = cfg['smtp_user']
        smtp_pass = cfg['smtp_pass']

        if not recipients:
            recipients = [smtp_user]

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = ', '.join(recipients)
        msg.set_content(body + "\n\nSent at: " + datetime.utcnow().isoformat() + 'Z')

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls(context=context)
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            print('[mailSending] Email sent to', recipients)
            return True
        except Exception as e:
            print('[mailSending] Email failed, simulation instead:', e)

    # fallback simulation
    print('--- send_alert (SIMULATION) ---')
    print('Subject:', subject)
    print('Body:', body)
    print('Recipients:', recipients or 'none configured')
    return False


def ai_alert(title, message, metadata=None):
    """AI alert placeholder"""
    log_line = f"{datetime.utcnow().isoformat()}Z\t{title}\t{message}\t{metadata or {}}\n"
    try:
        with open('ai_alerts.log', 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception:
        pass
    print('--- AI Alert ---')
    print('Title:', title)
    print('Message:', message)
    if metadata:
        print('Metadata:', metadata)
    return True

