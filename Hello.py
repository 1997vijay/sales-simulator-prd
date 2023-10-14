# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import json
import requests
import re
import secrets
from datetime import datetime
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio

LOGGER = get_logger(__name__)

# set configuration
st.set_page_config(
    page_title="Sales Simulator",
    page_icon="💰",
    layout='wide'
)
def generate_invoice_number(length=20):
    # Define characters to use in the invoice number (you can customize this)
    characters = "0123456789ABCDEFGHIJKLMNOP"

    # Use secrets.choice() to randomly select characters
    invoice_number = ''.join(secrets.choice(characters) for _ in range(length))
    return invoice_number

def validate_base_url(base_url):
    # Define a regular expression pattern for a valid base URL
    pattern = r"https?://[A-Za-z0-9.-]+(?:\:[0-9]+)?(?:[/?].*)?"
    
    # Check if the provided base URL matches the pattern
    if re.match(pattern, base_url):
        return True
    else:
        return False
  
def send_to_api(data,url):
    try:
        base_url=url
        try:
            header={
                "Content-Type":"application/json"
            }
            response=requests.post(url=base_url,data=data,headers=header)
        except Exception as e:
                st.warning(f'{e}')
    except Exception as e:
        st.warning(f'{e}')

async def send_to_iot_hub(data,connectionString):
    try:
        # Create an instance of the IoT Hub Client class
        device_client = IoTHubDeviceClient.create_from_connection_string(connectionString)
        await device_client.connect()

        await device_client.send_message(data)
        print("Message sent to IoT Hub:", data)
    except Exception as e:
        print("Error:", str(e))
    finally:
        # Shutdown the client
        await device_client.shutdown()


def run():
    st.title("Sales Simulator")
    # markdown_text = """
    # :red[Note: ] The application uses the POST method to send data through the API. 
    # Please ensure that your API is configured to accept data in JSON object format.
    # """
    # st.info(markdown_text)

    # set api url
    api_url=''
    # api_url=st.text_input("Enter API url")
    api_url=st.text_input("Enter IOT HUB connection string")

    # if st.button('set API',type='primary'):
    #     if api_url!=None and api_url!='':
    #         if not validate_base_url(api_url):
    #             st.warning("Invalid API base URL. Please provide a valid URL.")
    #         else:
    #             api_url=api_url
    #             st.success(f"API {api_url} integrated successfully!")
    #     else:
    #         st.info(f"API can not be blanked!")
    if st.button('set IOT Hub',type='primary'):
        if api_url!=None and api_url!='':
            api_url=api_url
            st.success(f"API {api_url} integrated successfully!")
        else:
            st.info(f"API can not be blanked!")
        
# Contact Information
    col1, col2, col3 = st.columns(3)
    with col1:
        full_name = st.text_input("Full Name",value="John Doe")
    with col2:
        email = st.text_input("Email Address",value="john@example.com")
    with col3:
        phone = st.text_input("Phone Number",value="123-456-7890")

    # Billing Information
    st.subheader("Billing Information")
    col1, col2 = st.columns(2)
    with col1:
        billing_address = st.text_input("Billing Address",value='Sanfrancisco')
        billing_city = st.text_input("City",value='Sanfrancisco')
        payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal"])
    with col2:
        billing_state = st.text_input("State/Province",value='california')
        billing_zip = st.text_input("ZIP/Postal Code",value='143545')

    # Shipping Information
    st.subheader("Shipping Information")
    col1, col2 = st.columns(2)
    with col1:
        shipping_address = st.text_input("Shipping Address",value='Sanfrancisco')
        shipping_city = st.text_input("Shipping City",value='Sanfrancisco')
        shipping_method = st.selectbox("Shipping Method", ["Standard", "Express"])
    with col2:
        shipping_state = st.text_input("Shipping State/Province",value='California')
        shipping_zip = st.text_input("Shipping ZIP/Postal Code",value='143545')

    # Product/Service Details
    st.subheader("Product/Service Details")
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product/Service Name",value='Laptop')
        quantity = st.number_input("Quantity", value=1, min_value=1)
    with col2:
        price_per_unit = st.number_input("Price per Unit", value=300.00, step=0.01)
        total_price = quantity * price_per_unit

    # Order Summary
    st.subheader("Order Summary")
    st.write(f"Subtotal: ${total_price:.2f}")
    col1, col2 = st.columns(2)
    with col1:
        tax = st.number_input("Tax", value=50.00, step=0.01)
    with col2:
        shipping_fee = st.number_input("Shipping Fee", value=100.00, step=0.01)
    total_amount = total_price + tax + shipping_fee
    st.write(f"Total Amount: ${total_amount:.2f}")

    # Promo Codes or Discounts
    st.subheader("Promo Codes or Discounts")
    promo_code = st.text_input("Promo Code",value='FGG560')

    # Submit Button
    if st.button("Place Order",type='primary'):
        # You can add further processing logic here
        order_data = {
                    "Contact Information": {
                        "Full Name": full_name,
                        "Email Address": email,
                        "Phone Number": phone,
                    },
                    "Billing Information": {
                        "Billing Address": billing_address,
                        "City": billing_city,
                        "State/Province": billing_state,
                        "ZIP/Postal Code": billing_zip,
                        "Payment Method": payment_method,
                    },
                    "Shipping Information": {
                        "Shipping Address": shipping_address,
                        "City": shipping_city,
                        "State/Province": shipping_state,
                        "ZIP/Postal Code": shipping_zip,
                        "Shipping Method": shipping_method,
                    },
                    "Product/Service Details": {
                        "Product/Service Name": product_name,
                        "Quantity": quantity,
                        "Price per Unit": price_per_unit,
                        "Total Price": total_price,
                    },
                    "Order Summary": {
                        "Tax": tax,
                        "Shipping Fee": shipping_fee,
                        "Total Amount": total_amount,
                    },
                    "Promo Codes or Discounts": {
                        "Promo Code": promo_code,
                    },
                    "Invoice Details": {
                        "Invoice Number":generate_invoice_number(length=20),
                        "Invoice Date":str(datetime.now())
                    }
                }

        # Display as JSON in console
        json_data = json.dumps(order_data, indent=4)

        # call rest api
        try:
            # send_to_api(data=json_data,url=api_url)
            asyncio.run(send_to_iot_hub(data=json_data,connectionString=api_url))
            st.success("Order placed successfully!")
        except Exception as e:
            st.warning(f'Something went wrong!!,{e}')
if __name__ == "__main__":
    run()
