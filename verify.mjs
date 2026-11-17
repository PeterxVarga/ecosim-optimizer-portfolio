// Independent replay: does not import Python optimizer or trust its trace.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const [input, report] = process.argv.slice(2);
const s = JSON.parse(fs.readFileSync(input, 'utf8'));
const r = JSON.parse(fs.readFileSync(report, 'utf8'));
assert.equal(r.evidence, 'synthetic_only');
assert.equal(r.best.decisions.length, s.periods);
assert.equal(r.best.trace.length, s.periods);
let balance = s.initial_cash, ev = s.initial_electric, emissions = 0, passengers = 0;
for (const [i, d] of r.best.decisions.entries()) {
  assert(s.fares.includes(d.fare) && s.conversions.includes(d.conversion));
  ev += d.conversion;
  assert(ev <= s.total_vehicles);
  const diesel = s.total_vehicles - ev;
  const carried = Math.min(7 * diesel + 9 * ev, Math.max(0,s.demand[i] - 3*(d.fare-4)));
  balance = balance + d.fare * carried - 45*d.conversion - 3*ev - 6*diesel - 16;
  assert(balance >= s.minimum_cash);
  passengers += carried;
  emissions += 2*ev + 8*diesel;
  assert.deepEqual(r.best.trace[i], {cash:balance,electric:ev,emissions,served:passengers});
}
assert.equal(r.best.objective, balance + 2*passengers - 3*emissions);
console.log('PASS: independent synthetic replay; feasibility and objective agree (not optimality proof)');
