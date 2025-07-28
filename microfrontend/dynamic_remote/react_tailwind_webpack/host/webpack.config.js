const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { ModuleFederationPlugin } = require('webpack').container;

module.exports = {
  entry: "./src/index.jsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.[contenthash].js",
    publicPath: "auto",
    clean: true,
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  devServer: {
    static: "./public",
    open: false, // auto open browser
    port: 3000,
    historyApiFallback: true,
    // proxy: {
    //   '/cookie/set-remote1': {
    //     target: 'http://localhost:8080', // URL backend
    //     changeOrigin: true,
    //     // pathRewrite: { '^/api': '' }, // jika perlu hapus `/api` prefix
    //   },
    //   '/cookie/set-remote2': {
    //     target: 'http://localhost:8080', // URL backend
    //     changeOrigin: true,
    //     // pathRewrite: { '^/api': '' }, // jika perlu hapus `/api` prefix
    //   },
    //   '/remoteEntry.js': {
    //     target: 'http://localhost:8080', // URL backend
    //     changeOrigin: true,
    //     // pathRewrite: { '^/api': '' }, // jika perlu hapus `/api` prefix
    //   },
    // },
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
      name: 'host',
      remotes: {
        // remote: 'remote@http://localhost:3001/remoteEntry.js',
      },
      shared: {
        react: { singleton: true, eager: true, requiredVersion: "^19.1.0" },
        'react-dom': { singleton: true, eager: true, requiredVersion: "^19.1.0" },
      },
    }),
  ],
};