import re
from datetime import datetime

def parse_transactions(text):
    lines = text.strip().split('\n')
    transactions = []
    current_transaction = {}

    date_pattern = re.compile(r'^[A-Z][a-z]{2} \d{1,2}, \d{4}$')
    time_pattern = re.compile(r'^\d{1,2}:\d{2} [ap]m$', re.IGNORECASE)
    amount_pattern = re.compile(r'^₹[\d,]+$')

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if date_pattern.match(line):
            if current_transaction:
                # Finalize and append current transaction
                transactions.append({
                    "date": current_transaction.get("date", ""),
                    "description": current_transaction.get("description", "").strip(),
                    "amount": current_transaction.get("amount", 0.0),
                    "type": current_transaction.get("type", "DEBIT"),
                    "category": "Uncategorized"
                })
                current_transaction = {}
            current_transaction["date"] = line

            if i + 1 < len(lines) and time_pattern.match(lines[i+1].strip()):
                current_transaction["date"] += " " + lines[i+1].strip()
                i += 1
        elif line in ["DEBIT", "CREDIT"]:
            current_transaction["type"] = line
        elif amount_pattern.match(line):
            current_transaction["amount"] = float(line.replace("₹", "").replace(",", ""))
        else:
            if "description" not in current_transaction:
                current_transaction["description"] = ""
            current_transaction["description"] += line + " "
        
        i += 1

    # Don't forget to push the last transaction
    if current_transaction:
        transactions.append({
            "date": current_transaction.get("date", ""),
            "description": current_transaction.get("description", "").strip(),
            "amount": current_transaction.get("amount", 0.0),
            "type": current_transaction.get("type", "DEBIT"),
            "category": "Uncategorized"
        })

    return transactions
