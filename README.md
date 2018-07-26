# UPI Payment Service
## Workflow:
1. User go to UPI payment page and enter details like Remitter Mobile Number, Remitter Email, Payee VPA, Payee Name, Amount, Transaction Reference ID, Transaction Note.
2. On clicking submit button, a UPI link is generated along with it’s short url.
3. This short URL is sent as SMS to user mobile and his email.
4. When user browse this short URL in mobile, it will redirect to that UPI link and invokes the local PSP application (like BHIM or PhonePe), where the user can confirm the details, and complete the payment.

![UPI](https://github.com/atultherajput/UPI/blob/master/assets/upi-screenshot.png)
<img src="https://github.com/atultherajput/UPI/blob/master/assets/PSP-PhonePe.png" alt="PSP" width="75%" height="800">
