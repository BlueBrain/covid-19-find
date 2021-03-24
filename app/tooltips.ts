export default {
  activePopulationProportion: `The percentage of the population with the capability to engage
    in economic activity. As a default, we use the percentage of
    the population aged between 15 and 64 years.`,
  hospitalBeds: `The average number of medical, nursing, administrative,
    technical and cleaning staff per hospital bed. In the US and
    Europe the average is approximately 2.5 staff/bed. In other
    countries, it may be higher or lower than this number.`,
  workingOutsideHomeProportion: `The percentage of the population whose occupation requires a
    high level of contact with other people (even in quarantine
    conditions), e.g. workers in essential shops, markets,
    factories, public transport and delivery services, doctors and
    dentists. Hospital staff are excluded (the number of hospital
    staff is calculated from the number of hospital beds for the
    country).`,
  belowPovertyLineProportion: `The percentage of the urban population living below the
    poverty line. Many members of this population live in
    conditions that make it difficult or impossible to comply with
    social distancing or quarantine regulations.`,
  fatalityReduction:
    'The percentage reduction in the average fatality rate from the start of the epidemic to the current date.',
  addPhase:
    'This allows you to define a new phase of government intervention e.g. a phase in which intervention is more or less stringent than in the previous phase',
  numTestsMitigation:
    'The number of tests performed with the goal of detecting and isolating infected individuals, thereby mitigating the impact of the epidemic',
  testingStrategy: ` This defines the government’s testing strategy. There are currently four options:

    * “no testing” (A scenario where there is no testing of any kind and no patients are isolated.),
    
    * “high contact groups first*: A scenario where testing focuses on people with a high probability of contracting COVID and transmitting it to other people (e.g. essential workers, poor people living in degraded urban areas). Members of these groups are regularly tested, whether or not they have symptoms. 
    
    * “symptomatic first”: A scenario where testing focuses on people with COVID-like symptoms. Unused tests are used to test people with no symptoms.
    
    * “open public testing”: A scenario where tests are administered on a “first come first served” basis. So long as enough tests are available, anyone who requests a test receives it.`,
  importedInfectionsPerDay:
    'The effectiveness of border controls preventing new infections from coming into a country. Border controls are especially important when a country has successfully suppressed community transmission within its own boundaries. ',
  trigger:
    'The value at which the new phase is triggered (e.g. the new phase begins when cases per million is greater than or equal to this value',
  triggerType:
    'The way the government defines the trigger for a change in its current measures (e.g. number of cases per million inhabitants, a rise in the number of cases). “Date” defines the date of an intervention that has already taken place or that is planned for a certain date. The date for “current phase” defines the date on which the current phase of intervention began. ',
  triggerCondition:
    'The way data is compared against the trigger condition e.g. a new phase is triggered when cases per million are greater or equal to (>=) a given value ',
  severity:
    'Stringency is measured on a scale of 0 (no restrictions) to 1 (complete lock down)',
  proportionOfContactsTraced:
    'The effectiveness of border controls preventing new infections from coming into a country. Border controls are especially important when a country has successfully suppressed community transmission within its own boundaries.',
  typeTestsMitigation: `This section describes tests used to detect and isolate infected individuals, preventing them from infecting other people.`,
  confirmationTests:
    'The number of tests performed per day for purposes of patient care. This includes confirmatory testing and tests before patient discharge. ',
  specificity:
    'The probability that an individual with a positive test result is actually infected',
  sensitivity:
    'The proportion of infected individuals the test is able to correctly detect',
  numTestsCare:
    'Tests performed with the goal of managing patients with a positive initial test result. Includes confirmatory testing and tests before patient discharge.',
  typeTestsCare: `The type of test used. Options are:

    * PCR: Polymerase Chain Reaction - the current gold standard. A molecular test providing high sensitivity and specificity. Requires qualified personnel to take swabs. Swabs are analyzed in a lab remote from the site of the test and are subject to delay
    
    * RDT: Rapid diagnostic test - an antibody or antigen based test. Cheaper and faster than PCR but may be less accurate, particularly during the early days of infection `,
  requiredDxTests:
    'The average number of tests performed on a patient from diagnosis to discharge, excluding the initial test used to diagnose the patient.',
  resultsPeriod:
    'The average time (in days) between the first appearance of symptoms and the availability of the test result.',
  fatalityReductionRecent:
    'The percentage reduction in the average fatality rate from the start of the epidemic to the start of the phase',
  livesSaved:
    'This panel shows the impact of increasing or decreasing the current number of tests per day, from the start of the current period until the end of the simulation. ',

  'Testing for Mitigation':
    'This section describes tests used to detect and isolate infected individuals, preventing them from infecting other people',
  'Testing for Care':
    'This section describes tests used for the care of patients who have already been diagnosed with COVID. These include tests used to confirm the initial diagnosis, and tests used to verify whether a patient is still infectious, before discharge from hospital.',
  'Samples Required for Serological Studies':
    'The number of samples required to accurately estimate the number of people carrying antibodies to the virus in a given population comprising a certain number of subgroups (e.g. people belonging to a specific age group, people living in a specific city or region, people with a specific socio-economic status).',
  reffGraph:
    ' The estimated value of the Effective Reproductive Number (Reff) for the epidemic on a given day. This is the mean number of new infections, caused by a single primary case of COVID, over the duration of the infection. The value of Reff depends on the effectiveness of government intervention and on the biology of the disease. New strains of COVID may have higher values of Reff.',
  prevalanceGraph:
    ' The estimated percentage of the population that is currently infected by COVID or that has been infected in the past.',
  livesSavedGraph:
    ' This graph shows the estimated number of lives that could be saved with different levels of testing. 1x on the horizontal axis corresponds to the current level of testing. 2x corresponds to twice the current level of testing. 3x corresponds to three times the current level of testing.',
};
