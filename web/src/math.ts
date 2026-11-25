/** Browser-local calculations for fictional planning scenarios. */
export type Pilot = {
  baseline: number; effect: number; capacity: number; concentration: number;
  capture: number; allocation: number; alpha: number; attrition: number;
  clusterSize: number; icc: number;
};

export function normal(x: number) {
  const a = Math.abs(x);
  if (a >= 8) return x > 0 ? 1 : 0;
  // Integrate the standard normal density using its odd-power series.
  let sum = a, term = a;
  for (let k = 3; term > Number.EPSILON * sum; k += 2) {
    term *= a * a / k;
    sum += term;
  }
  const area = sum * Math.exp(-a * a / 2) / Math.sqrt(2 * Math.PI);
  return x < 0 ? 0.5 - area : 0.5 + area;
}

function invert(f: (x: number) => number, target: number) {
  let low = 0, high = 20;
  for (let i = 0; i < 50; i++) {
    const mid = (low + high) / 2;
    if (f(mid) < target) low = mid;
    else high = mid;
  }
  return high;
}

export function pilotDesign(p: Pilot, enrollment: number, target: number) {
  const {baseline, effect, capacity, concentration, capture, allocation, alpha} = p;
  if (!Object.values(p).every(Number.isFinite) || !Number.isSafeInteger(enrollment) || enrollment < 2
      || !(baseline > 0 && baseline < 1 && capacity > 0 && capacity <= 1 && concentration >= 1
      && capture >= 0 && capture <= 1 && allocation > 0 && allocation < 1 && alpha > 0 && alpha < 1
      && target > alpha && target < 1 && p.attrition >= 0 && p.attrition < 1
      && p.clusterSize >= 1 && p.icc >= 0 && p.icc < 1)) {
    throw new Error('Enter valid values for each assumption.');
  }
  const high = capacity === 1 ? effect : concentration * effect;
  const low = capacity === 1 ? effect : (effect - capacity * high) / (1 - capacity);
  if ([high, low].some(tau => baseline + tau < 0 || baseline + tau > 1)) {
    throw new Error('These assumptions imply a subgroup outcome rate outside 0–100%. Adjust the effect or concentration.');
  }
  const uniform = baseline + capacity * effect;
  const gain = capacity * capture * (high - effect);
  const targeted = uniform + gain;
  const variance = (uniform * (1 - uniform) / (1 - allocation) + targeted * (1 - targeted) / allocation)
    * (1 + (p.clusterSize - 1) * p.icc) / (1 - p.attrition);
  const z = invert(normal, 1 - alpha / 2);
  const atShift = (shift: number) => normal(shift - z) + normal(-shift - z);
  const requiredShift = invert(atShift, target);
  const power = (n: number) => gain === 0 ? alpha : atShift(Math.abs(gain) * Math.sqrt(n / variance));
  const required = gain === 0 ? null : Math.max(2, Math.ceil(requiredShift ** 2 * variance / gain ** 2));
  return {uniform, targeted, gain, power, required, mde: requiredShift * Math.sqrt(variance / enrollment)};
}

export type Band = { name: string; share: number; risk: number; effect: number };
export const bands: readonly Band[] = [
  {name: 'Highest risk', share: 0.25, risk: 3, effect: 0.012},
  {name: 'Elevated risk', share: 0.35, risk: 2, effect: 0.041},
  {name: 'Moderate risk', share: 0.40, risk: 1, effect: 0.022},
];

export function comparePolicies(capacity: number, profile: readonly Band[] = bands) {
  if (!Number.isFinite(capacity) || capacity < 0 || capacity > 1) throw new Error('Capacity must be 0–100%.');
  const rank = (key: 'risk' | 'effect') => {
    let remainder = capacity;
    return [...profile].sort((a, b) => b[key] - a[key]).reduce((total, band) => {
      const portion = Math.min(remainder, band.share);
      remainder -= portion;
      return total + portion * band.effect;
    }, 0);
  };
  const uniform = profile.reduce((total, band) => total + capacity * band.share * band.effect, 0);
  return {uniform, risk: rank('risk'), benefit: rank('effect')};
}

export type Channel = {name: string; cents: number; effect: number; spread: number; eligible: number};

export function plan(population: number, capacity: number, budget: number, channels: readonly Channel[]) {
  if (!Number.isSafeInteger(population) || population < 1 || !Number.isFinite(capacity)
      || capacity < 0 || capacity > 1 || !Number.isSafeInteger(budget) || budget < 0) {
    throw new Error('Use a positive population, valid capacity, and a nonnegative budget.');
  }
  return channels.map(channel => {
    if (!Number.isSafeInteger(channel.cents) || channel.cents < 0 || !Number.isFinite(channel.effect)
        || !Number.isFinite(channel.spread) || channel.spread < 0 || !Number.isFinite(channel.eligible)
        || channel.eligible < 0 || channel.eligible > 1) {
      throw new Error('Channel assumptions are out of range.');
    }
    const contacts = Math.min(Math.floor(population * capacity), Math.floor(population * channel.eligible),
      channel.cents > 0 ? Math.floor(budget / channel.cents) : population);
    const spend = contacts * channel.cents / 100;
    const gain = contacts * channel.effect;
    return {...channel, contacts, spend, gain, low: contacts * (channel.effect - channel.spread),
      high: contacts * (channel.effect + channel.spread), perGain: gain > 0 ? spend / gain : null};
  });
}

export function planBenchmark(eligible: number, complete: number, reachable: number, capacity: number,
  budgetCents: number, costCents: number, benchmarkPercent: number) {
  if (![eligible, complete, reachable, capacity, budgetCents, costCents, benchmarkPercent].every(Number.isSafeInteger)
    || eligible < 1 || eligible > 10000000 || complete < 0 || complete > eligible || reachable < 0
    || reachable > eligible - complete || capacity < 0 || budgetCents < 0 || costCents < 0
    || benchmarkPercent < 0 || benchmarkPercent > 100) {
    return null;
  }
  const needed = Math.max(0, Math.ceil(eligible * benchmarkPercent / 100) - complete);
  const affordable = costCents === 0 ? reachable : Math.floor(budgetCents / costCents);
  const contacts = Math.min(reachable, capacity, affordable);
  return {needed, contacts, spend: contacts * costCents / 100,
    requiredEffect: needed === 0 ? 0 : contacts > 0 ? needed / contacts : null};
}
