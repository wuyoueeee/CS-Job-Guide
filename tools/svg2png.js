// 把 SVG 栅格化成 PNG，用于肉眼验收图表与示意图。
// 依赖 node workspace 里已安装的 sharp。
// 用法：node tools/svg2png.js input.svg output.png [width]
const path = require("path");
const fs = require("fs");
const sharp = require("sharp");

const [input, output, widthArg] = process.argv.slice(2);
if (!input || !output) {
  console.error("usage: node tools/svg2png.js <in.svg> <out.png> [width]");
  process.exit(1);
}
const width = Number(widthArg) || 1200;
fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
sharp(path.resolve(input), { density: 144 })
  .resize({ width })
  .png()
  .toFile(path.resolve(output))
  .then((info) => console.log(`${output} ${info.width}x${info.height}`))
  .catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
