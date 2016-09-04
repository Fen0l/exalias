# ExAlias

A simple awesome alias manager for exchange accounts.

Built with :
* [Python2.7][python2_7]
* [Tornado][tornado]
* [Python-OVH][python_ovh]

You can check a quick sample:

![](http://i.imgur.com/iFUMoyC.gif)

## Features

This app comes some features:
* Exchange 2013, 2016 OVH

## Installation

To be able to use it, you have to create an Application API. You can check a ticket on my website [First step with the OVH API][ovh_api_blog].
To prevent a maximum against hackers, you will provide a restricted access. Just enough for the app.

```
curl -XPOST -H"X-Ovh-Application: ÀPP_KEY" -H "Content-type: application/json" \
 https://eu.api.ovh.com/1.0/auth/credential  -d '{
     "accessRules": [
         {
             "method": "GET",
             "path": "/email/exchange*"
         },
         {
             "method": "POST",
             "path": "/email/exchange/*/service/*/account/*/alias*"
         },
         {
            "method": "DELETE",
             "path": "/email/exchange/*/service/*/account/*/alias*"
         }
     ],
     "redirection":"https://anthonypradal.com/"
}'
```

## Todo

* Be able to manage MX OVH Plan
* Multi-Exchange account
* Add other Exchange providers


## Contributing

Want to help make this theme even better? Contributions from the community are welcome!

Please follow these steps:

1. Fork/clone this repository.
2. Develop (and test!) your changes.
3. Open a pull request on GitHub. A description and/or screenshot of changes would be appreciated!

## License

MIT. See [LICENSE.MD](https://github.com/fen0l/exalias/blob/master/LICENSE.md).

[python2_7]: https://www.python.org/download/releases/2.7/
[tornado]: http://www.tornadoweb.org/en/stable/
[python_ovh]: https://github.com/ovh/python-ovh
[ovh_api_blog]: http://anthony.ovh/api/2016/09/03/first-step-with-the-ovh-api.html




