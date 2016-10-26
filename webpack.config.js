module.exports = {
  entry: './entry.js',
  output: {
    path: __dirname,
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      { test: /\.css$/,
      loaders: [
        'style',
        'css?modules&camelCase&localIdentName=[name]_[local]',
        'sass',
      ],
    },
      { test: /\.js$/, loader: 'jsx' },
    ],
  },
};
