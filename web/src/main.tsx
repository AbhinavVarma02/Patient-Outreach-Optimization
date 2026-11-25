import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { bands, comparePolicies, pilotDesign, plan } from './math';
import { osf, paper, studies, supplement } from './evidence';
import haryana from './haryana.json';
import './style.css';

const views = {overview: 'Overview', targeting: 'Patient Targeting', planner: 'Outreach Planner',
  pilot: 'Pilot Designer', evidence: 'Evidence & Methods'} as const;
type View = keyof typeof views;
const readView = () => Object.hasOwn(views, location.hash.slice(1)) ? location.hash.slice(1) as View : 'overview';
const number = (value: number, digits = 0) => value.toLocaleString('en-US', {maximumFractionDigits: digits});
const money = (value: number) => value.toLocaleString('en-US', {style:'currency',currency:'USD'});
const pp = (value: number) => number(value * 100, 2) + ' pp';

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
    <footer><div className="foot"><span>Patient Outreach Optimization</span><span>Independent research demo · No patient data</span><a href="#evidence">Sources and limits <span aria-hidden="true">↗</span></a></div></footer>
  </>;
}

function Overview() {
  return <>
    <section className="hero">
      <div className="hero-copy"><p className="eyebrow"><span className="dot"/> Preventive care research</p>
        <h1>Which outreach strategy is worth testing?</h1>
        <p>Compare ways to prioritize outreach, estimate channel costs, and size a randomized pilot. Start with evidence from immunization trials.</p>
        <div className="hero-actions"><a href="#targeting" className="button">Explore targeting <Icon name="arrow"/></a>
          <a href="#evidence" className="hero-link">Read the evidence <span aria-hidden="true">↗</span></a></div>
      </div>
      <figure className="hero-figure">
        <figcaption><span>ILLUSTRATIVE SCENARIO</span><strong>Risk and benefit can diverge</strong></figcaption>
        <svg className="hero-chart" viewBox="0 0 410 210" role="img" aria-label="A fictional bar chart. Elevated-risk patients have the largest outreach effect at 4.1 percentage points. The highest-risk group has a 1.2-point effect.">
          <path className="plot-grid" d="M41 18H389M41 49H389M41 80H389M41 111H389M41 142H389M41 173H389"/>
          <g className="hero-axis" textAnchor="end"><text x="32" y="22">5</text><text x="32" y="53">4</text><text x="32" y="84">3</text><text x="32" y="115">2</text><text x="32" y="146">1</text><text x="32" y="177">0</text></g>
          <rect x="64" y="105" width="66" height="68" rx="3" className="muted-bar"/>
          <rect x="182" y="46" width="66" height="127" rx="3" className="bright-bar"/>
          <rect x="300" y="136" width="66" height="37" rx="3" className="muted-bar"/>
          <g className="hero-axis" textAnchor="middle"><text x="97" y="194">Moderate</text><text x="215" y="194">Elevated</text><text x="333" y="194">Highest</text></g>
          <g className="hero-values" textAnchor="middle"><text x="97" y="97">+2.2</text><text x="215" y="37">+4.1</text><text x="333" y="128">+1.2</text></g>
        </svg>
        <p>Assumed vaccination effect by clinical risk band (pp)</p>
      </figure>
    </section>
    <aside className="evidence-strip"><span className="dot"/><p><strong>Limited research demonstration.</strong> Review an independent village-level analysis from Haryana and published Geisinger trial evidence. Interactive outputs use fictional assumptions.</p><a href="#evidence">Evidence status <span aria-hidden="true">↗</span></a></aside>
    <section className="section"><div className="section-title"><h2>From evidence to a pilot</h2><p>Work through a fictional outreach decision.</p></div>
      <div className="workflow">
        <Workflow view="targeting" verb="Compare allocation rules" detail="See how risk and estimated benefit change who receives the same number of contacts."/>
        <Workflow view="planner" verb="Estimate channel costs" detail="Compare the contacts and incremental vaccinations each channel could deliver under your assumptions."/>
        <Workflow view="pilot" verb="Size the experiment" detail="Estimate how many participants a randomized comparison would need to detect a policy difference."/>
      </div>
    </section>
    <section className="section snapshot"><div className="section-title"><h2>Trial evidence</h2><a href="#evidence">Explore methods <span aria-hidden="true">↗</span></a></div>
      <div className="snapshot-grid"><div><p className="eyebrow">Content studies</p><h3>Three randomized field trials</h3><p>Geisinger tested risk disclosure, message framing and reminder comparisons across three flu seasons.</p><a href={paper}>Published article <span aria-hidden="true">↗</span></a></div>
      <div><p className="eyebrow">Channel study</p><h3>One randomized modality trial</h3><p>Study 4 tested specific letter, portal and SMS configurations. Eligibility defines which comparisons apply.</p><a href={supplement}>Study 4 supplement <span aria-hidden="true">↗</span></a></div></div>
    </section>
  </>;
}

function Workflow({view, verb, detail}: {view: View; verb: string; detail: string}) {
  return <a className="workflow-item" href={'#' + view}><span className="workflow-label">{views[view]} <Icon name="arrow"/></span>
    <strong>{verb}</strong><span>{detail}</span></a>;
}

function Page({title, copy, children}: React.PropsWithChildren<{title: string; copy: string}>) {
  return <div className="page"><div className="page-title"><p className="eyebrow">Outreach research workspace</p>
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
  return <Page title="Patient Targeting" copy="Hold capacity constant and see when a rule based on expected outreach benefit changes the allocation.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Fictional inputs</p><h2>Allocation scenario</h2>
      <label className="field"><span>Outreach capacity <output>{capacity}%</output></span>
        <input type="range" min="0" max="100" value={capacity} onChange={e => setCapacity(e.target.valueAsNumber)}/></label>
      <label className="field">Effect pattern<select value={shape} onChange={e => setShape(e.target.value)}>
        <option value="inverted">Benefit peaks at elevated risk</option><option value="monotone">Benefit rises with clinical risk</option><option value="flat">Equal benefit across groups</option>
      </select></label>
      <p className="small">The benefit rule ranks groups by their assumed effects. Its advantage is an illustration of what could happen if those effects were known.</p>
    </aside><section className="output"><p className="eyebrow">Matched capacity · {capacity}%</p><h2>Expected incremental vaccinations</h2>
      <p>Per 1,000 eligible people, compared with no added outreach.</p>
      <svg className="policy-chart" viewBox="0 0 610 177" role="img" aria-label={values.map(([l,v]) => l+' '+number(v*1000,2)).join(', ')}>
        {values.map(([label, value], i) => <g key={label}><text x="0" y={33+54*i}>{label}</text>
          <rect x="163" y={16+54*i} width="350" height="22" rx="4" className="track"/>
          <rect x="163" y={16+54*i} width={350*value/max} height="22" rx="4" className={i === 2 ? 'primary-bar' : 'secondary-bar'}/>
          <text x="532" y={33+54*i}>{number(value*1000,2)}</text></g>)}
      </svg>
      <Table caption="Scenario output" headings={['Allocation rule','Extra vaccinations per 1,000']}
        rows={values.map(([label, value]) => [label, number(value*1000,2)])}/>
      <div className="callout"><strong>{pp(result.benefit-result.uniform)}</strong> modeled gain over uniform outreach at the same capacity. No sampling interval applies to these fixed fictional inputs.</div>
    </section></div>
    <section className="section"><h2>Assumed effects by risk band</h2><Table caption="Fictional population" headings={['Risk band','Share eligible','Effect of outreach']}
      rows={profile.map(band => [band.name, number(band.share*100)+'%', pp(band.effect)])}/></section>
    <div className="page-next"><a className="text-link" href="#planner">Next: compare channel costs <Icon name="arrow"/></a> <a href="#evidence">Evidence and limits</a></div>
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
  return <Page title="Outreach Planner" copy="Compare single-channel strategies under the same population, contact capacity and spending limit.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Fictional inputs</p><h2>Planning assumptions</h2>
      <Field label="Eligible population" value={population} min={1} max={10000000} onChange={pop}/>
      <Field label="Maximum contacts (%)" value={capacity} min={0} max={100} unit="%" onChange={cap}/>
      <Field label="Budget (USD)" value={budget} min={0} max={10000000} step={0.01} unit="USD" onChange={bud}/>
      <label className="field">Channel to edit<select value={index} onChange={e => select(Number(e.target.value))}>{options.map((item,i) => <option key={item.name} value={i}>{item.name}</option>)}</select></label>
      <Field label="Cost per contact (USD)" value={option.cents/100} min={0} max={100} step={0.01} unit="USD" onChange={value => update({cents:Math.round(value*100)})}/>
      <Field label="Channel eligibility (%)" value={option.eligible*100} min={0} max={100} unit="%" onChange={value => update({eligible:value/100})}/>
      <Field label="Effect (pp)" value={+(option.effect*100).toFixed(4)} min={-20} max={20} step={0.1} unit="pp" onChange={value => update({effect:value/100})}/>
      <Field label="Sensitivity ± (pp)" value={+(option.spread*100).toFixed(4)} min={0} max={20} step={0.1} unit="pp" onChange={value => update({spread:value/100})}/>
      <button className="secondary-button" onClick={() => {pop(10000);cap(35);bud(1800);setOptions(defaults);select(0);}}>Reset assumptions</button>
    </aside><section className="output"><p className="eyebrow">Scenario estimate</p><h2>Channel comparison</h2>
      {best && rows ? <>
        <div className="metrics" aria-live="polite"><div><span>Highest modeled yield</span><strong>{best.gain > 0 ? best.name : 'No outreach'}</strong></div>
        <div><span>Extra vaccinations</span><strong>{number(Math.max(0,best.gain),1)}</strong></div>
        <div><span>Scenario spend</span><strong>{money(best.gain > 0 ? best.spend : 0)}</strong></div></div>
        <Table caption="All channels under the same limits" headings={['Channel','Contacts','Spend','Extra vaccinations','Sensitivity range','Cost per additional vaccination']}
          rows={rows.map(row => [row.name, number(row.contacts), money(row.spend), number(row.gain,1),
            number(row.low,1)+' to '+number(row.high,1), row.perGain === null ? '—' : money(row.perGain)])}/>
        <p className="small">The sensitivity range varies the assumed effect by the entered margin. Each strategy uses whole contacts and a single channel. Near-zero gains can make cost per additional vaccination unstable.</p>
      </> : <p role="status" className="callout">Enter a valid population, capacity, budget and channel assumptions to calculate results.</p>}
      <div className="callout"><strong>Published comparison.</strong> Study 4 evaluated assigned modality bundles within defined eligibility groups. <a href={supplement}>Read its study design</a>.</div>
    </section></div>
    <div className="page-next"><a className="text-link" href="#pilot">Next: size the pilot <Icon name="arrow"/></a></div>
  </Page>;
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
    ['concentration','Effect concentration (×)',1,10,0.1,'×'],
    ['capture','Ranking quality (%)',0,100,1,'%'],
    ['allocation','Assigned to targeting (%)',5,95,1,'%'],
    ['target','Target power (%)',50,99,1,'%'],
    ['alpha','Significance level (%)',0.1,25,0.1,'%'],
    ['attrition','Expected attrition (%)',0,80,1,'%'],
    ['clusterSize','Mean cluster size',1,10000,0.1,''],
    ['icc','Intracluster correlation (%)',0,95,1,'%'],
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
  return <Page title="Pilot Designer" copy="Size a prospective randomized comparison of a frozen targeting rule against uniform outreach at equal capacity.">
    <div className="workbench"><aside className="controls"><p className="eyebrow">Randomized policy trial</p><h2>Design assumptions</h2>
      {fields.slice(0,8).map(([key,label,min,max,step,unit]) => <Field key={key} {...{label,min,max,step,unit}} value={d[key]}
        onChange={value => set({...d,[key]:value})}/>)}
      <details><summary>Significance, attrition and clustering</summary>{fields.slice(8).map(([key,label,min,max,step,unit]) =>
        <Field key={key} {...{label,min,max,step,unit}} value={d[key]} onChange={value => set({...d,[key]:value})}/>)}</details>
      <button className="secondary-button" onClick={() => set(pilotDefaults)}>Reset assumptions</button>
    </aside><section className="output"><p className="eyebrow">Analytic projection</p><h2>Power to detect the policy difference</h2>
      {result ? <>
        <div className="metrics" aria-live="polite"><div><span>Required enrollment</span><strong>{result.required === null ? 'No finite N' : result.required >= 1e9 ? 'Over 1 billion' : number(result.required)}</strong></div>
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
        <p className="small">The dashed line marks target power. Total enrollment includes both strategies and assumed attrition. The minimum detectable difference holds outcome variance fixed.</p>
        <Table caption="Projected power by enrollment" headings={['Enrollment','Estimated power']} rows={[0.5,1,1.5,2].map(multiplier => {
          const n = Math.max(2,Math.round(d.enrollment*multiplier)); return [number(n),number(result.power(n)*100,1)+'%'];
        }).filter((row,i,all) => i === 0 || row[0] !== all[i-1][0])}/>
        <div className="callout"><strong>{pp(result.gain)}</strong> assumed gain over uniform outreach. Ranking quality is the fraction of the perfect-ranking gain retained by the frozen policy.</div>
      </> : <p role="status" className="callout">{error}</p>}
    </section></div>
  </Page>;
}

function Evidence() {
  return <Page title="Evidence & Methods" copy="Trace the trial design behind each workflow and see which analyses remain pending.">
    <div className="evidence-strip"><span className="dot"/><p><strong>Current status.</strong> Haryana contributes independent community-level analysis. The Geisinger summaries report authors’ published findings while reuse permission remains open.</p></div>
    <HaryanaEvidence/>
    <section className="section"><div className="section-title"><h2>Trial explorer</h2><a href={paper}>Published article <span aria-hidden="true">↗</span></a></div>
      <div className="study-grid">{studies.map(study => <article className="study" key={study.id}><p className="eyebrow">Study {study.number} · {study.season}</p>
        <h3>{study.scope}</h3><p><strong>{study.population}</strong></p><p>{study.contrast}</p><p className="small">{study.status}</p>
        <a href={'https://clinicaltrials.gov/study/'+study.id}>{study.id} <span aria-hidden="true">↗</span></a>
      </article>)}</div>
    </section>
    <section className="section snapshot"><div className="section-title"><h2>One published channel comparison</h2><a href={supplement}>Supplement, section 7.2 <span aria-hidden="true">↗</span></a></div>
      <p>Among participants eligible for letter, portal and SMS, the authors reported a 2.5 percentage-point increase in vaccination for assignment to letter only versus passive control (95% CI 0.9 to 4.0 pp). The primary window was 29 days. The comparison does not establish that letters outperform every other tested bundle.</p>
    </section>
    <section className="section methods"><h2>Methods and limits</h2>
      <details open><summary>Assignment and outcomes</summary><p>Intent-to-treat contrasts compare assigned outreach. Delivery, receipt and engagement are separate. Different enrollment rules, flu seasons and outcome windows constrain comparisons across trials.</p></details>
      <details><summary>Scenario and power assumptions</summary><p>Targeting uses fictional, fixed group effects. The planner evaluates alternative single-channel strategies with user-entered assumptions. The pilot uses a normal approximation and a mean-cluster-size design effect. It assumes a frozen policy, stable outcome rates, and noninformative attrition.</p></details>
      <details><summary>Data provenance and rights</summary><p>The <a href={osf}>OSF catalog</a> is public and records no dataset license. The application does not load trial records, accept patient identifiers or store scenario inputs. Only theme preference is saved locally.</p></details>
    </section>
  </Page>;
}

function HaryanaEvidence() {
  const decimals = (value: number) => value.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  const bounds = (ci: number[]) => ci.map(decimals).join(' to ');
  const figure = haryana.phcInterval;
  const labels = {
    low_baseline_measles: 'Low baseline measles vaccination',
    low_predicted_control_count: 'Low predicted vaccination count without an ambassador',
    ridge_t_learner: 'Learned village benefit score',
  };
  return <section className="section snapshot">
    <div className="section-title"><h2>Haryana immunization trial</h2>
      <a href="https://zenodo.org/records/11392582">Banerjee et al. data · CC BY 4.0 <span aria-hidden="true">↗</span></a></div>
    <p>We reproduced Figure 4 across {number(haryana.villages)} villages and {number(haryana.villageMonths)} village-months.
      The population-weighted estimate for assigning information-hub ambassadors was {decimals(figure.estimate)} additional
      recorded measles vaccinations per village-month. The pure-control mean was {decimals(haryana.controlMean)}.</p>
    <Table caption="Information-hub assignment sensitivity" headings={['Analysis', 'Effect per village-month', '95% interval']}
      rows={[
        ['Published sub-center clustering', decimals(haryana.subCenterInterval.estimate), bounds(haryana.subCenterInterval.ci)],
        ['Primary health center clustering', decimals(figure.estimate), bounds(figure.ci)],
        ['Equal village-month weights', decimals(haryana.equalVillageMonthWeights.estimate), bounds(haryana.equalVillageMonthWeights.ci)],
      ]}/>
    <p>Primary health center clustering widened the interval to include zero. The estimate averages over the trial’s other
      assigned interventions. It describes a community outcome at immunization camps.</p>
    <p>In an exploratory holdout of {haryana.holdoutVillages} villages across {haryana.holdoutPhcs} primary health centers,
      targeted rules showed no clear improvement over uniform ambassador allocation at {haryana.capacityPct}% expected capacity.</p>
    <Table caption="Held-out village policy comparisons against uniform"
      headings={['Allocation rule', 'Difference per village-month', 'Nominal 95% simultaneous interval']}
      rows={Object.entries(haryana.comparisons).map(([key, result]) =>
        [labels[key as keyof typeof labels], decimals(result.estimate), bounds(result.ci)])}/>
    <p>Simulation found uneven interval coverage at this sample size. Interpretation also depends on limited spillover
      between villages and comparable outcome recording. The patient outreach calculators use separate fictional inputs.</p>
    <a href="https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/HARYANA_RESEARCH.md">Analysis, uncertainty and reproduction <span aria-hidden="true">↗</span></a>
  </section>;
}
createRoot(document.getElementById('root')!).render(<App/>);
