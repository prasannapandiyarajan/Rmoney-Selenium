import os
import json
import base64
import sys

import requests
import pandas as pd
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# from pageObjects.config import Props
from config_files.config import Props


def send_mail(subject: str,
              df: pd.DataFrame,
              df2: pd.DataFrame,
              df3: pd.DataFrame,
              csv_path: str = None):
    """
    Send pytest execution report email using two DataFrames
    df  -> detailed test result
    df2 -> module-wise summary
    """

    # ================= VALIDATION =================
    if df is None or df.empty:
        raise ValueError("Detailed DataFrame (df) is empty or None")

    if df2 is None or df2.empty:
        raise ValueError("Summary DataFrame (df2) is empty or None")

    if df3 is None or df3.empty:
        raise ValueError("Summary DataFrame (df2) is empty or None")

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
            <th>Status</th>
        </tr>
        {table_rows}
    </table>
    """

    # ================= TABLE 2 : SUMMARY =================
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

    # ================= TABLE 2 : SUMMARY =================
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
        <h3 style="color:#002060;text-align:center;">
            {subject}
        </h3>

        <p>Hello Team,</p>

        <p>Please find below the pytest execution summary:</p>

        <h4>📌 Detailed Test Results</h4>
        {html_table_1}

        <h4>📊 Module-wise Summary</h4>
        {html_table_2}

        <br>
        <h4>📊 Total Test Summary</h4>
        {html_table_3}

        <br>
        <p>Detailed CSV report is attached for reference.</p>

        <br>
        <p><b>Regards,</b><br>Codifi QA Team</p>
    </body>
    </html>
    """

    # ================= MAIL CONFIG =================
    url = Props.MAIL_API_URl
    sender = {"name": "Codifi Support", "email": "jananika@codifi.in"}

    to = [
        {"name": e.split("@")[0], "email": e.strip()}
        for e in Props.MAIL_RECEIVER.split(",")
    ]

    payload = {
        "sender": sender,
        "to": to,
        "subject": subject,
        "htmlContent": body
    }

    # ================= CSV ATTACHMENT =================
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


# -------------------------------
# Read CSV
# -------------------------------
df = pd.read_csv("D:/Python_projects/pythonProject/selenium_project/rmoney/pythonSel/login_test_results.csv")
print(df)
df.columns = df.columns.str.strip().str.lower()


# -------------------------------
# Derive Module
# -------------------------------
def derive_module(row):
    if pd.notna(row.get('username')) or pd.notna(row.get('otp')):
        return "Login"
    if row.get('page') == "Watchlist":
        return "Watchlist"
    if row.get('page') == "Order Window":
        return "Orderbook"
    if row.get('page') == 'Dashboard':
        return "Dashboard"
    if row.get('page') == 'Order Book':
        return "Order Book"
    if row.get('page') == 'Position':
        return "Position"
    if row.get('page') == 'Holdings':
        return "Holdings"
    if row.get('page') == 'Funds':
        return "Funds"
    if row.get('page') == 'Profile':
        return "Profile"
    return None


df['module'] = df.apply(derive_module, axis=1)

# Remove rows without module
df = df.dropna(subset=['module'])
print(df)
# -------------------------------
# Derive Test Description
# -------------------------------
df['test_description'] = (
    df['actual']
    .fillna(df['actual'])
    .fillna("Test case")
)


# -------------------------------
# Derive Status (Pass / Fail / Pending)
# -------------------------------
def derive_status(value):
    if pd.isna(value):
        return "Pending"
    return value.capitalize()


df['final_status'] = df['status'].apply(derive_status)

# -------------------------------
# Build Final Report
# -------------------------------
final_df = df[['module', 'test_description', 'final_status', 'order_type']].copy()

final_df.insert(0, 'S No', range(1, len(final_df) + 1))

final_df.rename(columns={
    'module': 'Module',
    'test_description': 'Test Description',
    'final_status': 'Status'
}, inplace=True)


# -------------------------------
# Export CSV
# -------------------------------


def derive_module(row):
    if pd.notna(row.get('username')) or pd.notna(row.get('otp')):
        return "Login"
    if row.get('page') == "Watchlist":
        return "Watchlist"
    if row.get('page') == "Order Window":
        return "Orderbook"
    if row.get('page') == 'Dashboard':
        return "Dashboard"
    if row.get('page') == 'Order Book':
        return "Order Book"
    if row.get('page') == 'Position':
        return "Position"
    if row.get('page') == 'Holdings':
        return "Holdings"
    if row.get('page') == 'Funds':
        return "Funds"
    if row.get('page') == 'Profile':
        return "Profile"
    return None


df['module'] = df.apply(derive_module, axis=1)

# Keep only required modules
df = df.dropna(subset=['module'])

# -------------------------------
# Calculate summary dynamically
# -------------------------------
summary = df.groupby('module').agg(
    Total_Test_Case=('module', 'count'),
    Executed_Test_Case=('status', lambda x: x.notna().sum()),
    PASS=('status', lambda x: (x.str.lower() == 'pass').sum()),
    FAIL=('status', lambda x: (x.str.lower() == 'fail').sum())
).reset_index()

summary['Pending_Test_Case'] = (
        summary['Total_Test_Case'] - summary['Executed_Test_Case']
)

summary.insert(0, 'S No', range(1, len(summary) + 1))

summary.rename(columns={'module': 'Module'}, inplace=True)

summary = summary[
    ['S No', 'Module',
     'Total_Test_Case', 'Executed_Test_Case',
     'Pending_Test_Case', 'PASS', 'FAIL']
]


def derive_module(row):
    if pd.notna(row.get('username')) or pd.notna(row.get('otp')):
        return "Login"
    if row.get('page') == "Watchlist":
        return "Watchlist"
    if row.get('page') == "Order Window":
        return "Orderbook"
    if row.get('page') == 'Dashboard':
        return "Dashboard"
    if row.get('page') == 'Order Book':
        return "Order Book"
    if row.get('page') == 'Position':
        return "Position"
    if row.get('page') == 'Holdings':
        return "Holdings"
    if row.get('page') == 'Funds':
        return "Funds"
    if row.get('page') == 'Profile':
        return "Profile"
    return None


df['module'] = df.apply(derive_module, axis=1)

# Consider only valid modules
df = df.dropna(subset=['module'])

# -------------------------------
# Overall Summary Calculation
# -------------------------------
total_test_case = len(df)
executed_test_case = df['status'].notna().sum()
pending_test_case = total_test_case - executed_test_case

pass_count = (df['status'].str.lower() == 'pass').sum()
fail_count = (df['status'].str.lower() == 'fail').sum()

# -------------------------------
# Create Summary DataFrame
# -------------------------------
overall_summary = pd.DataFrame([{
    "Total Test Case": total_test_case,
    "Executed Test Case": executed_test_case,
    "Pending Test Case": pending_test_case,
    "PASS": pass_count,
    "FAIL": fail_count
}])

# -------------------------------
# Export CSV
# -------------------------------
overall_summary.to_csv("overall_execution_summary.csv", index=False)
# -------------------------------------------------
# SEND MAIL  ✅ FIXED CALL
# -------------------------------------------------
send_mail(
    subject="Pytest Automation Execution Report",
    df=final_df,  # detailed table
    df2=summary,
    df3=overall_summary,  # summary table
    csv_path=""  # attachment (optional)
)
