#!/usr/bin/env python3
"""
Test script for Payment Gateway Integration

This script tests the payment initialization endpoint to verify the integration is working.

Usage:
    python scripts/test_payment_integration.py
    python scripts/test_payment_integration.py --client-id 1
    python scripts/test_payment_integration.py --client-id 1 --credit-id 6
"""

import argparse
import json
import sys
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed")
    print("Install it with: pip install requests")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print("=" * len(title))


def test_payment_initialization(
    base_url: str,
    client_id: int,
    credit_id: Optional[int] = None
) -> bool:
    """
    Test the payment initialization endpoint.
    
    Args:
        base_url: Base URL of the API
        client_id: Client ID to test with
        credit_id: Optional credit ID to test with
        
    Returns:
        bool: True if test passed, False otherwise
    """
    endpoint = f"{base_url}/api/payments/v1/payments/initialize_payment"
    
    payload = {"client_id": client_id}
    if credit_id:
        payload["credit_id"] = credit_id
    
    print_section("Testing Payment Initialization")
    print_info(f"Endpoint: {endpoint}")
    print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print_info("Sending request...")
        response = requests.post(
            endpoint,
            json=payload,
            timeout=30
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print_section("Response")
            print(json.dumps(data, indent=2))
            
            # Validate response structure
            required_fields = ["success", "sessionId", "paymentUrl", "expiresIn", "message"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_error(f"Missing fields in response: {', '.join(missing_fields)}")
                return False
            
            if not data.get("success"):
                print_error("Response indicates failure")
                return False
            
            print_section("Validation")
            print_success(f"Success: {data['success']}")
            print_success(f"Session ID: {data['sessionId']}")
            print_success(f"Payment URL: {data['paymentUrl']}")
            print_success(f"Expires In: {data['expiresIn']} seconds")
            print_success(f"Message: {data['message']}")
            
            print_section("Next Steps")
            print_info("To complete the payment, open this URL in a browser:")
            print(f"{Colors.BOLD}{data['paymentUrl']}{Colors.END}")
            
            return True
            
        else:
            print_error(f"Request failed with status code: {response.status_code}")
            
            try:
                error_data = response.json()
                print_section("Error Response")
                print(json.dumps(error_data, indent=2))
            except json.JSONDecodeError:
                print_error(f"Response: {response.text}")
            
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timed out after 30 seconds")
        print_warning("Check if the payment gateway is accessible")
        return False
        
    except requests.exceptions.ConnectionError:
        print_error("Failed to connect to the API")
        print_warning(f"Make sure the server is running at {base_url}")
        return False
        
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False


def test_server_health(base_url: str) -> bool:
    """
    Test if the server is running.
    
    Args:
        base_url: Base URL of the API
        
    Returns:
        bool: True if server is running, False otherwise
    """
    print_section("Testing Server Health")
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print_success(f"Server is running at {base_url}")
            return True
        else:
            print_warning(f"Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to server at {base_url}")
        print_info("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error checking server health: {str(e)}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test Payment Gateway Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--client-id",
        type=int,
        required=True,
        help="Client ID to test with"
    )
    
    parser.add_argument(
        "--credit-id",
        type=int,
        help="Optional credit ID to test with"
    )
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}Payment Gateway Integration Test{Colors.END}")
    print("=" * 40)
    
    # Test server health
    if not test_server_health(args.base_url):
        sys.exit(1)
    
    # Test payment initialization
    success = test_payment_initialization(
        args.base_url,
        args.client_id,
        args.credit_id
    )
    
    print_section("Test Result")
    if success:
        print_success("All tests passed! ✨")
        sys.exit(0)
    else:
        print_error("Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

