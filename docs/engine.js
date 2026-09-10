/* OdontoAge browser engine — mirrors the Python package exactly (same data, same
 * formulae) so results are identical. Pure logic, no DOM. Works in the browser
 * (window.OdontoAge) and in Node (module.exports) for parity testing. */
(function (root, factory) {
  var api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.OdontoAge = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  var TEETH = ["I1", "I2", "C", "PM1", "PM2", "M1", "M2"];
  var ABSENT = { "0": 1, "-": 1, "NONE": 1, "": 1, "NA": 1 };

  var DISCLAIMER =
    "OdontoAge is a research and educational reference implementation of published " +
    "dental age-estimation methods. Estimates carry substantial uncertainty and must " +
    "never be used as the SOLE basis for any legal, forensic, immigration, or clinical " +
    "determination about a real person. Dental age is not chronological age. Age " +
    "estimation of living people (e.g. asylum age-disputes) raises serious scientific " +
    "and ethical concerns; follow the guidance of the relevant professional bodies and " +
    "always keep a qualified human expert in the loop.";

  function sexToG(sex) {
    var s = String(sex == null ? "" : sex).trim().toLowerCase();
    if (["m", "male", "boy", "b", "1", "man"].indexOf(s) >= 0) return 1;
    if (["f", "female", "girl", "g", "0", "woman"].indexOf(s) >= 0) return 0;
    throw new Error("unrecognised sex value: " + sex + " (use male/female)");
  }
  function normalizeSex(sex) { return sexToG(sex) === 1 ? "male" : "female"; }

  function evalLinear(reg, vars) {
    var total = Number(reg.intercept);
    (reg.terms || []).forEach(function (term) {
      var name = term.var, val;
      if (name.indexOf("*") >= 0) {
        val = 1.0;
        name.split("*").forEach(function (f) { val *= Number(vars[f.trim()]); });
      } else {
        if (!(name in vars)) throw new Error("missing regression variable " + name);
        val = Number(vars[name]);
      }
      total += Number(term.coef) * val;
    });
    return total;
  }

  function cameriereOpenApexVars(sex, teeth, variables) {
    var g = sexToG(sex), reasoning = [];
    if (variables) {
      ["x5", "N0", "s"].forEach(function (k) {
        if (!(k in variables)) throw new Error("missing precomputed variable " + k);
      });
      reasoning.push("Using supplied variables x5=" + (+variables.x5).toFixed(4) +
        ", N0=" + variables.N0 + ", s=" + (+variables.s).toFixed(4) + ".");
      return [{ g: g, x5: +variables.x5, N0: +variables.N0, s: +variables.s }, reasoning];
    }
    if (!teeth) throw new Error("provide per-tooth 'teeth' measurements or precomputed 'variables'");
    var xs = {};
    TEETH.forEach(function (t) {
      if (!(t in teeth)) throw new Error("missing tooth " + t + "; need all 7");
      var info = teeth[t], x;
      if (typeof info === "number") x = info;
      else if (!info || info.closed || info.open === false) x = 0.0;
      else if (info.x != null) x = Number(info.x);
      else {
        if (info.Ai == null || info.Li == null) throw new Error("tooth " + t + ": give Ai and Li, or x, or mark closed");
        var Li = Number(info.Li);
        if (Li <= 0) throw new Error("tooth " + t + ": Li must be > 0");
        x = Number(info.Ai) / Li;
      }
      if (x < 0) throw new Error("tooth " + t + ": x must be >= 0");
      xs[t] = x;
    });
    var N0 = 0, s = 0;
    TEETH.forEach(function (t) { if (xs[t] === 0) N0 += 1; s += xs[t]; });
    reasoning.push("Normalised open apices x_i = A_i/L_i (closed -> 0).");
    reasoning.push("s = " + s.toFixed(4) + "; N0 = " + N0 + "/7; x5 = " + xs.PM2.toFixed(4) + ".");
    return [{ g: g, x5: xs.PM2, N0: N0, s: s }, reasoning];
  }

  function runCameriere(m, inp) {
    if (m.measurement === "open_apices") {
      var pair = cameriereOpenApexVars(inp.sex, inp.teeth, inp.variables);
      var age = evalLinear(m.regression, pair[0]);
      pair[1].push("Age = " + age.toFixed(3) + " y from " + m.id + ".");
      return { age: age, reasoning: pair[1], warnings: [], see: m.prediction_error_years };
    }
    if (m.measurement === "pulp_tooth_area") {
      var vv = Object.assign({}, inp.variables || {});
      if (!("RA" in vv)) {
        var aliases = ["RA", "ratio", "pulp_tooth_area_ratio", "area_ratio"];
        for (var ai = 0; ai < aliases.length; ai++) {
          var a = aliases[ai];
          if (a in vv) { vv.RA = Number(vv[a]); break; }
          if (inp[a] != null) { vv.RA = Number(inp[a]); break; }
        }
      }
      if (!("RA" in vv))
        throw new Error("adult method needs the pulp/tooth AREA ratio as variable 'RA' " +
          "(e.g. variables={RA: 0.08}) - pulp area / whole tooth area of the canine");
      var ra = Number(vv.RA);
      if (!(ra > 0 && ra < 1))
        throw new Error("pulp/tooth area ratio RA=" + ra + " is out of range; must be a fraction in (0, 1)");
      var age2 = evalLinear(m.regression, vv);
      var coef = Number(m.regression.terms[0].coef), op = coef < 0 ? "-" : "+";
      return { age: age2, reasoning: [
                 "Adult pulp/tooth AREA-ratio regression (" + m.id + "): age = " +
                   m.regression.intercept + " " + op + " " + Math.abs(coef) + "*RA, RA=" + ra.toFixed(4),
                 "  -> " + age2.toFixed(2) + " y."],
               warnings: ["Adult morphometric methods are less precise than " +
                 "developing-dentition methods (Cameriere reports SEE ~4.2-4.3 y)."],
               see: m.prediction_error_years };
    }
    throw new Error("cameriere: unsupported measurement " + m.measurement);
  }

  function stageValue(map, stage, tooth) {
    var st = String(stage).trim().toUpperCase();
    if (ABSENT[st] != null) return 0.0;
    if (!(st in map)) throw new Error("tooth " + tooth + ": stage " + st + " not defined");
    return Number(map[st]);
  }

  function runDemirjian(m, inp) {
    if (!inp.stages) throw new Error("Demirjian needs 'stages' for all 7 teeth");
    var sexk = normalizeSex(inp.sex);
    var table = (m.scores || {})[sexk];
    if (!table || !Object.keys(table).length) throw new Error("no Demirjian score table for " + sexk);
    var total = 0, reasoning = [];
    TEETH.forEach(function (t) {
      if (!(t in inp.stages)) throw new Error("missing stage for tooth " + t);
      var sc = stageValue(table[t] || {}, inp.stages[t], t);
      total += sc; reasoning.push("  " + t + " stage " + String(inp.stages[t]).toUpperCase() + ": " + sc);
    });
    reasoning.push("Maturity score = " + total.toFixed(1) + " / 100.");
    var age = null, note = "no conversion table available";
    var conv = (m.conversion || {})[sexk];
    if (conv && conv.length) {
      var pts = conv.map(function (p) { return [Number(p[0]), Number(p[1])]; })
                    .sort(function (a, b) { return a[0] - b[0]; });
      if (total <= pts[0][0]) { age = pts[0][1]; note = "clamped low"; }
      else if (total >= pts[pts.length - 1][0]) { age = pts[pts.length - 1][1]; note = "clamped high"; }
      else {
        for (var i = 0; i < pts.length - 1; i++) {
          var s0 = pts[i][0], a0 = pts[i][1], s1 = pts[i + 1][0], a1 = pts[i + 1][1];
          if (total >= s0 && total <= s1) { age = s1 === s0 ? a0 : a0 + (a1 - a0) * (total - s0) / (s1 - s0); note = "interpolated"; break; }
        }
      }
      reasoning.push("Converted to age " + age.toFixed(2) + " y (" + note + ").");
    } else {
      reasoning.push("Age conversion unavailable; maturity score only.");
    }
    return { age: age, maturityScore: total, reasoning: reasoning,
             warnings: ["Demirjian overestimates age in many non-French-Canadian populations."],
             see: m.prediction_error_years };
  }

  function runWillems(m, inp) {
    if (!inp.stages) throw new Error("Willems needs 'stages' for all 7 teeth");
    var sexk = normalizeSex(inp.sex);
    var table = (m.tables || {})[sexk];
    if (!table || !Object.keys(table).length) throw new Error("no Willems table for " + sexk);
    var total = 0, reasoning = [];
    TEETH.forEach(function (t) {
      if (!(t in inp.stages)) throw new Error("missing stage for tooth " + t);
      var v = stageValue(table[t] || {}, inp.stages[t], t);
      total += v; reasoning.push("  " + t + " stage " + String(inp.stages[t]).toUpperCase() + ": " + v + " y");
    });
    reasoning.push("Estimated age = sum = " + total.toFixed(2) + " y.");
    return { age: total, reasoning: reasoning, warnings: [], see: m.prediction_error_years };
  }

  function runKvaal(m, inp) {
    var equation = inp.equation || m.default_equation || "six_teeth";
    var eq = (m.equations || {})[equation];
    if (!eq || eq.intercept == null) throw new Error("Kvaal equation " + equation + " not available");
    if (!inp.variables) throw new Error("Kvaal needs 'variables' (at least M)");
    if (!("M" in inp.variables)) throw new Error("Kvaal needs variable 'M'");
    var M = Number(inp.variables.M);
    var intercept = Number(eq.intercept);
    var age = intercept + Number(eq.M) * M;
    var terms = [intercept + " + " + eq.M + "*M"];
    var detail = ["M=" + M.toFixed(4)];

    var wlCoef = eq.W_minus_L;
    if (wlCoef != null) {
      var wl;
      if ("W_minus_L" in inp.variables) wl = Number(inp.variables.W_minus_L);
      else if (("W" in inp.variables) && ("L" in inp.variables)) wl = Number(inp.variables.W) - Number(inp.variables.L);
      else throw new Error("Kvaal equation " + equation + " needs 'W_minus_L' (or both 'W' and 'L')");
      age += Number(wlCoef) * wl;
      terms.push(wlCoef + "*(W-L)");
      detail.push("(W-L)=" + wl.toFixed(4));
    }

    var gCoef = eq.G;
    var warnings = ["Adult pulp-ratio methods have wide error (Kvaal reports SEE ~8.6-11.5 " +
      "years depending on the equation); treat the result as a broad estimate."];
    if (gCoef != null) {
      if (inp.sex == null) throw new Error("Kvaal equation " + equation +
        " (mandibular lateral incisor) requires 'sex' for its gender term (male=1, female=0)");
      var g = sexToG(inp.sex);
      age += Number(gCoef) * g;
      terms.push(gCoef + "*G");
      detail.push("G=" + g + " (" + (g ? "male" : "female") + ")");
    }

    return { age: age, reasoning: [
               ("Kvaal " + equation + ": age = " + terms.join(" + ")).replace(/\+ -/g, "- "),
               "  with " + detail.join(", ") + "  ->  " + age.toFixed(1) + " y."],
             warnings: warnings, see: eq.see };
  }

  var RUNNERS = { cameriere: runCameriere, demirjian: runDemirjian, willems: runWillems, kvaal: runKvaal };

  function estimate(DATA, methodId, inp) {
    inp = inp || {};
    var m = DATA.methods[methodId];
    if (!m) throw new Error("unknown method " + methodId);
    if (!m.verified && !inp.allowUnverified)
      throw new Error("method " + methodId + " not verified yet (status: " + (m.status || "unverified") + ")");
    var res = RUNNERS[m.family](m, inp);
    var age = res.age, interval = null;
    if (age != null && res.see) {
      var see = Number(res.see);
      interval = { low: age - 1.96 * see, high: age + 1.96 * see, level: 0.95,
                   basis: "+/- 1.96 x SEE (" + see + " y); approximate" };
    }
    var warnings = (res.warnings || []).slice();
    var rng = m.age_range_years;
    if (age != null && rng && rng[0] != null && (age < rng[0] || age > rng[1]))
      warnings.push("Estimated age " + age.toFixed(1) + " y is outside the validated range " +
        rng[0] + "-" + rng[1] + " y; interpret with caution.");
    var src = (DATA.sources || {})[m.source] || {};
    return { method: methodId, label: m.label, dentition: m.dentition,
             estimatedAgeYears: age, interval: interval, maturityScore: res.maturityScore != null ? res.maturityScore : null,
             reasoning: res.reasoning || [], warnings: warnings, citation: src.citation || "",
             doi: src.doi || null, disclaimer: DISCLAIMER, verified: !!m.verified };
  }

  function compare(DATA, inp) {
    inp = inp || {};
    var out = [];
    Object.keys(DATA.methods).forEach(function (mid) {
      var m = DATA.methods[mid];
      if (!m.verified && !inp.allowUnverified) return;
      if (inp.dentition && m.dentition !== inp.dentition) return;
      try { out.push(estimate(DATA, mid, inp)); } catch (e) { /* not applicable */ }
    });
    return out;
  }

  return { TEETH: TEETH, DISCLAIMER: DISCLAIMER, sexToG: sexToG, evalLinear: evalLinear,
           estimate: estimate, compare: compare };
});
