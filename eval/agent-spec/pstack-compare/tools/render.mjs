import { render } from "pele";
import fs from "node:fs";
const [renderMd, ...files] = process.argv.slice(2);
const css = fs.readFileSync(renderMd, "utf8").match(/```css\n([\s\S]*?)```/)[1];
for (const f of files) {
  try {
    const { svg } = render(fs.readFileSync(f, "utf8"), { limit: 1_000_000, outputLimit: 8_000_000, maxEdges: 10_000 });
    const out = svg.replace(/(<svg[^>]*>)/, `$1<style>${css}</style>`);
    fs.writeFileSync(f.replace(/\.mmd$/, ".svg"), out);
    console.log("wrote", f.replace(/\.mmd$/, ".svg"), out.length, "bytes");
  } catch (e) { console.log("PeleError", f, e.name, e.message); }
}
