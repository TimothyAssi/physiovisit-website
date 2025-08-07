# PhysioVisit.be - Complete Tracking & Schema Implementation Guide

## Overview
This document provides a comprehensive guide for implementing tracking and schema markup across the PhysioVisit.be website. The implementation includes Google Analytics 4, Google Tag Manager, Facebook Pixel, structured data schemas, and Google Search Console integration.

## 🎯 Tracking Components Implemented

### 1. Google Analytics 4 (GA4)
**Implementation Location**: All HTML pages in `<head>` section
**GA4 ID**: `G-NY8Q6GZEVY` (your actual GA4 measurement ID)

#### Events Tracked:
- **Page Views**: Enhanced page view tracking with metadata
- **Phone Calls**: `phone_call_click` event when tel: links clicked  
- **Email Clicks**: `email_click` event when mailto: links clicked
- **Service Interactions**: `service_button_click` for service CTAs
- **Form Submissions**: `form_submit` with lead generation tracking
- **Scroll Depth**: 25%, 50%, 75%, 100% scroll milestones
- **Time on Page**: 30s, 1min, 2min, 5min engagement milestones
- **External Links**: `external_link_click` for outbound traffic
- **Google Reviews**: `google_reviews_click` for review interactions
- **FAQ Interactions**: `faq_interaction` for accordion clicks

#### E-commerce Events (Kinetec Rental):
- **view_item**: Product page views
- **begin_checkout**: When rental form is started
- **add_shipping_info**: Delivery service selection
- **purchase**: Rental form submissions
- **generate_lead**: Lead generation tracking

### 2. Google Tag Manager (GTM)
**Implementation Location**: All HTML pages
**GTM Container ID**: `GTM-WW27NH9Q` (your actual container ID)

#### GTM Setup Instructions:
1. **Create GTM Account**: Go to tagmanager.google.com
2. **Container ID**: Using `GTM-WW27NH9Q` (already configured)
3. **Configure Triggers**:
   - Page View Trigger
   - Form Submit Trigger
   - Click Triggers for buttons, links
   - Scroll Depth Triggers
   - Custom Event Triggers

#### Recommended GTM Tags:
```javascript
// GA4 Configuration Tag
Tag Type: Google Analytics: GA4 Configuration
Measurement ID: G-NY8Q6GZEVY
Trigger: All Pages

// GA4 Event Tags
Tag Type: Google Analytics: GA4 Event
Configuration Tag: {{GA4 Configuration}}
Event Name: {{Event Name Variable}}
Custom Parameters: {{Event Parameters}}
```

### 3. Facebook Pixel
**Implementation Location**: All HTML pages in `<head>` section  
**Pixel ID**: `FACEBOOK_PIXEL_ID` (replace with your actual pixel ID)

#### Events Tracked:
- **PageView**: Automatic page view tracking
- **Lead**: Phone clicks, email clicks, form submissions
- **ViewContent**: Service page views, product views
- **InitiateCheckout**: Rental form interactions
- **AddToCart**: Rental CTA clicks
- **Purchase**: Completed rental requests

### 4. Structured Data Schemas

#### Homepage (index.html):
- **LocalBusiness**: Complete business information
- **WebSite**: Website metadata with search action
- **Organization**: Company structure and contact points

#### Service Pages (kinesitherapie.html):
- **MedicalBusiness**: Healthcare service provider
- **Service**: Individual service offerings (Orthopedie, Neurologie, Gangrevalidatie)
- **FAQPage**: Frequently asked questions

#### Product Pages (kinetec-huren.html):
- **Product**: Kinetec rental equipment
- **Service**: Delivery and installation service
- **FAQPage**: Rental-specific FAQs

#### Contact Page (contact.html):
- **ContactPage**: Contact form and information
- **FAQPage**: Contact-related questions

## 🔧 Implementation Steps

### Step 1: Replace Placeholder IDs
Update the following placeholders with your actual IDs:

```html
<!-- Replace these IDs -->
GTM-WW27NH9Q ✅ (Updated)
G-NY8Q6GZEVY ✅ (Updated)  
FACEBOOK_PIXEL_ID → Your actual Facebook Pixel ID
YOUR_GOOGLE_SEARCH_CONSOLE_CODE → Your GSC verification code
```

### Step 2: Google Analytics 4 Setup
1. **Create GA4 Property**: In Google Analytics, create new GA4 property
2. **Get Measurement ID**: Copy your GA4 measurement ID (G-XXXXXXXXXX)
3. **Code Updated**: Already configured with `G-NY8Q6GZEVY`
4. **Configure Goals**: Set up conversion goals in GA4 interface

#### Recommended GA4 Conversions:
- Phone Call Clicks
- Form Submissions (Lead)
- Rental Requests (Purchase)
- Email Clicks

### Step 3: Google Tag Manager Configuration
1. **Create GTM Account**: Set up container at tagmanager.google.com
2. **Container Code**: Already installed with `GTM-WW27NH9Q`
3. **Import Configuration**: Use provided trigger and tag configurations

#### GTM Variables to Create:
```javascript
// Event Variables
Event Name: {{Event}}
Event Category: {{Event Category}}
Event Label: {{Event Label}}

// Page Variables  
Page Title: {{Page Title}}
Page URL: {{Page URL}}

// Form Variables
Form ID: {{Form ID}}
Form Classes: {{Form Classes}}
```

### Step 4: Facebook Pixel Setup  
1. **Create Facebook Pixel**: In Facebook Business Manager
2. **Get Pixel ID**: Copy your pixel ID
3. **Replace in Code**: Update `FACEBOOK_PIXEL_ID` with actual ID
4. **Configure Conversions**: Set up conversion tracking in Facebook Ads Manager

### Step 5: Google Search Console
1. **Add Property**: Add physiovisit.be to Google Search Console
2. **Verify Ownership**: Use HTML tag method
3. **Replace Verification Code**: Update `YOUR_GOOGLE_SEARCH_CONSOLE_CODE`
4. **Submit Sitemap**: Submit `/sitemap.xml` to GSC

## 📊 Verification & Testing

### GA4 Testing:
1. **Real-time Reports**: Check real-time events in GA4
2. **Debug Mode**: Use GA4 debug mode for testing
3. **Event Parameters**: Verify custom parameters are captured

### GTM Testing:
1. **Preview Mode**: Use GTM preview mode for testing
2. **Tag Assistant**: Install Google Tag Assistant extension
3. **Event Verification**: Check events fire correctly in preview

### Facebook Pixel Testing:
1. **Facebook Pixel Helper**: Install browser extension
2. **Test Events**: Verify events fire in Pixel Helper
3. **Conversion Tracking**: Test conversion events

### Schema Testing:
1. **Google Rich Results Test**: Test structured data
2. **Schema Markup Validator**: Validate schema syntax
3. **Google Search Console**: Monitor rich results status

## 🚀 Advanced Tracking Features

### Enhanced E-commerce (Kinetec Rentals):
```javascript
// Product View Tracking
gtag('event', 'view_item', {
  currency: 'EUR',
  value: 17,
  items: [{
    item_id: 'KINETEC-CPM-001',
    item_name: 'Kinetec CPM Machine Verhuur',
    item_category: 'Medical Equipment Rental',
    price: 17,
    quantity: 1
  }]
});

// Purchase Tracking (Rental Request)
gtag('event', 'purchase', {
  transaction_id: 'RENTAL-' + Date.now(),
  currency: 'EUR', 
  value: 17,
  items: [/* item details */]
});
```

### Custom Events:
```javascript
// Emergency Service Tracking
function trackEmergencyService() {
  gtag('event', 'emergency_service_request', {
    event_category: 'emergency',
    event_label: 'emergency_physiotherapy'
  });
}

// Location Interest Tracking  
gtag('event', 'location_interest', {
  event_category: 'location',
  location_name: 'Grimbergen',
  service_type: 'kinesitherapie'
});
```

## 📈 Reporting & Analysis

### Key Metrics to Monitor:
1. **Lead Generation**: Form submissions, phone clicks
2. **Service Interest**: Page views by service type
3. **Location Performance**: Interest by service area
4. **Rental Conversions**: Kinetec rental requests
5. **Engagement**: Scroll depth, time on page
6. **User Flow**: Page progression and drop-offs

### Custom Reports Setup:
1. **Lead Funnel**: Track path from landing to conversion
2. **Service Performance**: Compare service page effectiveness  
3. **Location Analysis**: Performance by service area
4. **Device Analysis**: Mobile vs desktop conversion rates

## 🛠️ Maintenance & Updates

### Regular Tasks:
1. **Monthly**: Review conversion rates and optimize
2. **Quarterly**: Update schema markup if services change
3. **Annually**: Review and refresh tracking implementation

### When to Update:
- New services added
- Contact information changes  
- Business hours modifications
- New locations added
- Policy changes

## 📞 Support & Troubleshooting

### Common Issues:
1. **Events Not Firing**: Check browser console for errors
2. **GTM Not Loading**: Verify container ID and implementation
3. **Schema Errors**: Use Google's structured data testing tool
4. **Facebook Pixel Issues**: Check pixel helper for diagnostics

### Debug Commands:
```javascript
// Check if GA4 is loaded
console.log(typeof gtag);

// Check if GTM is loaded
console.log(typeof dataLayer);

// Check if Facebook Pixel is loaded  
console.log(typeof fbq);
```

---

## 📋 Implementation Checklist

- [ ] Replace all placeholder IDs with actual account IDs
- [ ] Test GA4 events in real-time reports
- [ ] Configure GTM container with appropriate triggers/tags
- [ ] Set up Facebook Pixel conversion tracking
- [ ] Submit sitemap to Google Search Console
- [ ] Verify structured data with Google's testing tool
- [ ] Test form submissions end-to-end
- [ ] Monitor for any JavaScript errors
- [ ] Set up automated email alerts for tracking issues
- [ ] Document any custom modifications for future reference

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Contact**: info@physiovisit.be