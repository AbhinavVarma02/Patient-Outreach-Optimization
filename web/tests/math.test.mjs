import assert from 'node:assert/strict';
import {test} from 'node:test';
import {comparePolicies, pilotDesign, plan} from '../src/math.ts';
const scenario = {baseline:.315,effect:.026,capacity:.2,concentration:2,capture:.7,
  allocation:.5,alpha:.05,attrition:.05,clusterSize:1,icc:0};

test('targeting has matched capacity and converges when everyone is contacted', () => {
  const result = comparePolicies(.2);
  assert.ok(Math.abs(result.benefit - .0082) < 1e-12);
  assert.ok(result.benefit > result.uniform);
  assert.ok(result.uniform > result.risk);
  const all = comparePolicies(1);
  assert.ok(Math.abs(all.risk-all.benefit) < 1e-12);
  assert.ok(Math.abs(all.uniform-all.benefit) < 1e-12);
});

test('planner enforces floor of budget, contacts and eligibility', () => {
  const [quoted,free] = plan(100,.9,101,[
    {name:'paid',cents:20,effect:.05,spread:.02,eligible:.08},
    {name:'free',cents:0,effect:-.02,spread:0,eligible:.2},
  ]);
  assert.deepEqual([quoted.contacts,quoted.spend,quoted.gain,quoted.perGain], [5,1,.25,4]);
  assert.equal(free.contacts,20);
  assert.equal(free.perGain,null);
});

test('power calculation crosses the target and handles zero gain', () => {
  const result = pilotDesign(scenario,60000,.8);
  assert.ok(Math.abs(result.gain - .00364) < 1e-12);
  assert.equal(result.required, 544545);
  assert.ok(result.power(result.required) >= .8);
  assert.ok(result.power(result.required-1) < .8);
  const nullPolicy = pilotDesign({...scenario,capture:0},60000,.8);
  assert.equal(nullPolicy.required,null);
  assert.ok(Math.abs(nullPolicy.power(60000)-.05) < 1e-7);
  assert.throws(() => pilotDesign({...scenario,baseline:.99,effect:.2},60000,.8));
});
