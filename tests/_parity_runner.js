/* Reads fixtures (JSON array) from stdin, computes each estimate with the SHIPPED
 * docs/engine.js + docs/data.js, and prints the ages as JSON. Used by test_parity.py. */
const path = require("path");
const root = path.resolve(__dirname, "..");
global.window = global;
require(path.join(root, "docs", "data.js"));           // sets global.ODONTOAGE_DATA
const OdontoAge = require(path.join(root, "docs", "engine.js"));
const DATA = global.ODONTOAGE_DATA;

let input = "";
process.stdin.on("data", (d) => (input += d));
process.stdin.on("end", () => {
  const fixtures = JSON.parse(input);
  const out = fixtures.map((f) => {
    try {
      return OdontoAge.estimate(DATA, f.method, f).estimatedAgeYears;
    } catch (err) {
      return { error: String((err && err.message) || err) };
    }
  });
  process.stdout.write(JSON.stringify(out));
});
