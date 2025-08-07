# Google Tag Manager Configuration Guide for PhysioVisit

## GTM Container Setup

### Step 1: Create GTM Container
1. Go to [Google Tag Manager](https://tagmanager.google.com)
2. Create a new account for "PhysioVisit"
3. Create a container for "www.physiovisit.be" (Web)
4. Replace `GTM-PHYSIOVISIT` with your actual container ID in all HTML files

### Step 2: Install Container Code
The container code has already been added to all HTML files. You just need to replace the placeholder ID.

## Variables Setup

### Built-in Variables (Enable These)
- Page URL
- Page Hostname
- Page Path
- Page Title
- Referrer
- Event
- Click Element
- Click Text
- Click URL
- Form Element
- Form Classes
- Form ID

### Custom Variables

#### 1. GA4 Configuration Variable
```
Variable Type: Google Analytics Settings
Variable Name: GA4 - Configuration
Tracking ID: G-PHYSIOVISIT (replace with actual ID)
```

#### 2. Event Category Variable
```
Variable Type: Data Layer Variable
Variable Name: DLV - Event Category
Data Layer Variable Name: event_category
```

#### 3. Event Label Variable
```
Variable Type: Data Layer Variable
Variable Name: DLV - Event Label
Data Layer Variable Name: event_label
```

#### 4. Service Type Variable
```
Variable Type: Data Layer Variable
Variable Name: DLV - Service Type
Data Layer Variable Name: service_type
```

#### 5. Phone Number Variable
```
Variable Type: Data Layer Variable
Variable Name: DLV - Phone Number
Data Layer Variable Name: phone_number
```

## Triggers Setup

### 1. All Pages Trigger
```
Trigger Type: Page View
Trigger Name: All Pages
This trigger fires on: All Pages
```

### 2. Phone Click Trigger
```
Trigger Type: Custom Event
Trigger Name: Phone Call Click
Event Name: phone_call_click
This trigger fires on: All Custom Events
```

### 3. Email Click Trigger
```
Trigger Type: Custom Event
Trigger Name: Email Click
Event Name: email_click
This trigger fires on: All Custom Events
```

### 4. Form Submit Trigger
```
Trigger Type: Custom Event
Trigger Name: Form Submit
Event Name: form_submit
This trigger fires on: All Custom Events
```

### 5. Service Button Click Trigger
```
Trigger Type: Custom Event
Trigger Name: Service Button Click
Event Name: service_button_click
This trigger fires on: All Custom Events
```

### 6. Kinetec Rental Triggers
```
# Product View
Trigger Type: Custom Event
Event Name: view_item

# Begin Checkout
Trigger Type: Custom Event
Event Name: begin_checkout

# Purchase
Trigger Type: Custom Event
Event Name: purchase
```

## Tags Setup

### 1. GA4 Configuration Tag
```
Tag Type: Google Analytics: GA4 Configuration
Tag Name: GA4 - Configuration
Measurement ID: G-PHYSIOVISIT (replace with actual)
Triggering: All Pages
```

### 2. GA4 Event Tags

#### Phone Call Event
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Phone Call Click
Configuration Tag: {{GA4 - Configuration}}
Event Name: phone_call_click
Custom Parameters:
  - event_category: {{DLV - Event Category}}
  - event_label: {{DLV - Event Label}}
  - phone_number: {{DLV - Phone Number}}
Triggering: Phone Call Click
```

#### Email Click Event
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Email Click
Configuration Tag: {{GA4 - Configuration}}
Event Name: email_click
Custom Parameters:
  - event_category: {{DLV - Event Category}}
  - event_label: {{DLV - Event Label}}
Triggering: Email Click
```

#### Form Submit Event
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Form Submit
Configuration Tag: {{GA4 - Configuration}}
Event Name: form_submit
Custom Parameters:
  - event_category: lead_generation
  - event_label: {{DLV - Event Label}}
  - form_name: {{DLV - Event Label}}
Triggering: Form Submit
```

#### Service Interest Event
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Service Button Click
Configuration Tag: {{GA4 - Configuration}}
Event Name: service_button_click
Custom Parameters:
  - event_category: services
  - event_label: {{DLV - Service Type}}
  - service_type: {{DLV - Service Type}}
Triggering: Service Button Click
```

### 3. E-commerce Tags for Kinetec Rental

#### View Item Event
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Kinetec View Item
Configuration Tag: {{GA4 - Configuration}}
Event Name: view_item
Send an e-commerce event: true
Items:
  - item_id: KINETEC-CPM-001
  - item_name: Kinetec CPM Machine Verhuur
  - item_category: Medical Equipment Rental
  - price: 17
  - quantity: 1
  - currency: EUR
Triggering: Kinetec Page View
```

#### Purchase Event (Rental Request)
```
Tag Type: Google Analytics: GA4 Event
Tag Name: GA4 - Kinetec Purchase
Configuration Tag: {{GA4 - Configuration}}
Event Name: purchase
Send an e-commerce event: true
Transaction ID: {{Transaction ID}}
Value: 17
Currency: EUR
Items: [same as above]
Triggering: Kinetec Form Submit
```

### 4. Facebook Pixel Tags

#### Facebook Pixel Base Code
```
Tag Type: Custom HTML
Tag Name: Facebook Pixel - Base Code
HTML: 
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');
Triggering: All Pages
```

#### Facebook Pixel Lead Events
```
Tag Type: Custom HTML
Tag Name: Facebook Pixel - Lead
HTML:
fbq('track', 'Lead', {
  content_category: 'Form Submission',
  content_name: '{{Event Label}}',
  value: 1
});
Triggering: Form Submit, Phone Click, Email Click
```

## Testing & Debug

### Preview Mode Testing
1. Click "Preview" in GTM
2. Enter your website URL
3. Navigate through pages and test interactions
4. Verify tags fire correctly in the Tag Assistant panel

### Debug Checklist
- [ ] GA4 Configuration tag fires on all pages
- [ ] Phone click events tracked
- [ ] Email click events tracked
- [ ] Form submissions tracked
- [ ] Service button clicks tracked
- [ ] Kinetec rental events tracked
- [ ] Facebook Pixel events fire

### Variables to Test
- [ ] Event categories populate correctly
- [ ] Event labels contain meaningful data
- [ ] Service types are captured
- [ ] Phone numbers are tracked
- [ ] Form names are identified

## Conversion Setup

### GA4 Conversions
Mark these events as conversions in GA4:
1. form_submit
2. phone_call_click
3. purchase (Kinetec rentals)
4. generate_lead

### Facebook Conversions
Set up Custom Conversions for:
1. Lead - Form submissions
2. Lead - Phone clicks
3. Purchase - Rental requests

## Advanced Tracking

### Enhanced E-commerce Setup
For detailed e-commerce tracking, ensure these parameters are included:
- transaction_id
- value
- currency
- items array with detailed product information

### Custom Dimensions (GA4)
Consider setting up custom dimensions for:
- Service Type
- Location/City
- Contact Method Preference
- Device Category

## Maintenance

### Regular Tasks
- Monthly: Review conversion rates
- Quarterly: Update event parameters if needed
- Annually: Review and optimize tracking setup

### When to Update GTM
- New pages added
- New services launched
- Contact information changes
- New conversion points identified

---

**Last Updated**: January 2025  
**Version**: 1.0