
# 🚀 Jira to ServiceNow Incident Automation

This project demonstrates how to **automatically create a ServiceNow Incident** whenever a **new Jira issue** is created — using **Python**, **Flask**, the **Jira Webhook**, and **ServiceNow REST API**.

---

## 📌 Use Case

- Whenever a user creates a new Jira ticket (e.g., `BUG-123`), this script:
  1. Receives a webhook payload from Jira.
  2. Creates an Incident in ServiceNow using the REST API.
  3. Optionally, adds a comment back to the Jira ticket with the ServiceNow Incident number.

---

## ✅ Prerequisites

### 1. Jira Cloud (Free)
- [Sign up for Jira Cloud](https://www.atlassian.com/software/jira/free) (up to 10 users).
- Create a project (e.g., **BUG**).
- Generate a Jira API Token:
  - [Create API Token](https://id.atlassian.com/manage/api-tokens)

### 2. ServiceNow Developer Instance (Free)
- [Sign up for a free Personal Developer Instance (PDI)](https://developer.servicenow.com/).
- Request an instance and note:
  - Instance URL: `https://devXXXXX.service-now.com`
  - Username: `admin`
  - Password: (your chosen password)

### 3. Python & Dependencies
- Python 3.x installed on your local machine.
- Packages: `flask`, `requests`, `python-dotenv`

---

## ✅ Setup

### 1. Clone this repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>


### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your configuration

Add .env file: 

# Jira Config

JIRA_INSTANCE=https://your-site.atlassian.net

JIRA_USER=your-email@example.com

JIRA_API_TOKEN=your-jira-api-token


# ServiceNow Config

SNOW_INSTANCE=https://devXXXXX.service-now.com

SNOW_USER=your-snow-username

SNOW_PASSWORD=your-snow-password

SNOW_TABLE=incident

---

## ✅ How to Run Locally

### 1. Start your Flask server

```bash
python jira_to_servicenow.py
```

By default, Flask runs on `http://localhost:5000`.

### 2. Expose your local server with ngrok

Jira (cloud) must reach your local server. Use ngrok:

1. [Download ngrok](https://ngrok.com/download)
   
2. Run ngrok directly (Quick Method)
   
If you don’t want to add it to PATH yet:

Open Command Prompt in the folder containing ngrok.exe

 ```bash
   ngrok http 5000
   ```
 This will work as long as you run it from that folder.
 
3. Authenticate:
Sign in and add your auth token (First Time)

Sign up for a free ngrok account: https://dashboard.ngrok.com/signup

Copy your AuthToken.

   ```bash
   ngrok config add-authtoken <your-ngrok-auth-token>
   ```
3. Start the tunnel:

   ```bash
   ngrok http 5000
   ```

You’ll get a forwarding URL like:

```
Forwarding https://abcd1234.ngrok.io → http://localhost:5000
```

### 3. Configure the Jira Webhook

In Jira Cloud:

* Go to **⚙️ Settings → System → Webhooks**
* Add a new webhook:

  * **URL:** `https://abcd1234.ngrok.io/webhook`
  * **Event:** `Issue Created`
* Save it.

---

## ✅ How to Test

### 1. Create a new Jira issue

* Click **Create** in Jira.
* Fill in:

  * **Project:** `BUG` (or your project)
  * **Issue type:** `Bug`
  * **Summary:** `Test ServiceNow Integration`
  * **Description:** `This issue tests the automation script.`

When you create it, Jira triggers the webhook.

### 2. Watch your Flask console

* You should see the webhook JSON payload.
* If successful, you’ll see:

  ```
  Created ServiceNow Incident: INC0010005
  ```

### 3. Check in ServiceNow

* Log in to your PDI: `https://devXXXXX.service-now.com`
* In the left nav, search `Incident`.

  * Go to **Incident → All**.
  * Sort by **Created On** descending.
* You should see your new Incident:

  ```
  Short Description: [Jira BUG-123] Test ServiceNow Integration
  ```

---

## ✅ Troubleshooting Tips

* **Jira → ngrok not working?**

  * Restart ngrok and update your webhook with the new URL.
* **401 Unauthorized?**

  * Check your API tokens for Jira and ServiceNow credentials.
* **ServiceNow Incident not appearing?**

  * Use **REST API Explorer** in your PDI to confirm POST works.
* **Script crashes?**

  * Double-check your `.env` or hardcoded credentials.

---

## ✅ Next Steps for Production

* Deploy this Flask app to a server (AWS EC2, Railway, Heroku, etc.).
* Store secrets securely using environment variables or a vault.
* Use HTTPS and OAuth for ServiceNow if possible.
* Implement retries & logging for reliability.

---


## 🙌 Need Help?

Feel free to open an issue or pull request.
Enjoy automating your Jira + ServiceNow workflows! 🚀

