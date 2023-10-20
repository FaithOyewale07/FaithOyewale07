import requests
import json

# MythX API Credentials
MYTHX_API_KEY = "YOUR_MYTHX_API_KEY"
MYTHX_API_PASSWORD = "YOUR_MYTHX_API_PASSWORD"

# Smart Contract Code (Solidity Code)
SMART_CONTRACT_CODE = """
pragma solidity ^0.6.0;

contract VulnerableContract {
    uint256 public balance;

    function deposit(uint256 _amount) public {
        balance += _amount;
    }

    function withdraw(uint256 _amount) public {
        require(balance >= _amount, "Insufficient balance");
        balance -= _amount;
        msg.sender.transfer(_amount);
    }
}
"""


def analyze_smart_contract():
    # MythX API Endpoint
    api_url = "https://api.mythx.io/v1/analyses"

    # Prepare the request payload
    payload = {
        "data": {
            "type": "smartcontract",
            "attributes": {
                "bytecode": SMART_CONTRACT_CODE,
            }
        }
    }

    # Make the API request
    response = requests.post(api_url, json=payload, auth=(MYTHX_API_KEY, MYTHX_API_PASSWORD))

    if response.status_code == 202:
        analysis_uuid = response.json()["data"]["id"]
        print(f"Analysis queued with UUID: {analysis_uuid}")

        # Poll the analysis status until it's completed
        status_url = f"https://api.mythx.io/v1/analyses/{analysis_uuid}"
        while True:
            status_response = requests.get(status_url, auth=(MYTHX_API_KEY, MYTHX_API_PASSWORD))
            status_data = status_response.json()["data"]["attributes"]["status"]
            print(f"Analysis Status: {status_data}")
            if status_data == "Complete":
                break

        # Get the analysis result
        result_url = f"https://api.mythx.io/v1/analyses/{analysis_uuid}/issues"
        result_response = requests.get(result_url, auth=(MYTHX_API_KEY, MYTHX_API_PASSWORD))
        issues = result_response.json()["data"]

        if issues:
            print("Smart Contract Vulnerabilities Found:")
            for issue in issues:
                print(f"Title: {issue['attributes']['swcTitle']}, Severity: {issue['attributes']['severity']}")
        else:
            print("No vulnerabilities found in the smart contract.")
    else:
        print("Error submitting the analysis request.")


if __name__ == "__main__":
    analyze_smart_contract()
