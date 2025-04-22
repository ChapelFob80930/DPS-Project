# # # import streamlit as st
# # # import cv2
# # # from pyzbar.pyzbar import decode
# # # import requests
# # # import whois
# # # from datetime import datetime
# # # import csv
# # # import json
# # # from io import BytesIO
# # # import pandas as pd
# # # import numpy as np

# # # API_KEY = "AIzaSyCUj_bA0bwgtrut-Y5sC71efFxZKJ6f4s4"

# # # def check_url_with_google_safe_browsing(url):
# # #     endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
# # #     payload = {
# # #         "client": {"clientId": "qrscanner", "clientVersion": "1.0"},
# # #         "threatInfo": {
# # #             "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
# # #             "platformTypes": ["ANY_PLATFORM"],
# # #             "threatEntryTypes": ["URL"],
# # #             "threatEntries": [{"url": url}]
# # #         }
# # #     }

# # #     try:
# # #         response = requests.post(endpoint, json=payload)
# # #         result = response.json()
# # #         return "MALICIOUS" if result.get("matches") else "SAFE"
# # #     except Exception as e:
# # #         print("Error checking URL:", e)
# # #         return "ERROR"

# # # def get_domain_age(url):
# # #     try:
# # #         domain = url.split("//")[-1].split("/")[0]
# # #         w = whois.whois(domain)
# # #         creation_date = w.creation_date

# # #         if isinstance(creation_date, list):
# # #             creation_date = creation_date[0]

# # #         if creation_date is None:
# # #             return "Unknown (no creation date found)"

# # #         age_days = (datetime.now() - creation_date).days
# # #         return f"{'New' if age_days < 180 else 'Established'} Domain ({age_days} days old)"
# # #     except Exception as e:
# # #         print("WHOIS Lookup Failed:", e)
# # #         return "WHOIS Error"

# # # def process_qr_data(data):
# # #     status = check_url_with_google_safe_browsing(data)
# # #     age_info = get_domain_age(data)
# # #     return status, age_info

# # # def export_results(results, format="csv"):
# # #     df = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age"])
# # #     if format == "csv":
# # #         csv_buffer = BytesIO()
# # #         df.to_csv(csv_buffer, index=False)
# # #         return csv_buffer.getvalue()
# # #     elif format == "json":
# # #         return json.dumps([{"qr_data": r[0], "safety": r[1], "domain_age": r[2]} for r in results], indent=4)

# # # # Streamlit UI Setup
# # # st.set_page_config(page_title="Live QR Code Security Scanner", layout="wide")

# # # st.title("🔍 Live QR Code Security Scanner")
# # # st.write("Scan QR codes using your webcam and check their safety using Google Safe Browsing and WHOIS domain age.")

# # # start = st.button("📸 Start Scanning")

# # # results = []

# # # if start:
# # #     cap = cv2.VideoCapture(0)
# # #     stframe = st.empty()
# # #     scanned = set()

# # #     stop_button = st.button("🛑 Stop Scanning", key="stop_button")
# # #     stop = False

# # #     while cap.isOpened() and not stop:
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             st.warning("❌ Failed to access the webcam.")
# # #             break

# # #         decoded_objs = decode(frame)

# # #         for obj in decoded_objs:
# # #             data = obj.data.decode('utf-8')

# # #             if data not in scanned:
# # #                 scanned.add(data)
# # #                 status, age_info = process_qr_data(data)
# # #                 results.append((data, status, age_info))

# # #         # Draw rectangle around QR codes
# # #         for obj in decoded_objs:
# # #             points = obj.polygon
# # #             if len(points) > 4:
# # #                 hull = cv2.convexHull(np.array([p for p in points], dtype=np.float32))
# # #                 hull = list(map(tuple, np.squeeze(hull)))
# # #             else:
# # #                 hull = points
# # #             n = len(hull)
# # #             for j in range(0, n):
# # #                 cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

# # #         stframe.image(frame, channels="BGR")

# # #         # Stop logic
# # #         if stop_button:
# # #             stop = True

# # #     cap.release()
# # #     cv2.destroyAllWindows()

# # # # Show results
# # # if results:
# # #     st.subheader("✅ Scan Results")
# # #     df_results = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age"])
# # #     st.dataframe(df_results)

# # #     csv_data = export_results(results, format="csv")
# # #     json_data = export_results(results, format="json")

# # #     st.download_button("⬇️ Download CSV", data=csv_data, file_name="qr_results.csv", mime="text/csv")
# # #     st.download_button("⬇️ Download JSON", data=json_data, file_name="qr_results.json", mime="application/json")
# # import streamlit as st
# # import cv2
# # from pyzbar.pyzbar import decode
# # import requests
# # import whois
# # from datetime import datetime
# # import csv
# # import json
# # from io import BytesIO
# # import pandas as pd
# # import numpy as np
# # import re
# # from bs4 import BeautifulSoup

# # API_KEY = "AIzaSyCUj_bA0bwgtrut-Y5sC71efFxZKJ6f4s4"

# # def check_url_with_google_safe_browsing(url):
# #     endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
# #     payload = {
# #         "client": {"clientId": "qrscanner", "clientVersion": "1.0"},
# #         "threatInfo": {
# #             "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
# #             "platformTypes": ["ANY_PLATFORM"],
# #             "threatEntryTypes": ["URL"],
# #             "threatEntries": [{"url": url}]
# #         }
# #     }

# #     try:
# #         response = requests.post(endpoint, json=payload)
# #         result = response.json()
# #         return "MALICIOUS" if result.get("matches") else "SAFE"
# #     except Exception as e:
# #         print("Error checking URL:", e)
# #         return "ERROR"

# # def get_domain_age(url):
# #     try:
# #         domain = url.split("//")[-1].split("/")[0]
# #         w = whois.whois(domain)
# #         creation_date = w.creation_date

# #         if isinstance(creation_date, list):
# #             creation_date = creation_date[0]

# #         if creation_date is None:
# #             return "Unknown (no creation date found)"

# #         age_days = (datetime.now() - creation_date).days
# #         return f"{'New' if age_days < 180 else 'Established'} Domain ({age_days} days old)"
# #     except Exception as e:
# #         print("WHOIS Lookup Failed:", e)
# #         return "WHOIS Error"

# # def get_website_owner(url):
# #     try:
# #         domain = url.split("//")[-1].split("/")[0]
# #         w = whois.whois(domain)
        
# #         # Try different fields where owner info might be found
# #         if w.org:
# #             return w.org
# #         elif w.registrant_organization:
# #             return w.registrant_organization
# #         elif w.name:
# #             return w.name
# #         elif w.registrant_name:
# #             return w.registrant_name
# #         else:
# #             return "Owner information not available"
# #     except Exception as e:
# #         print("Owner Lookup Failed:", e)
# #         return "Owner information not available"

# # def detect_site_type(url):
# #     try:
# #         headers = {
# #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# #         }
# #         response = requests.get(url, headers=headers, timeout=5)
# #         if response.status_code != 200:
# #             return "Unknown"
        
# #         # Parse HTML
# #         soup = BeautifulSoup(response.text, 'html.parser')
        
# #         # Check title and meta descriptions for common patterns
# #         title = soup.title.string if soup.title else ""
# #         meta_desc = ""
# #         if soup.find("meta", attrs={"name": "description"}):
# #             meta_desc = soup.find("meta", attrs={"name": "description"}).get("content", "")
        
# #         # Check for educational sites
# #         if re.search(r'university|college|school|education|academy|institute|learn', title.lower() + " " + meta_desc.lower()):
# #             return "Education"
# #         # Check for e-commerce
# #         elif re.search(r'shop|store|buy|product|cart|checkout|order', title.lower() + " " + meta_desc.lower()):
# #             return "E-commerce"
# #         # Check for social media
# #         elif re.search(r'social|community|connect|network|forum|share|profile', title.lower() + " " + meta_desc.lower()):
# #             return "Social Media"
# #         # Check for news/blog
# #         elif re.search(r'news|blog|article|post|journal|magazine', title.lower() + " " + meta_desc.lower()):
# #             return "News/Blog"
# #         # Check for corporate/business
# #         elif re.search(r'company|business|corporate|enterprise|firm|industry|service', title.lower() + " " + meta_desc.lower()):
# #             return "Corporate/Business"
# #         # Check for government
# #         elif re.search(r'government|gov|official|agency|department|public', title.lower() + " " + meta_desc.lower()) or url.endswith('.gov'):
# #             return "Government"
# #         # Banking/Financial
# #         elif re.search(r'bank|finance|payment|money|credit|invest', title.lower() + " " + meta_desc.lower()):
# #             return "Financial/Banking"
# #         else:
# #             return "General Website"
            
# #     except Exception as e:
# #         print(f"Error detecting site type: {e}")
# #         return "Unknown"

# # def process_qr_data(data):
# #     status = check_url_with_google_safe_browsing(data)
# #     age_info = get_domain_age(data)
# #     owner_info = get_website_owner(data)
# #     site_type = detect_site_type(data)
# #     return status, age_info, owner_info, site_type

# # def export_results(results, format="csv"):
# #     df = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
# #     if format == "csv":
# #         csv_buffer = BytesIO()
# #         df.to_csv(csv_buffer, index=False)
# #         return csv_buffer.getvalue()
# #     elif format == "json":
# #         return json.dumps([{"qr_data": r[0], "safety": r[1], "domain_age": r[2], "owner": r[3], "site_type": r[4]} for r in results], indent=4)

# # # Streamlit UI Setup
# # st.set_page_config(page_title="Live QR Code Security Scanner", layout="wide")

# # st.title("🔍 Live QR Code Security Scanner")
# # st.write("Scan QR codes using your webcam and check their safety using Google Safe Browsing, WHOIS domain age, owner information, and website type.")

# # start = st.button("📸 Start Scanning")

# # results = []

# # if start:
# #     cap = cv2.VideoCapture(0)
# #     stframe = st.empty()
# #     scanned = set()

# #     stop_button = st.button("🛑 Stop Scanning", key="stop_button")
# #     stop = False

# #     while cap.isOpened() and not stop:
# #         ret, frame = cap.read()
# #         if not ret:
# #             st.warning("❌ Failed to access the webcam.")
# #             break

# #         decoded_objs = decode(frame)

# #         for obj in decoded_objs:
# #             data = obj.data.decode('utf-8')

# #             if data not in scanned:
# #                 scanned.add(data)
# #                 with st.spinner(f"Analyzing {data}..."):
# #                     status, age_info, owner_info, site_type = process_qr_data(data)
# #                     results.append((data, status, age_info, owner_info, site_type))
# #                     st.success(f"New QR Code analyzed: {data}")

# #         # Draw rectangle around QR codes
# #         for obj in decoded_objs:
# #             points = obj.polygon
# #             if len(points) > 4:
# #                 hull = cv2.convexHull(np.array([p for p in points], dtype=np.float32))
# #                 hull = list(map(tuple, np.squeeze(hull)))
# #             else:
# #                 hull = points
# #             n = len(hull)
# #             for j in range(0, n):
# #                 cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

# #         stframe.image(frame, channels="BGR")

# #         # Stop logic
# #         if stop_button:
# #             stop = True

# #     cap.release()
# #     cv2.destroyAllWindows()

# # # Show results
# # if results:
# #     st.subheader("✅ Scan Results")
# #     df_results = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
# #     st.dataframe(df_results)

# #     csv_data = export_results(results, format="csv")
# #     json_data = export_results(results, format="json")

# #     st.download_button("⬇️ Download CSV", data=csv_data, file_name="qr_results.csv", mime="text/csv")
# #     st.download_button("⬇️ Download JSON", data=json_data, file_name="qr_results.json", mime="application/json")

# import streamlit as st
# import cv2
# from pyzbar.pyzbar import decode
# import requests
# import whois
# from datetime import datetime
# import csv
# import json
# from io import BytesIO
# import pandas as pd
# import numpy as np
# import re
# from bs4 import BeautifulSoup

# API_KEY = "AIzaSyCUj_bA0bwgtrut-Y5sC71efFxZKJ6f4s4"

# def check_url_with_google_safe_browsing(url):
#     endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
#     payload = {
#         "client": {"clientId": "qrscanner", "clientVersion": "1.0"},
#         "threatInfo": {
#             "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
#             "platformTypes": ["ANY_PLATFORM"],
#             "threatEntryTypes": ["URL"],
#             "threatEntries": [{"url": url}]
#         }
#     }

#     try:
#         response = requests.post(endpoint, json=payload)
#         result = response.json()
#         return "MALICIOUS" if result.get("matches") else "SAFE"
#     except Exception as e:
#         print("Error checking URL:", e)
#         return "ERROR"

# def get_domain_age(url):
#     try:
#         domain = url.split("//")[-1].split("/")[0]
#         w = whois.whois(domain)
#         creation_date = w.creation_date

#         if isinstance(creation_date, list):
#             creation_date = creation_date[0]

#         if creation_date is None:
#             return "Unknown (no creation date found)"

#         age_days = (datetime.now() - creation_date).days
#         return f"{'New' if age_days < 180 else 'Established'} Domain ({age_days} days old)"
#     except Exception as e:
#         print("WHOIS Lookup Failed:", e)
#         return "WHOIS Error"

# def get_website_owner(url):
#     try:
#         domain = url.split("//")[-1].split("/")[0]
#         w = whois.whois(domain)
        
#         # Try different fields where owner info might be found
#         if w.org:
#             return w.org
#         elif w.registrant_organization:
#             return w.registrant_organization
#         elif w.name:
#             return w.name
#         elif w.registrant_name:
#             return w.registrant_name
#         else:
#             return "Owner information not available"
#     except Exception as e:
#         print("Owner Lookup Failed:", e)
#         return "Owner information not available"

# def detect_site_type(url):
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
#         response = requests.get(url, headers=headers, timeout=5)
#         if response.status_code != 200:
#             return "Unknown"
        
#         # Parse HTML
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Check title and meta descriptions for common patterns
#         title = soup.title.string if soup.title else ""
#         meta_desc = ""
#         if soup.find("meta", attrs={"name": "description"}):
#             meta_desc = soup.find("meta", attrs={"name": "description"}).get("content", "")
        
#         # Check for educational sites
#         if re.search(r'university|college|school|education|academy|institute|learn', title.lower() + " " + meta_desc.lower()):
#             return "Education"
#         # Check for e-commerce
#         elif re.search(r'shop|store|buy|product|cart|checkout|order', title.lower() + " " + meta_desc.lower()):
#             return "E-commerce"
#         # Check for social media
#         elif re.search(r'social|community|connect|network|forum|share|profile', title.lower() + " " + meta_desc.lower()):
#             return "Social Media"
#         # Check for news/blog
#         elif re.search(r'news|blog|article|post|journal|magazine', title.lower() + " " + meta_desc.lower()):
#             return "News/Blog"
#         # Check for corporate/business
#         elif re.search(r'company|business|corporate|enterprise|firm|industry|service', title.lower() + " " + meta_desc.lower()):
#             return "Corporate/Business"
#         # Check for government
#         elif re.search(r'government|gov|official|agency|department|public', title.lower() + " " + meta_desc.lower()) or url.endswith('.gov'):
#             return "Government"
#         # Banking/Financial
#         elif re.search(r'bank|finance|payment|money|credit|invest', title.lower() + " " + meta_desc.lower()):
#             return "Financial/Banking"
#         else:
#             return "General Website"
            
#     except Exception as e:
#         print(f"Error detecting site type: {e}")
#         return "Unknown"

# def process_qr_data(data):
#     status = check_url_with_google_safe_browsing(data)
#     age_info = get_domain_age(data)
#     owner_info = get_website_owner(data)
#     site_type = detect_site_type(data)
#     return status, age_info, owner_info, site_type

# def export_results(results, format="csv"):
#     df = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
#     if format == "csv":
#         csv_buffer = BytesIO()
#         df.to_csv(csv_buffer, index=False)
#         return csv_buffer.getvalue()
#     elif format == "json":
#         return json.dumps([{"qr_data": r[0], "safety": r[1], "domain_age": r[2], "owner": r[3], "site_type": r[4]} for r in results], indent=4)

# # Streamlit UI Setup
# st.set_page_config(page_title="Live QR Code Security Scanner", layout="wide")

# st.title("🔍 Live QR Code Security Scanner")
# st.write("Scan QR codes using your webcam and check their safety using Google Safe Browsing, WHOIS domain age, owner information, and website type.")

# # Initialize session state for results if it doesn't exist
# if 'results' not in st.session_state:
#     st.session_state.results = []

# # Create a placeholder for the results table that will be updated in real-time
# results_placeholder = st.empty()

# # Function to display current results
# def show_current_results():
#     if st.session_state.results:
#         df_results = pd.DataFrame(st.session_state.results, 
#                                  columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
#         results_placeholder.dataframe(df_results)

# # Show any existing results when page loads
# show_current_results()

# # Start scanning button
# if st.button("📸 Start Scanning"):
#     cap = cv2.VideoCapture(0)
#     stframe = st.empty()
#     scanned = set()  # Keep track of already scanned QR codes
    
#     # Create a placeholder for the stop button
#     stop_button_placeholder = st.empty()
#     stop = stop_button_placeholder.button("🛑 Stop Scanning", key="stop_button")
    
#     # Create a placeholder for status messages
#     status_placeholder = st.empty()
    
#     while cap.isOpened() and not stop:
#         ret, frame = cap.read()
#         if not ret:
#             status_placeholder.warning("❌ Failed to access the webcam.")
#             break

#         decoded_objs = decode(frame)

#         for obj in decoded_objs:
#             data = obj.data.decode('utf-8')

#             if data not in scanned:
#                 scanned.add(data)
#                 status_placeholder.info(f"Analyzing QR Code: {data}")
                
#                 # Process the QR data
#                 status, age_info, owner_info, site_type = process_qr_data(data)
                
#                 # Add to results
#                 st.session_state.results.append((data, status, age_info, owner_info, site_type))
                
#                 # Update the results display
#                 show_current_results()
                
#                 # Show success message
#                 status_placeholder.success(f"New QR Code analyzed: {data}")
                
#                 # Display detailed result for the latest scan
#                 st.subheader(f"Latest QR Code Result")
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.markdown(f"**URL:** {data}")
#                     st.markdown(f"**Safety Status:** {status}")
#                     st.markdown(f"**Domain Age:** {age_info}")
#                 with col2:
#                     st.markdown(f"**Owner:** {owner_info}")
#                     st.markdown(f"**Site Type:** {site_type}")

#         # Draw rectangle around QR codes
#         for obj in decoded_objs:
#             points = obj.polygon
#             if len(points) > 4:
#                 hull = cv2.convexHull(np.array([p for p in points], dtype=np.float32))
#                 hull = list(map(tuple, np.squeeze(hull)))
#             else:
#                 hull = points
#             n = len(hull)
#             for j in range(0, n):
#                 cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

#         stframe.image(frame, channels="BGR")

#         # Check if stop button was pressed
#         stop = stop_button_placeholder.button("🛑 Stop Scanning", key=f"stop_button_{datetime.now().timestamp()}")

#     cap.release()
#     cv2.destroyAllWindows()

# # Show export options if there are results
# if st.session_state.results:
#     st.subheader("✅ Export Results")
    
#     csv_data = export_results(st.session_state.results, format="csv")
#     json_data = export_results(st.session_state.results, format="json")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.download_button("⬇️ Download CSV", data=csv_data, file_name="qr_results.csv", mime="text/csv")
#     with col2:
#         st.download_button("⬇️ Download JSON", data=json_data, file_name="qr_results.json", mime="application/json")
    
#     # Option to clear results
#     if st.button("🗑️ Clear Results"):
#         st.session_state.results = []
#         st.experimental_rerun()

import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import requests
import whois
from datetime import datetime
import csv
import json
from io import BytesIO
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import time

API_KEY = "AIzaSyCUj_bA0bwgtrut-Y5sC71efFxZKJ6f4s4"

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
        return "MALICIOUS" if result.get("matches") else "SAFE"
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
        return f"{'New' if age_days < 180 else 'Established'} Domain ({age_days} days old)"
    except Exception as e:
        print("WHOIS Lookup Failed:", e)
        return "WHOIS Error"

def get_website_owner(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        w = whois.whois(domain)
        
        # Try different fields where owner info might be found
        if w.org:
            return w.org
        elif w.registrant_organization:
            return w.registrant_organization
        elif w.name:
            return w.name
        elif w.registrant_name:
            return w.registrant_name
        else:
            return "Owner information not available"
    except Exception as e:
        print("Owner Lookup Failed:", e)
        return "Owner information not available"

def detect_site_type(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return "Unknown"
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check title and meta descriptions for common patterns
        title = soup.title.string if soup.title else ""
        meta_desc = ""
        if soup.find("meta", attrs={"name": "description"}):
            meta_desc = soup.find("meta", attrs={"name": "description"}).get("content", "")
        
        # Check for educational sites
        if re.search(r'university|college|school|education|academy|institute|learn', title.lower() + " " + meta_desc.lower()):
            return "Education"
        # Check for e-commerce
        elif re.search(r'shop|store|buy|product|cart|checkout|order', title.lower() + " " + meta_desc.lower()):
            return "E-commerce"
        # Check for social media
        elif re.search(r'social|community|connect|network|forum|share|profile', title.lower() + " " + meta_desc.lower()):
            return "Social Media"
        # Check for news/blog
        elif re.search(r'news|blog|article|post|journal|magazine', title.lower() + " " + meta_desc.lower()):
            return "News/Blog"
        # Check for corporate/business
        elif re.search(r'company|business|corporate|enterprise|firm|industry|service', title.lower() + " " + meta_desc.lower()):
            return "Corporate/Business"
        # Check for government
        elif re.search(r'government|gov|official|agency|department|public', title.lower() + " " + meta_desc.lower()) or url.endswith('.gov'):
            return "Government"
        # Banking/Financial
        elif re.search(r'bank|finance|payment|money|credit|invest', title.lower() + " " + meta_desc.lower()):
            return "Financial/Banking"
        else:
            return "General Website"
            
    except Exception as e:
        print(f"Error detecting site type: {e}")
        return "Unknown"

def process_qr_data(data):
    status = check_url_with_google_safe_browsing(data)
    age_info = get_domain_age(data)
    owner_info = get_website_owner(data)
    site_type = detect_site_type(data)
    return status, age_info, owner_info, site_type

def export_results(results, format="csv"):
    df = pd.DataFrame(results, columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
    if format == "csv":
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    elif format == "json":
        return json.dumps([{"qr_data": r[0], "safety": r[1], "domain_age": r[2], "owner": r[3], "site_type": r[4]} for r in results], indent=4)

# Streamlit UI Setup
st.set_page_config(page_title="Live QR Code Security Scanner", layout="wide")

st.title("🔍 Live QR Code Security Scanner")
st.write("Scan QR codes using your webcam and check their safety using Google Safe Browsing, WHOIS domain age, owner information, and website type.")

# Initialize session state variables
if 'results' not in st.session_state:
    st.session_state.results = []

# Create placeholders for dynamic content
status_placeholder = st.empty()
control_placeholder = st.empty()
camera_placeholder = st.empty()
results_placeholder = st.empty()
latest_scan_placeholder = st.empty()

# Show existing results
if st.session_state.results:
    with results_placeholder.container():
        st.subheader("✅ Scan Results")
        df_results = pd.DataFrame(st.session_state.results, 
                                 columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
        st.dataframe(df_results)
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            csv_data = export_results(st.session_state.results, format="csv")
            st.download_button("⬇️ Download CSV", data=csv_data, file_name="qr_results.csv", mime="text/csv")
        with col2:
            json_data = export_results(st.session_state.results, format="json")
            st.download_button("⬇️ Download JSON", data=json_data, file_name="qr_results.json", mime="application/json")
        
        # Clear results button
        if st.button("🗑️ Clear Results"):
            st.session_state.results = []
            st.rerun()

# Start scanning button
start_button = st.button("📸 Start Scanning")

if start_button:
    # Create a stop button
    if control_placeholder.button("🛑 Stop Scanning", key="stop_button"):
        st.stop()
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            status_placeholder.error("❌ Unable to access webcam. Please check your camera settings.")
            st.stop()
            
        scanned = set()  # Keep track of already scanned QR codes
        
        while True:
            # Check if camera is still open and get frame
            ret, frame = cap.read()
            if not ret:
                status_placeholder.error("❌ Failed to read from webcam.")
                break

            # Display the camera feed
            camera_placeholder.image(frame, channels="BGR")
            
            # Decode QR codes
            decoded_objs = decode(frame)

            # Process detected QR codes
            for obj in decoded_objs:
                try:
                    data = obj.data.decode('utf-8')
                    
                    # Draw rectangle around QR code
                    points = obj.polygon
                    if len(points) > 4:
                        hull = cv2.convexHull(np.array([p for p in points], dtype=np.float32))
                        hull = list(map(tuple, np.squeeze(hull)))
                    else:
                        hull = points
                    n = len(hull)
                    for j in range(0, n):
                        cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)
                    
                    # Only process new QR codes
                    if data not in scanned:
                        scanned.add(data)
                        status_placeholder.info(f"New QR Code analyzed: {data}")
                        
                        # Process the QR data
                        status, age_info, owner_info, site_type = process_qr_data(data)
                        
                        # Add to results
                        st.session_state.results.append((data, status, age_info, owner_info, site_type))
                        
                        # Show latest scan details
                        with latest_scan_placeholder.container():
                            st.subheader("Last Scanned Result")
                            cols = st.columns(3)
                            with cols[0]:
                                st.markdown(f"**URL:** {data}")
                                st.markdown(f"**Safety:** {status}")
                            with cols[1]:
                                st.markdown(f"**Domain Age:** {age_info}")
                                st.markdown(f"**Owner:** {owner_info}")
                            with cols[2]:
                                st.markdown(f"**Site Type:** {site_type}")
                        
                        # Update results display
                        with results_placeholder.container():
                            st.subheader("✅ Scan Results")
                            df_results = pd.DataFrame(st.session_state.results, 
                                                    columns=["QR Data", "Safety", "Domain Age", "Owner", "Site Type"])
                            st.dataframe(df_results)
                            
                            # Export options
                            col1, col2 = st.columns(2)
                            with col1:
                                csv_data = export_results(st.session_state.results, format="csv")
                                st.download_button("⬇️ Download CSV", data=csv_data, file_name="qr_results.csv", mime="text/csv")
                            with col2:
                                json_data = export_results(st.session_state.results, format="json")
                                st.download_button("⬇️ Download JSON", data=json_data, file_name="qr_results.json", mime="application/json")
                except Exception as e:
                    status_placeholder.error(f"Error processing QR code: {e}")
            
            # Update camera display
            camera_placeholder.image(frame, channels="BGR")
            
            # Small sleep to prevent high CPU usage
            time.sleep(0.1)
            
    except Exception as e:
        status_placeholder.error(f"An error occurred: {e}")
    finally:
        # Always clean up
        try:
            cap.release()
        except:
            pass