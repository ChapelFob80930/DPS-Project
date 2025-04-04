import cv2
from pyzbar.pyzbar import decode
import requests
import whois
from datetime import datetime
import csv
import json
import argparse

API_KEY = "AIzaSyCUj_bA0bwgtrut-Y5sC71efFxZKJ6f4s4"

def scan_qr_codes(image_path):
    image = cv2.imread(image_path)
    qr_codes = decode(image)

    if not qr_codes:
        print("No QR codes found.")
        return []

    extracted_data = []
    for i, qr in enumerate(qr_codes):
        data = qr.data.decode('utf-8')
        print(f"\n[QR {i+1}] Data: {data}")

        status = check_url_with_google_safe_browsing(data)
        age_info = get_domain_age(data)

        print(f"    Safety: {status}")
        print(f"    Domain Age: {age_info}")

        extracted_data.append((data, status, age_info))

    return extracted_data

def check_url_with_google_safe_browsing(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    payload = {
        "client": {"clientId": "qrscanner", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()
        if result.get("matches"):
            return "MALICIOUS"
        else:
            return "SAFE"
    except Exception as e:
        print("Error checking URL:", e)
        return "ERROR"

def get_domain_age(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return "Unknown (no creation date found)"

        age_days = (datetime.now() - creation_date).days

        if age_days < 180:
            return f"New Domain ({age_days} days old)"
        else:
            return f"Established Domain ({age_days} days old)"
    except Exception as e:
        print("WHOIS Lookup Failed:", e)
        return "WHOIS Error"

def export_to_csv(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["QR Data", "Safety", "Domain Age"])
        for row in results:
            writer.writerow(row)
    print(f"\nResults exported to {filename}")

def export_to_json(results, filename):
    data = [
        {"qr_data": r[0], "safety": r[1], "domain_age": r[2]}
        for r in results
    ]
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Results exported to {filename}")

def main():
    parser = argparse.ArgumentParser(description="QR Code Security Scanner")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--csv", help="Path to save CSV output")
    parser.add_argument("--json", help="Path to save JSON output")
    args = parser.parse_args()

    results = scan_qr_codes(args.image)

    if results:
        if args.csv:
            export_to_csv(results, args.csv)
        if args.json:
            export_to_json(results, args.json)

if __name__ == "__main__":
    main()
