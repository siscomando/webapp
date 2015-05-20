# &lt;star-rating&gt;

Web Component for generate a star rating using Polymer.

## Demo

> [Check it live](http://manoelneto.github.io/star-rating/).

## Usage

1. Import Web Components' polyfill:

    ```xml
    <script src="//cdnjs.cloudflare.com/ajax/libs/polymer/0.0.20130816/polymer.min.js"></script>
    ```

2. Import Custom Element:

    ```xml
    <link rel="import" href="src/star-rating.html">
    ```

3. Start using it!

    ```xml
    <star-rating></star-rating>
    ```

## Options

Attribute     | Options             | Default        | Description
---           | ---                 | ---            | ---
`votes`      | *number* | 0 | The votes count
`votesSum` | *number* | 0 | The votes sum 
`starCount`        | *number* | 5 | The number of star to display
`readyOnly`        | true, false | false | Make the stars not interactable

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

Check [Release](https://github.com/manoelneto/star-rating/releases/) list.

## License

[MIT License](http://mit-license.org/) © Manoel Quirino