import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { bands, comparePolicies, pilotDesign, plan, planBenchmark } from './math';
import { osf, paper, studies, supplement } from './evidence';
import haryana from './haryana.json';
import sierra from './sierra-leone.json';
import us from './us-evidence.json';
import './style.css';

const views = {overview: 'Overview', targeting: 'Patient Targeting', planner: 'Outreach Planner',
  pilot: 'Pilot Designer', evidence: 'Evidence & Methods'} as const;
type View = keyof typeof views;
const readView = () => Object.hasOwn(views, location.hash.slice(1)) ? location.hash.slice(1) as View : 'overview';
const number = (value: number, digits = 0) => value.toLocaleString('en-US', {maximumFractionDigits: digits});
const money = (value: number) => value.toLocaleString('en-US', {style:'currency',currency:'USD'});
const pp = (value: number) => number(value * 100, 2) + ' pp';
const cmsNotes = 'https://www.cms.gov/files/document/2027-star-ratings-technical-notes.pdf';
const uclaResults = 'https://clinicaltrials.gov/study/NCT05525494?tab=results';
const scoreArticle = 'https://doi.org/10.1001/jamanetworkopen.2024.46693';

function Icon({name}: { name: 'mark' | 'arrow' | 'theme' }) {
  const paths = {mark: 'M3 17h18M5 13l5-4 4 2 5-6m-4 0h4v4', arrow: 'M4 12h15m-6-6 6 6-6 6',
    theme: 'M20 15a8.5 8.5 0 0 1-11-11 8.5 8.5 0 1 0 11 11Z'};
  return <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"
    strokeLinecap="round" strokeLinejoin="round"><path d={paths[name]}/></svg>;
}

function App() {
  const [view, setView] = useState(readView);
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem('outreach-theme') ?? 'system'; }
    catch { return 'system'; }
  });
  useEffect(() => {
    const change = () => {
      setView(readView());
      window.scrollTo(0, 0);
      requestAnimationFrame(() => document.getElementById('content')?.focus({preventScroll: true}));
    };
    window.addEventListener('hashchange', change);
    return () => window.removeEventListener('hashchange', change);
  }, []);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('outreach-theme', theme); }
    catch { /* Theme remains usable without storage. */ }
  }, [theme]);
  useEffect(() => { document.title = views[view] + ' | Patient Outreach Optimization'; }, [view]);
  return <>
    <a className="skip" href="#content" onClick={event => { event.preventDefault(); document.getElementById('content')?.focus(); }}>Skip to content</a>
    <header className="masthead"><div className="mast-inner">
      <a className="brand" href="#overview"><span className="brand-icon"><Icon name="mark"/></span>
        <span>Patient Outreach<span className="brand-second"> Optimization</span></span></a>
      <label className="theme"><Icon name="theme"/><span className="sr-only">Color theme</span>
        <select aria-label="Color theme" value={theme} onChange={e => setTheme(e.target.value)}>
          <option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option>
        </select></label>
    </div></header>
    <nav aria-label="Workspace" className="nav"><div className="nav-inner">
      {(Object.entries(views) as [View, string][]).map(([id,label]) =>
        <a href={'#' + id} key={id} aria-current={view === id ? 'page' : undefined}>{label}</a>)}
    </div></nav>
    <main id="content" tabIndex={-1}>
      {view === 'overview' && <Overview/>}
      {view === 'targeting' && <Targeting/>}
      {view === 'planner' && <Planner/>}
      {view === 'pilot' && <Pilot/>}
      {view === 'evidence' && <Evidence/>}
    </main>
    <footer><div className="foot"><span>Patient Outreach Optimization</span><span>Research demo · No patient data</span><a href="#evidence">Sources and limits <span aria-hidden="true">↗</span></a></div></footer>
  </>;
}

function Overview() {
  return <>
    <section className="hero">
      <div className="hero-copy"><p className="eyebrow"><span className="dot"/> Preventive care research</p>
        <h1>Which outreach strategy is worth testing?</h1>
        <p>Compare targeting rules and channel costs, then size a randomized pilot.</p>
        <div className="hero-actions"><a href="#targeting" className="button">Explore targeting <Icon name="arrow"/></a>
          <a href="#evidence" className="hero-link">Read the evidence <span aria-hidden="true">↗</span></a></div>
      </div>
      <figure className="hero-figure">
        <figcaption><span>FICTIONAL SCENARIO</span><strong>Risk and benefit can diverge</strong></figcaption>
        <svg className="hero-chart" viewBox="0 0 410 210" role="img" aria-label="Fictional vaccination gains: moderate risk 2.2, elevated risk 4.1, highest risk 1.2 percentage points.">
          <path className="plot-grid" d="M41 18H389M41 49H389M41 80H389M41 111H389M41 142H389M41 173H389"/>
          <g className="hero-axis" textAnchor="end"><text x="32" y="22">5</text><text x="32" y="53">4</text><text x="32" y="84">3</text><text x="32" y="115">2</text><text x="32" y="146">1</text><text x="32" y="177">0</text></g>
          <rect x="64" y="105" width="66" height="68" rx="3" className="muted-bar"/>
          <rect x="182" y="46" width="66" height="127" rx="3" className="bright-bar"/>
          <rect x="300" y="136" width="66" height="37" rx="3" className="muted-bar"/>
          <g className="hero-axis" textAnchor="middle"><text x="97" y="194">Moderate</text><text x="215" y="194">Elevated</text><text x="333" y="194">Highest</text></g>
          <g className="hero-values" textAnchor="middle"><text x="97" y="97">+2.2</text><text x="215" y="37">+4.1</text><text x="333" y="128">+1.2</text></g>
        </svg>
        <p>Assumed vaccination gain by risk group (pp)</p>
      </figure>
    </section>
    <aside className="evidence-strip"><span className="dot"/><p><strong>Research demo.</strong> Explore fictional scenarios alongside CMS benchmarks and randomized trials.</p><a href="#evidence">Evidence status <span aria-hidden="true">↗</span></a></aside>
    <section className="section"><div className="section-title"><h2>From targeting to a pilot</h2></div>
      <div className="workflow">
        <Workflow view="targeting" verb="Compare targeting rules" detail="Compare risk and expected benefit at equal capacity."/>
        <Workflow view="planner" verb="Plan outreach costs" detail="Compare channels and size a Medicare Advantage quality gap."/>
        <Workflow view="pilot" verb="Size a randomized pilot" detail="Estimate enrollment and statistical power."/>
      </div>
    </section>
    <section className="section snapshot"><div className="section-title"><h2>Trial evidence</h2><a href="#evidence">Explore methods <span aria-hidden="true">↗</span></a></div>
      <div className="snapshot-grid"><div><h3>Flu reminder content</h3><p>Three Geisinger trials tested risk disclosure, framing and reminders.</p><a href={paper}>Published article <span aria-hidden="true">↗</span></a></div>
      <div><h3>Flu reminder channels</h3><p>Geisinger tested letter, portal and SMS combinations among eligible patients.</p><a href={supplement}>Study 4 supplement <span aria-hidden="true">↗</span></a></div></div>
    </section>
  </>;
}

function Workflow({view, verb, detail}: {view: View; verb: string; detail: string}) {
  return <a className="workflow-item" href={'#' + view}><span className="workflow-label">{views[view]} <Icon name="arrow"/></span>
    <strong>{verb}</strong><span>{detail}</span></a>;
}

function Page({title, copy, children}: React.PropsWithChildren<{title: string; copy: string}>) {
  return <div className="page"><div className="page-title">
    <h1>{title}</h1><p>{copy}</p></div>{children}</div>;
}
function Field({label, value, min, max, step = 1, unit, onChange}: {
  label: string; value: number; min: number; max: number; step?: number; unit?: string; onChange: (value: number) => void;
}) {
  return <label className="field"><span>{label}</span><span className="input-wrap"><input type="number" required aria-label={label}
    value={Number.isNaN(value) ? '' : value} min={min} max={max} step={step} onChange={e => onChange(e.target.valueAsNumber)}/>
    {unit && <span className="unit" aria-hidden="true">{unit}</span>}</span></label>;
}
function Table({caption, headings, rows}: {caption: string; headings: string[]; rows: (string | number)[][]}) {
  return <div className="table-scroll" tabIndex={0} role="region" aria-label={caption}><table><caption>{caption}</caption>
    <thead><tr>{headings.map(title => <th key={title} scope="col">{title}</th>)}</tr></thead>
    <tbody>{rows.map(([first, ...values]) => <tr key={first}><th scope="row">{first}</th>
      {values.map((value,index) => <td key={index}>{value}</td>)}</tr>)}</tbody>
  </table></div>;
}

function Targeting() {
  const [capacity, setCapacity] = useState(20);
  const [shape, setShape] = useState('inverted');
  const profile = shape === 'inverted' ? bands : bands.map((band,i) => ({
    ...band, effect: shape === 'flat' ? 0.027 : [0.045,0.027,0.012][i],
  }));
  const result = comparePolicies(capacity/100, profile);
  const values = [['Uniform', result.uniform], ['Clinical risk', result.risk], ['Outreach benefit', result.benefit]] as const;
  const max = Math.max(0.001, ...values.map(([,value]) => value));
  return <Page title="Patient Targeting" copy="Compare who gets outreach when every rule reaches the same share of people.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Fictional inputs</p><h2>Targeting assumptions</h2>
      <label className="field"><span>Outreach capacity <output>{capacity}%</output></span>
        <input type="range" min="0" max="100" value={capacity} onChange={e => setCapacity(e.target.valueAsNumber)}/></label>
      <label className="field">Effect pattern<select value={shape} onChange={e => setShape(e.target.value)}>
        <option value="inverted">Most benefit at elevated risk</option><option value="monotone">More benefit at higher risk</option><option value="flat">Same benefit across groups</option>
      </select></label>
    </aside><section className="output"><p className="eyebrow">Matched capacity · {capacity}%</p><h2>Projected extra vaccinations</h2>
      <p>Per 1,000 eligible people versus no added outreach.</p>
      <svg className="policy-chart" viewBox="0 0 610 177" role="img" aria-label={'Projected extra vaccinations per 1,000 eligible people: ' + values.map(([label, value]) => label + ' ' + number(value * 1000, 2)).join(', ')}>
        {values.map(([label, value], i) => <g key={label}><text x="0" y={33+54*i}>{label}</text>
          <rect x="163" y={16+54*i} width="350" height="22" rx="4" className="track"/>
          <rect x="163" y={16+54*i} width={350*value/max} height="22" rx="4" className={i === 2 ? 'primary-bar' : 'secondary-bar'}/>
          <text x="532" y={33+54*i}>{number(value*1000,2)}</text></g>)}
      </svg>
      <Table caption="Vaccinations by targeting rule" headings={['Allocation rule','Extra vaccinations per 1,000']}
        rows={values.map(([label, value]) => [label, number(value*1000,2)])}/>
      <div className="callout"><strong>{pp(result.benefit-result.uniform)}</strong> projected gain over uniform outreach. Fixed fictional inputs have no confidence interval.</div>
    </section></div>
    <section className="section"><h2>Assumed effects by risk group</h2><Table caption="Fictional population" headings={['Risk band','Share eligible','Effect of outreach']}
      rows={profile.map(band => [band.name, number(band.share*100)+'%', pp(band.effect)])}/></section>
    <div className="page-next"><a className="text-link" href="#planner">Compare channel costs <Icon name="arrow"/></a> <a href="#evidence">Evidence and limits</a></div>
  </Page>;
}

const defaults = [
  {name:'SMS', cents:12, effect:0.008, spread:0.005, eligible:0.80},
  {name:'Patient portal', cents:25, effect:0.015, spread:0.008, eligible:0.65},
  {name:'Letter', cents:125, effect:0.028, spread:0.012, eligible:0.95},
];
function Planner() {
  const [population, pop] = useState(10000), [capacity, cap] = useState(35), [budget, bud] = useState(1800);
  const [options, setOptions] = useState(defaults);
  const [index, select] = useState(0);
  const option = options[index];
  const update = (fields: Partial<typeof option>) => setOptions(options.map((item,i) => i === index ? {...item,...fields} : item));
  const valid = Number.isInteger(population) && population >= 1 && population <= 10000000 && capacity >= 0 && capacity <= 100
    && budget >= 0 && budget <= 10000000 && options.every(o => Number.isSafeInteger(o.cents) && o.cents >= 0 && o.cents <= 10000
    && Math.abs(o.effect)+o.spread <= 1 && o.effect >= -0.20 && o.effect <= 0.20 && o.spread >= 0 && o.spread <= 0.20
    && o.eligible >= 0 && o.eligible <= 1);
  const rows = valid ? plan(population, capacity/100, Math.round(budget*100), options) : null;
  const best = rows?.reduce((a,b) => b.gain > a.gain ? b : a);
  return <Page title="Outreach Planner" copy="Compare outreach channels under the same budget and contact limit.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Fictional inputs</p><h2>Planning assumptions</h2>
      <Field label="Eligible population" value={population} min={1} max={10000000} onChange={pop}/>
      <Field label="Maximum contacts (%)" value={capacity} min={0} max={100} unit="%" onChange={cap}/>
      <Field label="Budget (USD)" value={budget} min={0} max={10000000} step={0.01} unit="USD" onChange={bud}/>
      <label className="field">Channel to edit<select value={index} onChange={e => select(Number(e.target.value))}>{options.map((item,i) => <option key={item.name} value={i}>{item.name}</option>)}</select></label>
      <Field label="Cost per contact (USD)" value={option.cents/100} min={0} max={100} step={0.01} unit="USD" onChange={value => update({cents:Math.round(value*100)})}/>
      <Field label="Channel eligibility (%)" value={option.eligible*100} min={0} max={100} unit="%" onChange={value => update({eligible:value/100})}/>
      <Field label="Vaccination gain (pp)" value={+(option.effect*100).toFixed(4)} min={-20} max={20} step={0.1} unit="pp" onChange={value => update({effect:value/100})}/>
      <Field label="Effect margin (pp)" value={+(option.spread*100).toFixed(4)} min={0} max={20} step={0.1} unit="pp" onChange={value => update({spread:value/100})}/>
      <button className="secondary-button" onClick={() => {pop(10000);cap(35);bud(1800);setOptions(defaults);select(0);}}>Reset assumptions</button>
    </aside><section className="output"><p className="eyebrow">Scenario estimate</p><h2>Channel comparison</h2>
      {best && rows ? <>
        <div className="metrics" aria-live="polite"><div><span>Top channel by projected gain</span><strong>{best.gain > 0 ? best.name : 'No outreach'}</strong></div>
        <div><span>Extra vaccinations</span><strong>{number(Math.max(0,best.gain),1)}</strong></div>
        <div><span>Projected spend</span><strong>{money(best.gain > 0 ? best.spend : 0)}</strong></div></div>
        <Table caption="Results by channel" headings={['Channel','Contacts','Spend','Extra vaccinations','Sensitivity range','Cost per extra vaccination']}
          rows={rows.map(row => [row.name, number(row.contacts), money(row.spend), number(row.gain,1),
            number(row.low,1)+' to '+number(row.high,1), row.perGain === null ? 'N/A' : money(row.perGain)])}/>
        <p className="small">The range adds and subtracts the effect margin. Cost per extra vaccination is unstable near zero gain.</p>
      </> : <p role="status" className="callout">Check the population, contact limit, budget and channel inputs.</p>}
      <div className="callout"><a href={supplement}>Geisinger tested specific channel combinations</a> among eligible patients.</div>
    </section></div>
    <PayerPlanning/>
    <div className="page-next"><a className="text-link" href="#pilot">Size the pilot <Icon name="arrow"/></a></div>
  </Page>;
}

const gapDefaults = {eligible:10000, complete:6000, reachable:3000, contacts:2500, budget:1800, cost:0.75};

function PayerPlanning() {
  const measures = us.measures.filter(measure => measure.id === 'C03' || measure.id === 'C02');
  const [measureId, setMeasureId] = useState('C03');
  const [inputs, setInputs] = useState(gapDefaults);
  const measure = measures.find(candidate => candidate.id === measureId)!;
  const fields = [
    ['eligible', 'Measure-eligible members', 1, 10000000, 1],
    ['complete', 'Expected completions with usual care', 0, 10000000, 1],
    ['reachable', 'Reachable members still due', 0, 10000000, 1],
    ['contacts', 'Contact limit', 0, 10000000, 1],
    ['budget', 'Campaign budget (USD)', 0, 10000000, 0.01],
    ['cost', 'Campaign cost per contact (USD)', 0, 10000, 0.01],
  ] as const;
  const inRange = fields.every(([key, , min, max]) => inputs[key] >= min && inputs[key] <= max);
  const result = inRange ? planBenchmark(inputs.eligible, inputs.complete, inputs.reachable, inputs.contacts,
    Math.round(inputs.budget * 100), Math.round(inputs.cost * 100), measure.cmsMean) : null;
  return <section className="section">
    <div className="section-title"><h2>Medicare Advantage gap planning</h2><a href={cmsNotes}>CMS benchmark <span aria-hidden="true">↗</span></a></div>
    <p>Estimate the extra completions needed to reach the CMS average.</p>
    <div className="workbench"><aside className="controls"><p className="eyebrow">Fictional plan inputs</p><h3>Campaign assumptions</h3>
      <label className="field">Quality measure<select value={measureId} onChange={event => setMeasureId(event.target.value)}>
        {measures.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
      </select></label>
      {fields.map(([key, label, min, max, step]) => <Field key={key} label={label} value={inputs[key]} min={min}
        max={max} step={step} onChange={value => setInputs(previous => ({...previous, [key]: value}))}/>)}
      <button className="secondary-button" onClick={() => {setInputs(gapDefaults); setMeasureId('C03');}}>Reset gap assumptions</button>
    </aside><div className="output"><p className="eyebrow">Benchmark scenario</p><h3>Campaign target</h3>
      {result ? <>
        <div className="metrics" aria-live="polite">
          <div><span>CMS {us.ratingsYear} contract average</span><strong>{measure.cmsMean}%</strong></div>
          <div><span>Additional completions needed</span><strong>{number(result.needed)}</strong></div>
          <div><span>Feasible contacts</span><strong>{number(result.contacts)}</strong></div>
        </div>
        <p>Projected contact spend is {money(result.spend)}.</p>
        <div className="callout" aria-live="polite">{result.needed === 0 ? 'Usual care meets the benchmark.'
          : result.requiredEffect === null ? 'The budget and contact limits allow zero contacts.'
          : result.requiredEffect > 1 ? 'Too few contacts to close the gap, even if every member contacted completes.'
          : <><strong>{pp(result.requiredEffect)}</strong> minimum gain in completion rate among contacted members.</>}</div>
      </> : <p className="callout" role="status">Check counts and costs. Reachable members cannot exceed members still due.</p>}
      <p className="small">The CMS average is descriptive. The eligible population stays fixed, with at most one completion per contact.</p>
      <a href="#evidence">US trial evidence <span aria-hidden="true">↗</span></a>
    </div></div>
  </section>;
}

const pilotDefaults = {enrollment:60000, baseline:31.5, effect:2.6, capacity:20, concentration:2,
  capture:70, allocation:50, alpha:5, attrition:5, clusterSize:1, icc:0, target:80};
function Pilot() {
  const [data, set] = useState(pilotDefaults);
  const fields = [
    ['enrollment','Planned enrollment',2,100000000,1,''],
    ['baseline','Baseline vaccination rate (%)',1,99,0.1,'%'],
    ['effect','Average outreach effect (pp)',-20,20,0.1,'pp'],
    ['capacity','Outreach capacity (%)',1,100,1,'%'],
    ['concentration','Target group effect (× average)',1,10,0.1,'×'],
    ['capture','Share of ideal targeting gain (%)',0,100,1,'%'],
    ['allocation','Assigned to targeting (%)',5,95,1,'%'],
    ['target','Target power (%)',50,99,1,'%'],
    ['alpha','Significance level (%)',0.1,25,0.1,'%'],
    ['attrition','Expected attrition (%)',0,80,1,'%'],
    ['clusterSize','Mean cluster size',1,10000,0.1,''],
    ['icc','Within-cluster correlation (%)',0,95,1,'%'],
  ] as const;
  const d = data;
  let result: ReturnType<typeof pilotDesign> | undefined;
  let error = '';
  try {
    for (const [key,label,min,max] of fields) {
      if (!Number.isFinite(d[key]) || d[key] < min || d[key] > max) {
        throw new Error(label + ' must be between ' + min + ' and ' + max + '.');
      }
    }
    result = pilotDesign({baseline:d.baseline/100,effect:d.effect/100,capacity:d.capacity/100,concentration:d.concentration,
      capture:d.capture/100,allocation:d.allocation/100,alpha:d.alpha/100,attrition:d.attrition/100,
      clusterSize:d.clusterSize,icc:d.icc/100},d.enrollment,d.target/100);
  } catch (cause) { error = cause instanceof Error ? cause.message : 'Invalid scenario.'; }
  const maxN = result ? Math.min(1e9, Math.max(20, d.enrollment*1.4, (result.required || d.enrollment)*1.15)) : 0;
  const positions = result ? Array.from({length:41},(_,i) => [i/40, result.power(maxN*i/40)]) : [];
  return <Page title="Pilot Designer" copy="Size a trial of a fixed targeting rule against uniform outreach at equal capacity.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Trial inputs</p><h2>Design assumptions</h2>
      {fields.slice(0,8).map(([key,label,min,max,step,unit]) => <Field key={key} {...{label,min,max,step,unit}} value={d[key]}
        onChange={value => set({...d,[key]:value})}/>)}
      <details><summary>Significance, attrition and clustering</summary>{fields.slice(8).map(([key,label,min,max,step,unit]) =>
        <Field key={key} {...{label,min,max,step,unit}} value={d[key]} onChange={value => set({...d,[key]:value})}/>)}</details>
      <button className="secondary-button" onClick={() => set(pilotDefaults)}>Reset assumptions</button>
    </aside><section className="output"><p className="eyebrow">Analytic projection</p><h2>Power to detect a difference</h2>
      {result ? <>
        <div className="metrics" aria-live="polite"><div><span>Required enrollment</span><strong>{result.required === null ? 'No finite sample size' : result.required >= 1e9 ? 'Over 1 billion' : number(result.required)}</strong></div>
          <div><span>Power at {number(d.enrollment)}</span><strong>{number(result.power(d.enrollment)*100,1)}%</strong></div>
          <div><span>Minimum detectable difference</span><strong>{pp(result.mde)}</strong></div></div>
        <svg className="power-chart" viewBox="0 0 620 260" role="img" aria-label={'Projected power by total enrollment. At '+number(d.enrollment)+' participants, power is '+number(result.power(d.enrollment)*100,1)+' percent.'}>
          {[0,0.25,0.5,0.75,1].map(p => <g key={p}><path className="gridline" d={'M 51 '+(215-p*190)+' H 594'}/><text x="1" y={220-p*190}>{p*100}%</text></g>)}
          <path className="target-line" d={'M51 '+(215-d.target*1.9)+' H594'}/>
          <polyline className="curve" points={positions.map(([x,y]) => (51+x*543)+','+(215-y*190)).join(' ')}/>
          <circle className="primary-bar" cx={51+d.enrollment/maxN*543} cy={215-result.power(d.enrollment)*190} r="6"/>
          <text x="51" y="241">0</text><text x="322" y="241" textAnchor="middle">{number(maxN/2)}</text>
          <text x="594" y="241" textAnchor="end">{number(maxN)}</text>
        </svg>
        <p className="small">The dashed line marks target power. Enrollment includes both arms and accounts for attrition.</p>
        <Table caption="Projected power by enrollment" headings={['Enrollment','Estimated power']} rows={[0.5,1,1.5,2].map(multiplier => {
          const n = Math.max(2,Math.round(d.enrollment*multiplier)); return [number(n),number(result.power(n)*100,1)+'%'];
        }).filter((row,i,all) => i === 0 || row[0] !== all[i-1][0])}/>
        <div className="callout"><strong>{pp(result.gain)}</strong> assumed gain over uniform outreach.</div>
      </> : <p role="status" className="callout">{error}</p>}
    </section></div>
  </Page>;
}

function Evidence() {
  return <Page title="Evidence & Methods" copy="Review trial findings, methods and data access.">
    <div className="evidence-strip"><span className="dot"/><p><strong>Study access.</strong> We reproduced results from Sierra Leone and Haryana. Geisinger summaries use published findings while data reuse permission is pending.</p></div>
    <USEvidence/>
    <SierraLeoneEvidence/>
    <HaryanaEvidence/>
    <section className="section"><div className="section-title"><h2>Geisinger flu trials</h2><a href={paper}>Published article <span aria-hidden="true">↗</span></a></div>
      <div className="study-grid">{studies.map(study => <article className="study" key={study.id}><p className="eyebrow">Study {study.number} · {study.season}</p>
        <h3>{study.scope}</h3><p><strong>{study.population}</strong></p>
        {'contrast' in study && <p>{study.contrast}</p>}<p className="small">{study.status}</p>
        <a href={'https://clinicaltrials.gov/study/'+study.id}>{study.id} <span aria-hidden="true">↗</span></a>
      </article>)}</div>
    </section>
    <section className="section snapshot"><div className="section-title"><h2>Letter outreach versus no study outreach</h2><a href={supplement}>Supplement, section 7.2 <span aria-hidden="true">↗</span></a></div>
      <p>Letter-only assignment increased 29-day vaccination by 2.5 percentage points (95% CI 0.9 to 4.0) versus passive control among participants eligible for letter, portal and SMS.</p>
    </section>
    <section className="section methods"><h2>Methods and limits</h2>
      <details open><summary>Assignment and outcomes</summary><p>Effects compare assigned groups, regardless of delivery or response. Eligibility, seasons and follow-up differ across trials.</p></details>
      <details><summary>Scenario and power assumptions</summary><p>The calculators use fictional inputs. The pilot assumes a fixed rule, stable rates and attrition unrelated to outcomes. It uses a normal approximation and adjusts variance using mean cluster size. The minimum detectable difference holds variance fixed.</p></details>
      <details><summary>Trial document extraction</summary><p>Trial summaries use reviewed sources. On 12 held-out protocols, the best rules-based method matched 7 of 13 scorable fields. The verified local model matched 2 of 13. Release required at least 90% exact match and correct abstention. <a href="https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/AI_EVALUATION.md">Benchmark results</a></p></details>
      <details><summary>Data provenance and rights</summary><p>The public <a href={osf}>OSF catalog</a> lists no dataset license. The app uses aggregate evidence and stores only the theme preference.</p></details>
    </section>
  </Page>;
}

function USEvidence() {
  const flu = us.influenzaTrial;
  const crc = us.screeningTrial;
  const shown = (value: number, unit: string) => number(value, 1) + (unit === '%' ? '%' : '');
  const rr = (value: number) => value.toFixed(2);
  return <section className="section snapshot">
    <div className="section-title"><h2>US payer evidence</h2><a href={cmsNotes}>CMS technical notes <span aria-hidden="true">↗</span></a></div>
    <p>The {us.ratingsYear} CMS ratings summarize local and regional Medicare Advantage coordinated care contracts with reported values.</p>
    <Table caption="CMS quality and member experience" headings={['Measure', 'CMS average', 'Middle half', 'Reported contracts']}
      rows={us.measures.map(measure => [measure.name, shown(measure.cmsMean, measure.unit),
        measure.iqr.map(value => shown(value, measure.unit)).join(' to '), number(measure.reported)])}/>
    <p className="small">Reporting periods and denominators vary. Access to care uses a 0–100 survey score.</p>
    <h3>US randomized trials</h3>
    <p><a href={uclaResults}>UCLA flu trial</a> found no clear gain from added text or portal reminder bundles. The registry lists {flu.window} for the primary outcome.</p>
    <Table caption="UCLA influenza vaccination by assigned reminder" headings={['Group', 'Vaccination', 'Adjusted risk ratio (95% CI)']}
      rows={Object.entries(flu.arms).map(([name, arm]) => [name, shown(arm.rate, '%'),
        'adjustedRR' in arm ? rr(arm.adjustedRR) + ' (' + arm.ci.map(rr).join(' to ') + ')' : 'Reference'])}/>
    <p>In the <a href={scoreArticle}>SCORE trial</a>, mailed stool test kits, reminders and navigation increased colorectal screening at {crc.window} by {crc.total.pp} pp overall (95% CI {crc.total.ci.join(' to ')} pp) in two North Carolina health center systems. The Medicare subgroup gained {crc.medicare.pp} pp (95% CI {crc.medicare.ci.join(' to ')} pp). The effect in Medicare Advantage remains unknown.</p>
    <p><a href="#planner">Plan a benchmark gap</a> with separate fictional inputs.</p>
  </section>;
}

function SierraLeoneEvidence() {
  const effects = sierra.effects;
  const labels = {
    low_baseline_uptake: 'Low baseline vaccination',
    low_predicted_control: 'Low predicted uptake without the package',
    ridge_t_learner: 'Ridge T-learner',
    ridge_dr_learner: 'Ridge DR-learner',
  };
  const interval = (ci: number[]) => ci.map(value => number(value, 1)).join(' to ');
  const row = (label: string, result: {pp: number, ci: number[]}) =>
    [label, number(result.pp, 1), interval(result.ci)];
  return <section className="section snapshot">
    <div className="section-title"><h2>Sierra Leone mobile vaccination trial</h2>
      <a href="https://doi.org/10.7910/DVN/PRXF5Z">Meriggi et al. data · CC0 <span aria-hidden="true">↗</span></a></div>
    <p>Mobile clinics plus community outreach increased adult vaccination. An extra visit had no clear effect. The replication covers {number(sierra.adults)} adults in {sierra.villages} villages.</p>
    <Table caption="Replicated effects on adult vaccination"
      headings={['Assignment contrast', 'Effect (pp)', '95% interval (pp)']}
      rows={[
        row('Mobile package vs control, adult-weighted', effects.mobile_package_adult_weighted),
        row('Mobile package vs control, equal village weights', effects.mobile_package_equal_village),
        row('Door-to-door vs small-group mobile package', effects.mobile_door_to_door_vs_small_group),
        row('Extra visit within door-to-door villages', effects.extra_visit_within_door_to_door_villages),
      ]}/>
    <p>Extra visits were randomized across eligible structures in door-to-door villages ({number(sierra.structureTrialAdults)} adults in {number(sierra.structureTrialUnits)} structures). Both village packages provided mobile clinics.</p>
    <p>Use uniform allocation at {sierra.capacityPct}% expected village capacity for this scenario. Targeting showed no reliable gain in {sierra.holdoutTriplets} held-out triplets. Inference assumes limited spillover.</p>
    <Table caption="Exploratory village allocation vs uniform"
      headings={['Village allocation rule', 'Difference (pp)', 'Conservative joint 95% interval (pp)']}
      rows={Object.entries(sierra.policiesVsUniform).map(([key, result]) => row(labels[key as keyof typeof labels], result))}/>
    <a href="https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/SIERRA_LEONE_RESEARCH.md">Study design and replication <span aria-hidden="true">↗</span></a>
  </section>;
}

function HaryanaEvidence() {
  const decimals = (value: number) => value.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  const bounds = (ci: number[]) => ci.map(decimals).join(' to ');
  const figure = haryana.phcInterval;
  const labels = {
    low_baseline_measles: 'Low baseline measles vaccination',
    low_predicted_control_count: 'Low predicted count without an ambassador',
    ridge_t_learner: 'Learned village benefit score',
  };
  return <section className="section snapshot">
    <div className="section-title"><h2>Haryana immunization trial</h2>
      <a href="https://zenodo.org/records/11392582">Banerjee et al. data · CC BY 4.0 <span aria-hidden="true">↗</span></a></div>
    <p>Ambassador villages recorded more measles vaccinations, but the primary health center interval includes zero. The Figure 4 replication covers {number(haryana.villages)} villages and {number(haryana.villageMonths)} village-months. The pure-control mean was {decimals(haryana.controlMean)} vaccinations per village-month.</p>
    <Table caption="Information-hub assignment sensitivity" headings={['Analysis', 'Effect per village-month', '95% interval']}
      rows={[
        ['Published sub-center clustering', decimals(haryana.subCenterInterval.estimate), bounds(haryana.subCenterInterval.ci)],
        ['Primary health center clustering', decimals(figure.estimate), bounds(figure.ci)],
        ['Equal village-month weights', decimals(haryana.equalVillageMonthWeights.estimate), bounds(haryana.equalVillageMonthWeights.ci)],
      ]}/>
    <p>These are camp-recorded village counts averaged over the other trial assignments.</p>
    <p>Targeting showed no clear gain over uniform ambassador allocation at {haryana.capacityPct}% expected capacity across {haryana.holdoutVillages} held-out villages in {haryana.holdoutPhcs} primary health centers.</p>
    <Table caption="Held-out ambassador allocation vs uniform"
      headings={['Allocation rule', 'Difference per village-month', 'Nominal 95% simultaneous interval']}
      rows={Object.entries(haryana.comparisons).map(([key, result]) =>
        [labels[key as keyof typeof labels], decimals(result.estimate), bounds(result.ci)])}/>
    <p>Simulated interval coverage varied. The estimates assume limited spillover and comparable recording across villages.</p>
    <a href="https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/HARYANA_RESEARCH.md">Study methods and uncertainty <span aria-hidden="true">↗</span></a>
  </section>;
}
createRoot(document.getElementById('root')!).render(<App/>);
