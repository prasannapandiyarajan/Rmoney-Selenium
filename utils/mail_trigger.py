import os
import json
import base64
import requests
import pandas as pd

from config_files.config import Props


def send_mail(subject, df: pd.DataFrame, csv_path=None):
    """
    Send pytest execution report email using DataFrame
    """

    if df is None or df.empty:
        raise ValueError("DataFrame is empty or None")

    # ================= STATUS COLOR =================
    def status_color(status):
        status = str(status).lower()
        if status == "pass":
            return "#28a745"   # green
        elif status == "fail":
            return "#dc3545"   # red
        else:
            return "#ffc107"   # pending / others

    # ================= BUILD HTML TABLE =================
    table_rows = ""
    for _, row in df.iterrows():
        table_rows += f"""
        <tr>
            <td>{row.get('S No', '')}</td>
            <td>{row.get('Module', '')}</td>
            <td>{row.get('Test Description', '')}</td>
            <td style="background-color:{status_color(row.get('Status'))};
                       color:white;font-weight:bold;">
                {row.get('Status', '')}
            </td>
        </tr>
        """

    html_table = f"""
    <table border="1" cellspacing="0" cellpadding="8"
           style="border-collapse:collapse;width:90%;
                  font-family:Calibri;text-align:center;">
        <tr style="background-color:#002060;color:white;font-weight:bold;">
            <th>S No</th>
            <th>Module</th>
            <th>Test Description</th>
            <th>Status</th>
        </tr>
        {table_rows}
    </table>
    """

    # ================= EMAIL BODY =================
    body = f"""
    <html>
    <body style="font-family:Calibri;">
        <h3 style="color:#002060;text-align:center;">{subject}</h3>

        <p>Hello Team,</p>

        <p>Please find below the pytest execution summary:</p>

        {html_table}

        <br>
        <p>Detailed CSV report is attached for reference.</p>

        <br>
        <p><b>Regards,</b><br>Codifi QA Team</p>
    </body>
    </html>
    """

    # ================= MAIL CONFIG =================
    url = Props.MAIL_API_URl
    recipient_email = Props.MAIL_CREDENTIAL_RECEIVER
    sender = {"name": "Codifi Support", "email": "vinitha@codifi.in"}
    to = [{"name": e.split("@")[0], "email": e.strip()} for e in recipient_email.split(",")]

    to = [
        {"name": e.split("@")[0], "email": e.strip()}
        for e in recipient_email.split(",")
    ]

    payload = {
        "sender": sender,
        "to": to,
        "subject": subject,
        "htmlContent": body
    }

    # ================= ATTACH CSV (OPTIONAL) =================
    if csv_path and os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        payload["attachment"] = [{
            "content": encoded,
            "name": os.path.basename(csv_path),
            "type": "text/csv"
        }]

    headers = {
        "Accept": "application/json",
        "api-key": Props.MAIL_APP_KEY,
        "Content-Type": "application/json"
    }

    # ================= SEND =================
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print("✅ Mail sent successfully")
        return True
    else:
        print("❌ Mail failed:", response.text)
        return False
