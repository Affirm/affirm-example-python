## Quick Start

Add this snippet to your page:

```html
<script>
  var affirm=window.affirm||{};
  (function(c,e,a,d,b,l){var f,g=document.createElement(d),k=document.getElementsByTagName(d)[0],h=function(a,b,c){return function(){a[b]._.push([c,arguments])}};c[e]=h(c,e,"set");d=c[e];c[a]={};c[a]._=[];d._=[];affirm.ui[b]=h(c,a,b);a=0;for(b="set add save post open empty reset on off trigger ready".split(" ");
    a<b.length;a++)d[b[a]]=h(c,e,b[a]);a=0;for(b=["get","token","url","items"];a<b.length;a++)f=b[a],d[f]=function(){try{console.warn("affirm.checkout."+f+"() called before Affirm Checkout initialized")}catch(a){}};g.async=!0;g.src=l;k.parentNode.insertBefore(g,k)
  })(affirm,"checkout","ui","script","ready","https://sandbox.affirm.com/js/v2/affirm.js");
</script>
```

Setup and submit the checkout
```html
<script>

  // setup and configure options
  affirm.checkout({
    checkout_id:          "ABC-123456",
    merchant: {
      public_api_key:           "XXXXXXXXXXXXXXXXXXX",
      user_confirmation_url:    "http://example.com/confirm",
      user_cancel_url:          "http://example.com/cancel"
    },
    items: [
      {
        display_name:         "Awesome Pants",
        sku:                  "ABC-123", // must be unique
        unit_price:           1999,      // in cents
        item_image_url:       "http://example.com/images/awesome-pants.jpg",
        item_url:             "http://example.com/products/awesome-pants.html"
      }
    ]
  });

  // save and start the checkout
  affirm.checkout.open();

</script>
```


If you want to save the checkout, but not immediately open the checkout UI, you can use the `.save()` method

```javascript
affirm.checkout.save(function(response){

  // if the save was not successful, an `error` object will be set on the response
  if( response.error ){
    alert( "Error!" );

  // if successful, a `url` will be available for the saved checkout
  } else {
    console.log( response.url );
  }

});
```

### Set & Get Options

```javascript

// To set options on the checkout, you can use the top level `checkout({...})`
affirm.checkout({
  checkout_id:          "f2390jfds9a0jfds",
  shipping_amount:      1900,

  merchant: {
    public_api_key:           "23kjfds0f902jf39",
    user_confirmation_url:    "http://example.com/confirm",
    user_cancel_url:          "http://example.com/cancel"
  }
});

// You can also use the `.set({...})` method
affirm.checkout.set({
  billing: {
    email: "test@example.net",
    name:  "John Doe"
  }
});
```

Set a single field
```javascript
affirm.checkout.set("shipping_amount", 1299);

affirm.checkout.set("shipping.phone", "1 (989) 555-5555");
affirm.checkout.set("shipping.phone.first", "John");

affirm.checkout.set("merchant", {
  public_api_key:           "XXXXXXXXXXXXXXXXXXX",
  user_confirmation_url:    "http://example.com/confirm",
  user_cancel_url:          "http://example.com/cancel"
})
```


Get a field
```javascript
// You should wrap any .get() calls in .ready() to ensure affirm.checkout has loaded
affirm.checkout.ready(function(){

  affirm.checkout.get("shipping_amount"); // 1299

  affirm.checkout.get("shipping.phone");         // "1 (989) 555-5555"
  affirm.checkout.get("shipping.name.first");    // "John"

  affirm.checkout.get("merchant");
  // {
  //   public_api_key:           "XXXXXXXXXXXXXXXXXXX",
  //   user_confirmation_url:    "http://example.com/confirm",
  //   user_cancel_url:          "http://example.com/cancel"
  // }

});
```

You can reset all options with `.reset()`
```javascript
// reset all config options and remove all items
affirm.checkout.reset()
```


### Adding Items to the checkout

You can add items to the checkout a few different ways:
```javascript
// Add a single item
affirm.checkout.add({
  display_name:         "Awesomest Product",
  sku:                  "f2390j",
  unit_price:           1999,
  qty:                  2, // optional, default is 1
  item_image_url:       "http://example.com/product.jpg",
  item_url:             "http://example.com/product.html"
});
```

```javascript
// add multiple items as arguments
affirm.checkout.add({
  display_name:         "Awesome Pants",
  sku:                  "ABC-123",
  unit_price:           1999,
  item_image_url:       "http://example.com/images/awesome-pants.jpg",
  item_url:             "http://example.com/products/awesome-pants.html"
},{
  display_name:         "Blue Shirt",
  sku:                  "DEF-456",
  unit_price:           1999,
  qty:                  3,
  item_image_url:       "http://example.com/images/blue-shirt.jpg",
  item_url:             "http://example.com/products/blue-shirt.html"
},{
  display_name:         "Green Shoes",
  sku:                  "GHI-789",
  unit_price:           2345,
  item_image_url:       "http://example.com/images/green-shoes.jpg",
  item_url:             "http://example.com/products/green-shoes.html"
});


// add multiple items with an array
var my_items = [{
  display_name:         "Awesome Pants",
  sku:                  "ABC-123",
  unit_price:           1999,
  item_image_url:       "http://example.com/images/awesome-pants.jpg",
  item_url:             "http://example.com/products/awesome-pants.html"
},{
  display_name:         "Blue Shirt",
  sku:                  "DEF-456",
  unit_price:           1999,
  item_image_url:       "http://example.com/images/blue-shirt.jpg",
  item_url:             "http://example.com/products/blue-shirt.html"
}];


affirm.checkout.add(my_items);


// You can also add items when setting options
affirm.checkout({
  items: [{
    display_name:         "Awesome Pants",
    sku:                  "ABC-123",
    unit_price:           1999,
    item_image_url:       "http://example.com/images/awesome-pants.jpg",
    item_url:             "http://example.com/products/awesome-pants.html"
  },{
    display_name:         "Blue Shirt",
    sku:                  "DEF-456",
    unit_price:           1999,
    item_image_url:       "http://example.com/images/blue-shirt.jpg",
    item_url:             "http://example.com/products/blue-shirt.html"
  }]
});
```

To read the items, you can use `.items()`
```javascript
// You should wrap this call in a .ready() to ensure affirm.checkout has loaded
affirm.checkout.ready(function(){

  // returns an array of all items added to the cart
  affirm.checkout.items();

});
```

You can clear the items in the checkout with the `.empty()` method
```javascript
affirm.checkout.empty();
```

### Saving & Initiating the Checkout
Calling `.open()` will save the checkout and immediately open the checkout flow.  If you have already called `.save()` and it was successful, it will open the most recently saved checkout.

```javascript
// opens the checkout modal on desktop, forwards to the checkout on mobile
affirm.checkout.open()
```

Save the checkout:
```javascript
// save the checkout and get the url
affirm.checkout.save(function(response){

  if(response.error){
    // handle error case
  } else {

    // if successfully saved, the response will have a `url` for the checkout
    response.url;
  }
});

// once it has been saved, you can access the url
affirm.checkout.url()
```

If you want to POST the checkout directly to Affirm, you can use `.post()`.  This is similar to `.open()`, but will always
save a new version and the checkout flow will be on the affirm.com domain instead of your website.
```javascript
// post checkout directly (and redirect to affirm.com)
affirm.checkout.post()
```


### Checkout API Settings Reference

```javascript
affirm.checkout({

  // Optional identifier for the checkout, used for tracking by the merchant
  checkout_id:          "ABC-123456789",

  // Total tax cost for the checkout (cents)
  tax_amount:           987,

  // Any extra fees applied to the checkout (cents)
  misc_fee_amount:      298,

  // Total shipping amount for the checkout (cents)
  shipping_amount:      1900,

  // States that cannot be shipped to for any item.
  // Format should be "state=xx,xx,xx..."
  shipping_exclusions:  "state=FL,CN",

  // Currency for the checkout, only USD is currently allowed
  currency:             "USD",

  // Merchant settings / configuration
  merchant: {

    // Required
    public_api_key:           "23kjfds0f902jf39",

    // Required. Url that the user is sent to after a successful checkout
    // with a charge_id or charge_token set as a parameter
    user_confirmation_url:    "http://example.com/confirm",

    // Required. Url that the user is redirected to if they cancel the checkout
    // *note: if the user is on desktop and is in the affirm checkout widget on
    // your site, the widget will simply close when the user cancels and they
    // will not be redirected.  This is only used if the user is checking out
    // on the affirm.com domain
    user_cancel_url:          "http://example.com/cancel",

    // Url that the user will be redirected to after being declined during the checkout
    charge_declined_url:      "http://example.com/declined"

    // This url we receive a POST with all of the details of the checkout
    // before the user is allowed to complete the checkout.  You can verify and/or
    // modify the checkout information if required.
    checkout_amendment_url:   "http://example.com/amend"
  },

  // configuration options for the checkout
  config: {

    // If any shipping fields are required for the order and are not provided
    // by you, they will be asked for during the checkout flow. All possible
    // values are below
    required_shipping_fields:     ["name","address","phone_number", "email"],

    // If any billing fields are required for the order and are not provided
    // by you, they will be asked for during the checkout flow.  Affirm
    // already requires 'phone_number', 'dob', 'name', and 'email'.  All
    // possible values are listed below.
    required_billing_fields:      ["name","phone_number","email", "dob", "ssn_last4"],

    // Action that will be used when the user is sent to the user_confirmation_url.
    // Possible values are 'GET' and 'POST'. Default is 'POST'
    user_confirmation_url_action: "POST"
  },

  // User's shipping address for the checkout
  shipping: {

    email: "test@example.net",
    phone: "+989 555-5555",

    // Name can be either be a string or a hash
    name: 'John Doe',

    // If it is a hash, it must either contain 'full' or 'first' and 'last'
    name: {
      // optional
      prefix: "Mr.",

      // required if 'full' is not provided
      first:  "John",

      // optional
      middle: "Joe",

      // required if 'full' is not provided
      last:   "Doe"

      // optional
      suffix: "Jr.",

      // required if 'first' and 'last' are not provided
      full: "Mr. John Joe Doe Jr."
    },

    // Shipping address
    address: {

      // required
      line1:        "12345 Main",

      // optional
      line2:        "#1",

      // required
      city:         "San Francisco",
      state:        "CA",
      country:      "US",
      zipcode:      "94122"
    }
  },

  // Billing information for the user to applied to the user's Affirm account
  billing: {
    email: "test@example.net",

    // Name can be either be a string or a hash
    name: 'John Doe',

    // If it is a hash, it must either contain 'full' or 'first' and 'last'
    name: {
      // optional
      prefix: "Mr.",

      // required if 'full' is not provided
      first:  "John",

      // optional
      middle: "Joe",

      // required if 'full' is not provided
      last:   "Doe"

      // optional
      suffix: "Jr.",

      // required if 'first' and 'last' are not provided
      full: "Mr. John Joe Doe Jr."
    },

    // Billing address
    address: {

      // required
      line1:        "12345 Main",

      // optional
      line2:        "#1",

      // required
      city:         "San Francisco",
      state:        "CA",
      country:      "US",
      zipcode:      "94122"
    }
  },


  // You can add items with the .set method by providing an array
  items: [
    {
      // Required. Name for the product displayed to the user
      display_name:         "Awesome Product",

      // Required. Cost of the item, per unit (cents)
      unit_price:           1999,

      // Required. Unique identifier for the item
      sku:                  "f2390j",

      // Required. Image used to display the product during the checkout flow
      item_image_url:       "http://example.com/product.jpg",

      // Required. Url to view the item
      item_url:             "http://example.com/product.html",

      // Item Quantity, default is 1 (integer)
      qty:                  1,

      // Date when the item will be shipping (ISO 8601)
      shipping_date:        "2014-11-30",

      // Expected delivery date for the item (ISO 8601)
      delivery_date:        "2015-01-15"
    }
  ]
});
```




## UI Elements

Affirm.js has several UI elements that it uses for the checkout flow.  You can access these to use for your integration via `affirm.ui`.

When working with any affirm ui elements, you will want to wrap it in the `.ready()` method in order to make sure that the affirm.ui has loaded and initialized on the page.
```javascript
  affirm.ui.ready(function(){
    ...
  });
```

### affirm.ui.button

If you have an element on your page with an id of `affirm_button`, affirm.js will append a checkout button to the element.  When clicked, it will save and open the current checkout.

You can listen for the click event on the button:
```javascript
affirm.ui.ready(function(){
  affirm.ui.button.on('click',function(){

    // You can modify checkout fields here before it is opened
    affirm.checkout.set('shipping_amount', 3400);
  };
});
```

### affirm.ui.error

Affirm.js has a modal that it uses to display any errors.  You can use it to display errors as well:
```javascript
var my_error_screen = affirm.ui.error({
  title: "Your billing information is incorrect"
  body: "Please check that your information provided is complete and correct before submitting again"
});

// close the error screen
my_error_screen.close();
```

### affirm.ui.checkout
This is the checkout modal used on desktop. You can create a new checkout modal by passing in a `url` you received from calling `affirm.checkout.save()`:

```javascript
affirm.checkout.save(function(response){

  var my_new_checkout = affirm.ui.checkout(response.url);

});
```

### affirm.ui.learn_more

Affirm.js has an informational screen about how Affirm Checkout works, used by the `affirm.ui.button` widget.  You can open and close this screen at any time.
```javascript
affirm.ui.learn_more.open();
affirm.ui.leann_more.close();

```


