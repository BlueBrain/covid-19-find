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
    'the percentage reduction in the average fatality rate from the start of the epidemic to the current date',
  addPhase:
    ' This allows you to define a new phase of government intervention e.g. a phase in which intervention is more or less stringent than in the previous phase',
  numTestsMitigation:
    'tests performed with the goal of detecting and isolating infected individuals, thereby mitigating the impact of the epidemic',
  testingStrategy: ` This defines the government’s testing strategy. There are currently four options:

    * “no testing” (this is used as a counterfactual to show the impact of testing),
    
    * “high contact groups first*: in this strategy, members of social groups with high numbers of social contacts are tested first, whether or not individuals show symptoms. Any remaining tests are used to test members of other groups
    
    * “symptomatic first”: in this strategy, individuals showing symptoms are tested first. Any remaining tests are used to test asymptomatic individuals
    
    * “open public testing”: anyone requesting a test is tested, on a first come, first served basis. `,
  importedInfectionsPerDay:
    'The estimated number of infections brought into the country from outside (e.g. by tourists, returning tourists, business travellers, immigrants etc.). Imported infections can restart the epidemic even when it has been completely eliminated ',
  trigger:
    'defines the value at which the new phase is triggered (e.g. the new phase begins when cases per million is greater than or equal to this value',
  triggerType:
    'describes the way the government defines the trigger for a change in its current measures (e.g. number of cases per million inhabitants, a rise in the number of cases). “Date” defines the date of an intervention that has already taken place or that is planned for a certain date. The date for “current phase” defines the date on which the current phase of intervention began. ',
  triggerCondition:
    'defines the way data is compared against the trigger condition e.g. a new phase is triggered when cases per million are greater or equal to (>=) a given value ',
  severity:
    'This defines the severity of government intervention in a given phase. The value is given on a scale of 0 to 1 where 0 means absolutely no restrictive measures, and 1 means total lockdown.',
  proportionOfContactsTraced:
    'This defines the % of an infected person’s close social contacts who are traced, tested and placed in isolation (if positive). If no test and trace system is in place the correct value for this variable is 0.',
  typeTestsMitigation: `this is the type of test used. Options are:

    * PCR: Polymerase Chain Reaction - the current gold standard. A molecular test providing high sensitivity and specificity. Requires qualified personnel to take swabs. Swabs are analyzed in a lab remote from the site of the test and are subject to delay
    
    * RDT: Rapid diagnostic test - an antibody or antigen based test. Cheaper and faster than PCR but may be less accurate, particularly during the early days of infection`,
  confirmationTests:
    'the number of tests performed per day for purposes of patient care. This includes confirmatory testing and tests before patient discharge. ',
  specificity:
    'the probability that an individual with a positive test result is actually infected',
  sensitivity:
    'the proportion of infected individuals the test is able to correctly detect',
  numTestsCare:
    'tests performed with the goal of managing patients with a positive initial test result. Includes confirmatory testing and tests before patient discharge.',
  typeTestsCare: `this is the type of test used. Options are:

    * PCR: Polymerase Chain Reaction - the current gold standard. A molecular test providing high sensitivity and specificity. Requires qualified personnel to take swabs. Swabs are analyzed in a lab remote from the site of the test and are subject to delay
    
    * RDT: Rapid diagnostic test - an antibody or antigen based test. Cheaper and faster than PCR but may be less accurate, particularly during the early days of infection `,
  requiredDxTests:
    'the average number of tests performed on a patient from diagnosis to discharge, excluding the initial test used to diagnose the patient.',
  resultPeriod:
    'the average number of days between the first appearance of symptoms and the return of results from testing. ',
  fatalityReductionRecent:
    ' the percentage reduction in the average fatality rate from the start of the epidemic to the start of the phase',
  livesSaved:
    'This panel shows the impact of increasing or decreasing the current number of tests per day, from the start of the current period until the end of the simulation. ',
};
