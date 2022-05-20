# Search UI

## Tech stack

* TypeScript
* React
* Styled components (component specific css)
* Overmind (state management)

## How to create the bundle

The `full-bundle.js` file, which is emdedded to the hosting website, can be created with the following instructions.

First, install the module dependencies and the make the application build:

```
yarn install
yarn build
```

The build process will generate a set of javascript files into the `./build/static/js/` directory. Note that the filename hash (e.g. b7ecdeb5) will be different on every changed build.

```
2.b7ecdeb5.chunk.js
2.b7ecdeb5.chunk.js.LICENSE.txt
main.3246510d.chunk.js
runtime-main.4ef503da.js
```

You can catenate the javascript files into a single file, e.g.:

```
cat 2.b7ecdeb5.chunk.js main*.js runtime*.js > full-bundle.js
```

You can then upload the created `full-bundle.js` file into your website codebase or hosting environment.

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.
