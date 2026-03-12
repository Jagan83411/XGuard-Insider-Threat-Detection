import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_employee_logs(n_employees=50, n_days=90):
    records = []
    employees = [fake.name() for _ in range(n_employees)]
    
    for emp in employees:
        normal_login = random.randint(8, 10)
        normal_files = random.randint(20, 60)
        is_malicious = random.random() < 0.1

        for day in range(n_days):
            login_hour = normal_login + random.randint(-1, 1)
            files_accessed = normal_files + random.randint(-10, 10)
            emails_sent = random.randint(5, 20)
            usb_used = 0
            after_hours = 0

            if is_malicious and day > 80:
                login_hour = random.randint(0, 4)
                files_accessed = normal_files * random.randint(5, 10)
                usb_used = 1
                after_hours = 1

            records.append({
                "employee": emp,
                "day": day,
                "login_hour": login_hour,
                "files_accessed": files_accessed,
                "emails_sent": emails_sent,
                "usb_used": usb_used,
                "after_hours": after_hours,
                "is_malicious": int(is_malicious and day > 80)
            })

    df = pd.DataFrame(records)
    df.to_csv("employee_logs.csv", index=False)
    print("✅ Data generated! employee_logs.csv created.")
    return df

if __name__ == "__main__":
    generate_employee_logs()