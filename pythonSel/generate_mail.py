import os
import base64
import requests
import pandas as pd
from azure.identity import ClientSecretCredential

from configfile import (
    SES_SENDER,
    SES_RECEIVERS,
    TENANT_ID,
    CLIENT_SECRET,
    CLIENT_ID
)


def send_mail(subject: str,
              df: pd.DataFrame,
              df2: pd.DataFrame,
              df3: pd.DataFrame,
              csv_path: str = None):

    # ================= VALIDATION =================
    if df is None or df.empty:
        raise ValueError("Detailed DataFrame (df) is empty or None")
    if df2 is None or df2.empty:
        raise ValueError("Summary DataFrame (df2) is empty or None")
    if df3 is None or df3.empty:
        raise ValueError("Summary DataFrame (df3) is empty or None")

    # ================= STATUS COLOR =================
    def status_color(status):
        status = str(status).lower()
        if status == "pass":
            return "#28a745"
        elif status == "fail":
            return "#dc3545"
        else:
            return "#ffc107"

    # ================= TABLE 1 : DETAILED =================
    table_rows = ""
    for _, row in df.iterrows():
        table_rows += f"""
        <tr>
            <td>{row.get('S No', '')}</td>
            <td>{row.get('Module', '')}</td>
            <td>{row.get('Test Description', '')}</td>
            <td>{row.get('Expected', '')}</td>
            <td>{row.get('Actual', '')}</td>
            <td style="background-color:{status_color(row.get('Status'))};
                       color:white;font-weight:bold;">
                {row.get('Status', '')}
            </td>
        </tr>
        """

    html_table_1 = f"""
    <table border="1" cellspacing="0" cellpadding="8"
           style="border-collapse:collapse;width:95%;
                  font-family:Calibri;text-align:center;">
        <tr style="background-color:#002060;color:white;font-weight:bold;">
            <th>S No</th>
            <th>Module</th>
            <th>Test Description</th>
            <th>Expected</th>
            <th>Actual</th>
            <th>Status</th>
        </tr>
        {table_rows}
    </table>
    """

    # ================= TABLE 2 : MODULE SUMMARY =================
    table_rows_2 = ""
    for _, row in df2.iterrows():
        table_rows_2 += f"""
        <tr>
            <td>{row.get('S No', '')}</td>
            <td>{row.get('Module', '')}</td>
            <td>{row.get('Total_Test_Case', '')}</td>
            <td>{row.get('Executed_Test_Case', '')}</td>
            <td>{row.get('Pending_Test_Case', '')}</td>
            <td>{row.get('PASS', '')}</td>
            <td>{row.get('FAIL', '')}</td>
        </tr>
        """

    html_table_2 = f"""
    <table border="1" cellspacing="0" cellpadding="8"
           style="border-collapse:collapse;width:95%;
                  font-family:Calibri;text-align:center;margin-top:20px;">
        <tr style="background-color:#002060;color:white;font-weight:bold;">
            <th>S No</th>
            <th>Module</th>
            <th>Total Test-case</th>
            <th>Executed Test-case</th>
            <th>Pending Test-case</th>
            <th>PASS</th>
            <th>FAIL</th>
        </tr>
        {table_rows_2}
    </table>
    """

    # ================= TABLE 3 : OVERALL SUMMARY =================
    table_rows_3 = ""
    for _, row in df3.iterrows():
        table_rows_3 += f"""
        <tr>
            <td>{row.get('S No', '')}</td>
            <td>{row.get('Total Test Case', '')}</td>
            <td>{row.get('Executed Test Case', '')}</td>
            <td>{row.get('Pending Test Case', '')}</td>
            <td>{row.get('PASS', '')}</td>
            <td>{row.get('FAIL', '')}</td>
        </tr>
        """

    html_table_3 = f"""
    <table border="1" cellspacing="0" cellpadding="8"
           style="border-collapse:collapse;width:95%;
                  font-family:Calibri;text-align:center;margin-top:20px;">
        <tr style="background-color:#002060;color:white;font-weight:bold;">
            <th>S No</th>
            <th>Total Test-case</th>
            <th>Executed Test-case</th>
            <th>Pending Test-case</th>
            <th>PASS</th>
            <th>FAIL</th>
        </tr>
        {table_rows_3}
    </table>
    """

    # ================= EMAIL BODY =================
    body = f"""
    <html>
    <body style="font-family:Calibri;">
        <h3 style="color:#002060;text-align:center;">{subject}</h3>
        <p>Hello Team,</p>
        <p>Please find below the pytest execution summary:</p>
        <h4>&#128204; Detailed Test Results</h4>
        {html_table_1}
        <h4>&#128202; Module-wise Summary</h4>
        {html_table_2}
        <br>
        <h4>&#128202; Total Test Summary</h4>
        {html_table_3}
        <br>
        <p>Detailed CSV report is attached for reference.</p>
        <br>
        <p><b>Regards,</b><br>Codifi QA Team</p>
    </body>
    </html>
    """
    return body


def send_mail_graph(subject, body, csv_path=None):
    try:
        credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        token = credential.get_token("https://graph.microsoft.com/.default").token

        # SES_RECEIVERS list or string - both handle pannanum
        if isinstance(SES_RECEIVERS, list):
            receivers = [e.strip() for e in SES_RECEIVERS]
        else:
            receivers = [e.strip() for e in SES_RECEIVERS.split(",")]

        recipient_list = [{"emailAddress": {"address": email}} for email in receivers]

        attachments = []
        if csv_path and os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                encoded_file = base64.b64encode(f.read()).decode()
            attachments.append({
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(csv_path),
                "contentType": "text/csv",
                "contentBytes": encoded_file
            })

        payload = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": body},
                "toRecipients": recipient_list,
                "attachments": attachments
            },
            "saveToSentItems": True
        }

        url = f"https://graph.microsoft.com/v1.0/users/{SES_SENDER}/sendMail"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 202:
            print("✅ Mail sent successfully via Microsoft Graph")
            return True
        else:
            print(f"❌ Mail failed: {response.status_code} {response.text}")
            return False

    except Exception as e:
        print(f"❌ Mail failed: {str(e)}")
        return False


# ================= CSV -> DataFrame HELPER =================
def load_dataframes_from_csv(csv_path: str):
    """
    CSV structure confirmed (15 columns, no header row):
    col8  = test_name
    col9  = Module
    col14 = Status (pass/fail)

    Rows where col9 (Module) is NaN = login/OTP rows -> skip
    """
    raw_df = pd.read_csv(csv_path, header=None, skiprows=1)
    print(f"📋 CSV shape: {raw_df.shape}")

    # col8 = test_name, col9 = Module, col14 = Status
    raw_df.columns = [f"col{i}" for i in range(raw_df.shape[1])]

    raw_df.rename(columns={
        'col8': 'test_name',
        'col12':'Expected',
        'col13':'Actual',
        'col9': 'Module',
        'col14': 'Status'
    }, inplace=True)

    raw_df = raw_df[
        raw_df['Module'].notna() &
        (raw_df['Module'].astype(str).str.strip() != '') &
        (raw_df['Module'].astype(str).str.strip().str.lower() != 'nan') &
        raw_df['Status'].notna() &
        (raw_df['Status'].astype(str).str.strip() != '') &
        (raw_df['Status'].astype(str).str.strip().str.lower() != 'nan')
    ].reset_index(drop=True)

    print(f"✅ Valid rows after filter: {len(raw_df)}")

    # ===== df : DETAILED =====
    df = pd.DataFrame({
        'S No': range(1, len(raw_df) + 1),
        'Module': raw_df['Module'].astype(str).str.strip().values,
        'Test Description': raw_df['test_name'].astype(str).str.strip().values,
        'Expected': raw_df['Expected'].astype(str).str.strip().values,
        'Actual':raw_df['Actual'].astype(str).str.strip().values,
        'Status': raw_df['Status'].astype(str).str.strip().str.capitalize().values
    })

    # ===== df2 : MODULE SUMMARY =====
    df2_list = []
    for i, (module, grp) in enumerate(df.groupby('Module', sort=False), start=1):
        df2_list.append({
            'S No': i,
            'Module': module,
            'Total_Test_Case': len(grp),
            'Executed_Test_Case': len(grp[grp['Status'].str.lower() != 'pending']),
            'Pending_Test_Case': len(grp[grp['Status'].str.lower() == 'pending']),
            'PASS': len(grp[grp['Status'].str.lower() == 'pass']),
            'FAIL': len(grp[grp['Status'].str.lower() == 'fail']),
        })
    df2 = pd.DataFrame(df2_list)

    # ===== df3 : OVERALL SUMMARY =====
    df3 = pd.DataFrame([{
        'S No': 1,
        'Total Test Case': len(df),
        'Executed Test Case': len(df[df['Status'].str.lower() != 'pending']),
        'Pending Test Case': len(df[df['Status'].str.lower() == 'pending']),
        'PASS': len(df[df['Status'].str.lower() == 'pass']),
        'FAIL': len(df[df['Status'].str.lower() == 'fail']),
    }])

    return df, df2, df3


# ================= MAIN =================
if __name__ == "__main__":
    print("🚀 Script started...")

    csv_path = "login_test_results.csv"

    df, df2, df3 = load_dataframes_from_csv(csv_path)

    print("\n📌 Detailed df:")
    print(df)
    print("\n📊 Module Summary df2:")
    print(df2)
    print("\n📊 Overall Summary df3:")
    print(df3)

    body = send_mail(
        subject="Automation Test Report",
        df=df, df2=df2, df3=df3,
        csv_path=csv_path
    )

    send_mail_graph(
        subject="Rmoney Automation Test Report",
        body=body,
        csv_path=csv_path
    )

    print("\n✅ Done")
