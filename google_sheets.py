from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Файл с ключом сервисного аккаунта
SERVICE_ACCOUNT_FILE = "service_account.json"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

def add_user(spreadsheet_id, user_id, username):
    values = [[user_id, username, "Фаза 0", 0]]
    sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range="Лист1!A:D",
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

def update_task_status(spreadsheet_id, user_id, task_number, status, answer):
    all_data = sheet.values().get(spreadsheetId=spreadsheet_id, range="Лист1!A:Z").execute()
    rows = all_data.get("values", [])
    for i, row in enumerate(rows):
        if str(row[0]) == str(user_id):
            col_status = 3 + task_number * 2
            col_answer = col_status + 1
            while len(row) <= col_answer:
                row.append("")
            row[col_status] = status
            row[col_answer] = answer
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"Лист1!A{i+1}:Z{i+1}",
                valueInputOption="RAW",
                body={"values": [row]}
            ).execute()
            break

def get_unfinished_tasks(spreadsheet_id, user_id):
    all_data = sheet.values().get(spreadsheetId=spreadsheet_id, range="Лист1!A:Z").execute()
    rows = all_data.get("values", [])
    unfinished = []
    for row in rows:
        if str(row[0]) == str(user_id):
            for i in range(3, len(row), 2):
                if i < len(row) and row[i] != "выполнено":
                    unfinished.append(f"Задание {(i-3)//2 + 1}")
            break
    return unfinished
