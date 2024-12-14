[![image](/images/howtounloadhtmxhistory.png)](https://youtu.be/Tc64QmkXpqo)

# Seamlessly unload/remove htmx cache history

A web page serves for internet public access and authenticated users, often time offer some type of browser cache to improve user experience.  

Modern browser support varies type of [HTTP Web API][4] caching machinesm to effectively improve load performance. It reduces unnecessary network requests by storing copies of pages, images, and other media content on your device. The browser uses these copies to load content faster the next time you visit those sites. 

htmx provides couple of mechanism for interacting with [browser history API][1] like hx-push-url attribute allows browser navigation bar and magically add the current state of the page visits into the browser's history.  

For instance, When a user clicks on a URL link, htmx will try took snapshot the current DOM and cache it before it makes a request to respective destination. 

Another instance were, authenticated web pages that when the user signs out takes the user back to the sign in page, 
but when user click the back button after logout, the page just loads from without sending a request to the server, 
thus, the user could still navigate to the home page without being authenticated.

### Enable htmx History Snapshots with [hx-boost][6] or [hx-push-url][5]

```html
<a href="/articles/565678" hx-boost="true">article 565678</a>
```

```html
<a hx-get="/articles/565680" hx-push-url="true" hx-target="#mquote">quote</a>
```

![image](/images/htmx-cache-local-storage.png)

On otherway around, When a user hits the back button, htmx will retrieve the old content from cache and swap it back into the DOM target, simulating “going back” to the previous state. 
If the url location is not found in the cache, htmx will make an ajax request to the given URL, with the header "HX-History-Restore-Request" set to true, and expects back the HTML needed for the entire page. 

![image](/images/restore-request-header.png)

more information about how htmx history work can refer [htmx site][2]

### Disabling htmx History Snapshots

[htmx History][3] snapshotting can be disabled for a URL by setting the hx-history attribute to false on any element in the current document, or any html fragment loaded into the current document by htmx. This can be used to prevent sensitive data entering the localStorage cache, which can be important for shared-use / public computers. History navigation will work as expected, but on restoration the URL will be requested from the server instead of the local history cache.

You may use the hx-history="false" attribute somewhere in your page when the user is logged in - that will prevent it being cached for history restores. 

```html
<body hx-history="false">
```

Note:
after adding the htmx hx-history attribute, you will need to manually delete your htmx localStorage cache, in order to erase any previously htmx-history-cache cached pages. 

To facilitate cache deletion while user log-off, js script will be fire upon clicking logout button. more information can refer to [local storage remove item][7].

```java
    <script>
        function CacheDeleteItemHTMX() {
        window.localStorage.removeItem("htmx-history-cache");
      }
    </script>
```
### See removal function in action
![image](/images/log-off.gif)

## Tools comes with web app:

-  sqlalchemy record removal tool

```python
db_rec_removal.py

HowTO:
        python .\db_rec_removal.py -l <local_filename> -v all           // view all username records
        python .\db_rec_removal.py -l <local_filename> -s <username>    // show matched username record; if no matched record return None
        python .\db_rec_removal.py -l <local_filename> -d <username>    // delete matched username record
```

```python
(.venv) instance>python .\db_rec_removal.py -l .\site.db -v all
[('batman',), ('spiderman',), ('superman',)]

(.venv) instance>python .\db_rec_removal.py -l .\site.db -d batman
succesfully deleted batman
```

> simple SQL tool allow to display all existing DB username table records, check if specific username exist, and perform deletion action.


## Final thoughts:

By applying these 3 htmx attributes allow to take adventage of htmx-hisroty-cache feature enhance your web app user experience.
Furthermore, having a option to unload/remove htmx caching feature while user logout or back button.


## Install & run web app

```python
git clone https://github.com/scheehan/disable_and_enable_htmx_history_cache.git
```

```python
cd http_auth_error_handling_with_htmx

pip install -r requirements.txt
```
```python
flask run --debug
```

[1]: https://developer.mozilla.org/en-US/docs/Web/API/History_API
[2]: https://htmx.org/docs/#history
[3]: https://htmx.org/docs/#disabling-history-snapshots
[4]: https://developer.mozilla.org/en-US/docs/Web/API/Cache
[5]: https://htmx.org/attributes/hx-push-url/
[6]: https://htmx.org/attributes/hx-boost/
[7]: https://developer.mozilla.org/en-US/docs/Web/API/Storage/removeItem