const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
// const ModuleFederationPlugin = require('webpack').container.ModuleFederationPlugin;
const { ModuleFederationPlugin } = require('webpack').container;


module.exports = {
  entry: "./src/index.jsx",
  // mode: 'development',
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.[contenthash].js",
    // publicPath: "/remote/",
    publicPath: '/remote/',
    clean: true,
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  devServer: {
    static: "./public",
    open: false, // auto open browser
    port: 3001,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "public/index.html", // ambil HTML kamu
    }),
    new ModuleFederationPlugin({
      name: 'remote',
      filename: 'remoteEntry.js',
      exposes: {
        './Remote': './src/components/Remote',
        './AboutRemote': './src/components/AboutRemote',
        './ProfileRemote': './src/components/ProfileRemote',
      },
      shared: {
        react: { singleton: true, eager: true, requiredVersion: "^19.1.0" },
        'react-dom': { singleton: true, eager: true, requiredVersion: "^19.1.0" },
      }
    }),
  ],
};

// const HtmlWebpackPlugin = require('html-webpack-plugin');
// const ModuleFederationPlugin = require('webpack').container.ModuleFederationPlugin;
// const path = require('path');

// module.exports = {
//   entry: './src/index.js',
//   mode: 'development',
//   devServer: {
//     port: 3001,
//   },
//   output: {
//     publicPath: 'auto',
//   },
//   module: {
//     rules: [
//       {
//         test: /\.jsx?$/,
//         loader: 'babel-loader',
//         exclude: /node_modules/,
//       },
//       {
//         test: /\.css$/,
//         use: ['style-loader', 'css-loader', 'postcss-loader'],
//       },
//     ],
//   },
//   plugins: [
//     new ModuleFederationPlugin({
//       name: 'header',
//       filename: 'remoteEntry.js',
//       exposes: {
//         './Header': './src/components/Header',
//       },
//       shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
//     }),
//     new HtmlWebpackPlugin({
//       template: './public/index.html',
//     }),
//   ],
//   resolve: {
//     extensions: ['.js', '.jsx'],
//   },
// };
