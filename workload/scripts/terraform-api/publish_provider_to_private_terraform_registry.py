import requests
import json
import re
import sys

# Terraform Cloud API token
terraform_token = "3MuM9yPtymjI8g.atlasv1.dO9bsLOJhFaRM3Org1lX1ZJmyjbkxMeHzjCLAkwJSQlJm7PpqAtdzOgDQPlbL6Faze0"

# GitHub API token
github_token = "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"

# Organization and provider details
organization = "deploymenttheory"
provider_name = "jamfpro"
version = "v10.48.0"

# GitHub repository details and paths to the files
github_repo = "deploymenttheory/terraform-provider-jamfpro"

# GPG signing key (ASCII-armored representation of a public GPG key)
public_gpg_key = """
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBGTHkbkBEAC7VvD7JFDHKmZfTO2YqO1cHICahFojsvO/2VTu43CpupSroAQt
xRNhFOCdLYokYXyeBAEgVI/4I03DDkYvs7bHARG0zrk0YJfx4W5+lcomIzHliP78
eE+F38TAQ+Rp0ojdfd8lWuI5AwhQ1bMl//q/4pAGB3SfNuXKY12Yjv3VdcfPebD2
Z1ETyHV9O7Vj5vDiCcffn9MkhvUljcal46lVcg32inbp7dzTrXM07WlDlzjGCLRa
ov7l//gsSP8TZZKnlUCkEdvOnfVd31g6lNQLgCzwwmBDC+JFMDUWT7gyihX/61vd
l1veVQlXa5UG+217xwUCggFNVw2O/nxFHGULcn0uJ7d/cStbBFXpgwm43CKlItjI
k0a/b62qUiGUi2CM7LOEnrnsTnyA6fyKOwntKZRYXmIUXp9hDEANPIORBJtyLKgV
RvKXLPW4jnwoLo/VMF1ru4kWkPE//5dDzRYYc12Agn9WPK4bplDrMWIP2An65Fid
keG+Rqpo/vtJA5qqw52S87eKLbPKcidr5wNR1bBX/710jpg6u6nlI+lYLwrMlzRW
Uss2NJjAHY2YOT0Riv56GlzpbO9ec89EQxrjHWe+tmhnYtwgOyyHoBdlvuamgFzJ
Wx3i7e0d27SEJPI4gUcdzOuu4g0gWT+4nyLoWEpeF7fDeFbtY+VSMg1JtwARAQAB
tDREYWZ5ZGQgV2F0a2lucyA8ZGFmeWRkLndhdGtpbnNAZGVwbG95bWVudHRoZW9y
eS5jb20+iQJUBBMBCAA+FiEEuKH0RG0grXpgYNritZD7yxRvE/wFAmTHkbkCGwMF
CQPCZwAFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AACgkQtZD7yxRvE/x70Q//d2mk
HOkp81CRoUHF+XVH6l2ljO160PFthxII9NwYhO8ezOW58+4n/RHV5GfXb+0RyIqJ
/EdWeRWS8SlEulUCcmexNiha+rmT+vHZjg8V4u+Hb/RplwrM1XkWHwTR/gpIWR9B
WtWXQMGkKigZkL6Nf9TzE24dtAE7SP9zQ3KvqnEfWxL1H9Kyh9xBatiBoFYP9TQ1
3JN3QwVrmut2Wji0d+DcYk4ubS8VPC3lU9zqhugmmHTZUUGQ0TfWEmmCEHp4OcMT
X7sA3MOTTgx3DPmVBDF/JECe7NTAh2GQdRDCFVGmZa4LA4icE8VnmOmBB7OLqFCK
LQ3g/iA+DLKTG3vOo0uhER960fTyxVmQe39a3gv54uOhP6KrEbeuknHRVeJLAO5g
46b7265YoWZ1c/m20zglOjvUMxeKNCtfO/MfeK3WopfQwKLX4lSYH1wpAXJLg+wN
dur3wjcrKtudunKGCS8ySIAXeQ8aJufKjvy0y0fv/le+qD8kym2Wc0eimkSjg2UF
0CVDXJx+8i7FWtnJPDT32xf7LfRcuUKae5KW+tX1Fjxbd5sFLkO907hDHmfV1iII
RbD6TExR2kT4RMvxCnjuKpeE8ja/bLkcxceglvSPtWqZ98iz30zHL6hlCV4L+V3X
wCDiwMuv2YZdljENgFtKNS1fYmPLvaJL/GnlllY=
=gOsY
-----END PGP PUBLIC KEY BLOCK------
"""

terraform_headers = {
    "Authorization": "Bearer " + terraform_token,
    "Content-Type": "application/vnd.api+json",
}

github_headers = {
    "Authorization": "token " + github_token,
}

# Error handling function
def handle_response(response, skip_gpg_error=False):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if skip_gpg_error and "GPG key already exists for namespace" in response.text:
            print("Skipping GPG key creation: GPG key already exists for namespace.")
        else:
            print(f"HTTP error occurred: {err}")
            print(f"Response headers: {response.headers}")
            print(f"Response content: {response.content}")
            print(response.text)  # print the response body
            exit(1)


# Use the GitHub API to get the release by tag
url = f"https://api.github.com/repos/{github_repo}/releases/tags/{version}"
response = requests.get(url, headers=github_headers)
handle_response(response)
assets = response.json()["assets"]

# Download an asset from GitHub
def download_asset(asset_url):
    response = requests.get(asset_url, headers=github_headers)
    handle_response(response)
    return response.content

# Create a provider
url = f"https://app.terraform.io/api/v2/organizations/{organization}/registry-providers"
data = {
    "data": {
        "type": "registry-providers",
        "attributes": {
            "name": provider_name,
            "namespace": organization,
            "registry-name": "private"
        }
    }
}
response = requests.post(url, headers=terraform_headers, data=json.dumps(data))
handle_response(response)
print("Provider created.")

# Add a GPG key
url = f"https://app.terraform.io/api/registry/private/v2/gpg-keys"
data = {
    "data": {
        "type": "gpg-keys",
        "attributes": {
            "namespace": organization,
            "ascii-armor": public_gpg_key,
        }
    }
}
response = requests.post(url, headers=terraform_headers, data=json.dumps(data))

# If the GPG key already exists, retrieve the existing one
if response.status_code == 400 and "GPG key already exists for namespace" in response.text:
    print("GPG key already exists for namespace. Retrieving the existing key.")
    response = requests.get(url, headers=terraform_headers, params={"filter[namespace]": organization})
    handle_response(response)
    keys = response.json()["data"]
    for key in keys:
        if key["attributes"]["namespace"] == organization and key["attributes"]["ascii-armor"] == public_gpg_key:
            key_id = key["id"]
            break
    else:
        print("No matching GPG key found.")
        exit(1)
else:
    handle_response(response)
    key_id = response.json()["data"]["id"]
print("GPG key added.")


# Create a provider version
url = f"https://app.terraform.io/api/v2/organizations/{organization}/registry-providers/private/{organization}/{provider_name}/versions"
data = {
    "data": {
        "type": "registry-provider-versions",
        "attributes": {
            "version": version,
            "key-id": key_id,
            "protocols": ["5.0"]
        }
    }
}

try:
    response = requests.post(url, headers=terraform_headers, data=json.dumps(data), timeout=30)
    response.raise_for_status()  # raises HTTPError if the request returns an HTTP status code that is 400 or above

    json_data = response.json()

    if 'data' not in json_data:
        print("The response does not contain expected 'data' field.")
        sys.exit(1)

    if 'links' not in json_data['data']:
        print("The 'data' field in the response does not contain expected 'links' field.")
        sys.exit(1)

    sha256sums_upload_url = json_data["data"]["links"].get("shasums-upload")
    if not sha256sums_upload_url:
        print("The 'links' field in the response does not contain 'shasums-upload' URL.")
        sys.exit(1)

    sha256sums_sig_upload_url = json_data["data"]["links"].get("shasums-sig-upload")
    if not sha256sums_sig_upload_url:
        print("The 'links' field in the response does not contain 'shasums-sig-upload' URL.")
        sys.exit(1)

    print("Provider version created.")

    # Upload SHA256SUMS and SHA256SUMS.sig
    for asset in assets:
        if asset["name"].endswith("_SHA256SUMS"):
            sha256sums = download_asset(asset["browser_download_url"])
            response = requests.put(sha256sums_upload_url, headers={"Content-Type": "application/octet-stream"}, data=sha256sums)
            handle_response(response)
            print("SHA256SUMS uploaded.")
        elif asset["name"].endswith("_SHA256SUMS.sig"):
            sha256sums_sig = download_asset(asset["browser_download_url"])
            response = requests.put(sha256sums_sig_upload_url, headers={"Content-Type": "application/octet-stream"}, data=sha256sums_sig)
            handle_response(response)
            print("SHA256SUMS.sig uploaded.")

except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
    print(f'Response content: {response.content}')

except requests.exceptions.RequestException as req_err:
    print(f'Request error occurred: {req_err}')

except json.JSONDecodeError as json_err:
    print(f'JSON decode error occurred: {json_err}')

except Exception as e:
    print(f'An error occurred: {e}')


# Parse SHA256SUMS
shasums_dict = {}
for line in sha256sums.decode("utf-8").split("\n"):  # <-- Fixed variable name here
    parts = line.split("  ")
    if len(parts) == 2:
        shasums_dict[parts[1]] = parts[0]


# Upload all provider binaries
for asset in assets:
    if asset["name"].endswith(".zip"):
        os_name, arch_name = re.findall(r"_(\w+)_", asset["name"])
        filename = asset["name"]
        shasum = shasums[filename]  # Retrieve the shasum from the parsed SHA256SUMS file
        provider_binary = download_asset(asset["browser_download_url"])
        url = f"https://app.terraform.io/api/v2/organizations/{organization}/registry-providers/private/{organization}/{provider_name}/versions/{version}/platforms"
        data = {
            "data": {
                "type": "registry-provider-platforms",
                "attributes": {
                    "os": os_name,
                    "arch": arch_name,
                    "shasum": shasum,
                    "filename": filename
                }
            }
        }
        response = requests.post(url, headers=terraform_headers, data=json.dumps(data))
        handle_response(response)
        provider_binary_upload_url = response.json()["data"]["links"]["provider-binary-upload"]
        response = requests.put(provider_binary_upload_url, headers={"Content-Type": "application/octet-stream"}, data=provider_binary)
        handle_response(response)
        print(f"Provider binary for {os_name} {arch_name} uploaded.")

