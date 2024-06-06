import requests

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRCSGNQS0l1RzFDb0V2UWtMekFYZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1mM2I2cWFxMTZ1Z3oyaWF0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJsaW5rZWRpbnxLbXhaVUczTXhKIiwiYXVkIjpbImh0dHBzOi8vdG9rZW4vdXNlcl9pbmZvIiwiaHR0cHM6Ly9kZXYtZjNiNnFhcTE2dWd6MmlhdC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzE0NjMzMjYwLCJleHAiOjE3MTQ3MTk2NjAsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiI2WDRGeEV4MlQ2RUNUQXdZQk43V2Y2WTZCcTVRaXNGeiJ9.crkoysY9tIZpcqiuMTNfkyZgwNiJ5VQ9bmXwa5ChyobsUIzInswRsjPRpIrQV7F0mfsZL2GJ4PpUyFQ2X4hncUWo9mxsq5ooxhxuNwb_rR8-xodhrLXNRusMgJTWely5UtJLH9s4Hu1OEh1YZhkz9B7ph6JHzXhpvsfHvIrIqw8vDxzJpiHOPPoTeEDiXRlQIRwn0ltIN-PQYddm3seNhC7gmex_xCWelwuJcfS9K2dLi6lxNc2zfkIOGAvyZXjtFwwINdwny5fuJJ-yncTG53PmM21xEO3XmZazWrXQQG6Zk25vSoKFoMKJ87W27I_QRfbzf0p4eQD3cBH-Vft4mA"
headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

response = requests.get("https://dev-f3b6qaq16ugz2iat.us.auth0.com/userinfo", headers=headers)
if response.status_code == 200:
    user_info = response.json()
    print(user_info)