const path = require("path");
const glob = require('glob');

// Credits: https://hackernoon.com/webpack-creating-dynamically-named-outputs-for-wildcarded-entry-files-9241f596b065
const entryArray = glob.sync('./src/**/index.ts');

const entryObject = entryArray.reduce((acc, item) => {
    let name = path.dirname(item.replace('./src/', ''))
    acc[name] = item
    return acc;
}, {});

module.exports = {
  entry: entryObject,
  devtool: 'source-map',
    target: "node",
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: [
                    'ts-loader',
                    {
                        loader: 'webpack-preprocessor-loader',
                        options: {
                            debug: process.env.NODE_ENV !== 'production',
                            params: {
                                ENV: process.env.NODE_ENV,
                                mock: !!process.env.USE_MOCK,
                            },
                            verbose: false,
                        }
                    }
                ],
                exclude: /node_modules/
            },
        ]
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js']
    },
    // Output directive will generate dist/<function-name>/index.js
    output: {
        filename: '[name]/index.js',
        path: path.resolve(__dirname, 'dist'),
        devtoolModuleFilenameTemplate: '[absolute-resource-path]',
        // credits to Rich Buggy!!!
        libraryTarget: 'commonjs2'
    }
};