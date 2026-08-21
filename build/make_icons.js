// Generates native Windows (.ico) and macOS (.icns) icons from build/icon.png.
// png2icons is pure JS and runs on any platform.
const png2icons = require('png2icons');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const inputPath = path.join(root, 'icon.png');
const input = fs.readFileSync(inputPath);

const ico = png2icons.createICO(input, png2icons.BICUBIC, 0);
const icns = png2icons.createICNS(input, png2icons.BICUBIC, 0);

fs.writeFileSync(path.join(root, 'icon.ico'), ico);
fs.writeFileSync(path.join(root, 'icon.icns'), icns);

console.log('icon.ico', ico.length, 'bytes');
console.log('icon.icns', icns.length, 'bytes');
