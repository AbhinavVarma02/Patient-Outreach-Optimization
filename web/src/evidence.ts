export const paper = 'https://pubmed.ncbi.nlm.nih.gov/42834081/';
export const supplement = 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-026-02603-4/MediaObjects/41562_2026_2603_MOESM1_ESM.pdf';
export const osf = 'https://osf.io/mqbux/';
export const studies = [
  {number: 1, id: 'NCT04323137', season: '2020–21', scope: 'Risk disclosure and message framing', population: 'Highest 10% by modeled clinical risk', contrast: 'Three risk disclosure messages versus no study outreach.', status: 'Content trial · Authors report a season-long primary window.'},
  {number: 2, id: 'NCT05009251', season: '2021–22', scope: 'Risk disclosure versus a reminder', population: 'Highest 10% by modeled clinical risk', contrast: 'Risk disclosure, general reminder and passive control. Eligible modalities were used within message arms.', status: 'Content trial · Primary outcome 8 weeks + 1 day after study start.'},
  {number: 3, id: 'NCT05509283', season: '2022–23', scope: 'Outreach in the next risk band', population: '11–20% by modeled clinical risk', contrast: 'Distinct risk band and outcome window limit cross-trial causal interpretation.', status: 'Content trial · Six-week primary window.'},
  {number: 4, id: 'NCT05509270', season: '2022–23', scope: 'Test of communication modalities', population: 'Primary analysis eligible for letter, portal and SMS', contrast: 'Six randomized arms covering five specific modality configurations plus passive control.', status: 'Channel trial · 29-day primary window.'},
] as const;
