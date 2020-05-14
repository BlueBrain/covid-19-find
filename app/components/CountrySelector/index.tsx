import * as React from 'react';
import { SVGMap } from 'react-svg-map';
import Select from 'react-select';
import { IoIosInformationCircleOutline } from 'react-icons/io';
import ReactTooltip from 'react-tooltip';
import World from '@svg-maps/world';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import Color from 'color';

import colors from '../../colors';
import useFormInput from '../../hooks/useFormInput';

import './country-selector.less';

export type CountrySelectorResponse = {
  countryCode: string;
  population: number | null;
  hospitalBeds: number | null;
  workingOutsideHomeProportion: number | null;
  belowPovertyLineProportion: number | null;
  urbanPopulationProportion: number | null;
  hospitalStaffPerBed: number | null;
  hospitalEmployment: number | null;
  activePopulationProportion: number | null;
  over64Proportion: number | null;
};

const CountrySelector: React.FC<{
  countries: any[];
  onSubmit?: (value: CountrySelectorResponse, valid: boolean) => void;
  onChange?: VoidFunction;
  onClickSelectCountry: (country: any) => void;
  countryInfo: CountrySelectorResponse;
  loading: boolean;
}> = ({
  countries,
  onSubmit,
  onChange,
  countryInfo = {},
  onClickSelectCountry,
  loading,
}) => {
  const population = useFormInput(countryInfo.population, null, true);
  const urbanPopulationProportion = useFormInput(
    countryInfo.urbanPopulationProportion,
    'Enter... [1 - 100]',
    true,
  );
  const hospitalEmployment = useFormInput(
    countryInfo.hospitalEmployment,
    null,
    true,
  );
  const belowPovertyLineProportion = useFormInput(
    countryInfo.belowPovertyLineProportion,
    'Enter... [1 - 100]',
    true,
  );
  const hospitalBeds = useFormInput(countryInfo.hospitalBeds, null, true);
  const hospitalStaffPerBed = useFormInput(
    countryInfo.hospitalStaffPerBed,
    null,
    true,
  );
  const workingOutsideHomeProportion = useFormInput(
    countryInfo.workingOutsideHomeProportion,
    'Enter... [1 - 100]',
    true,
  );
  const activePopulationProportion = useFormInput(
    countryInfo.activePopulationProportion,
    'Enter... [1 - 100]',
    true,
  );
  const over64Proportion = useFormInput(
    countryInfo.over64Proportion,
    'Enter... [1 - 100]',
    true,
  );

  const selectCountry = ({ value, label }) => {
    onClickSelectCountry(value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit &&
      onSubmit(
        {
          countryCode: countryInfo.countryCode,
          population: population.value,
          hospitalEmployment: hospitalEmployment.value,
          hospitalBeds: hospitalBeds.value,
          hospitalStaffPerBed: hospitalStaffPerBed.value,
          workingOutsideHomeProportion: workingOutsideHomeProportion.value,
          urbanPopulationProportion: urbanPopulationProportion.value,
          belowPovertyLineProportion: belowPovertyLineProportion.value,
          activePopulationProportion: activePopulationProportion.value,
          over64Proportion: over64Proportion.value,
        },
        e.target.checkValidity(),
      );
  };

  const countrySelectOptions = countries.map(country => ({
    value: country.countryCode,
    label: country.name,
  }));

  return (
    <form id="country-select-form" onSubmit={handleSubmit} onChange={onChange}>
      <div className="country-selector">
        <div className="title">
          <div className="number">
            <span>1</span>
          </div>
          <h2 className="underline">
            Enter your <em>Country Information</em>
          </h2>
        </div>
        <div className="container">
          <div className="input">
            <div className="form-column">
              <label>Country name</label>
              <Select
                // @ts-ignore
                theme={theme => ({
                  ...theme,
                  borderRadius: '10px',
                  colors: {
                    ...theme.colors,
                    primary25: Color(colors.turqouise)
                      .alpha(0.25)
                      .toString(),
                    primary: colors.turqouise,
                  },
                })}
                styles={{
                  valueContainer: defaults => ({
                    ...defaults,
                    height: '39px',
                  }),
                  container: defaults => ({
                    ...defaults,
                    margin: '5px 0 10px 0',
                  }),
                }}
                value={countrySelectOptions.filter(
                  ({ value }) => value === countryInfo.countryCode,
                )}
                options={countrySelectOptions}
                onChange={selectCountry}
              />
              <label>Population in urban areas (%)</label>
              <input
                {...urbanPopulationProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <label>
                Total hospital beds
                <br />
                (private and public)
              </label>
              <input {...hospitalBeds} required min="1" type="number" />
              <a data-tip data-for="hospitalBeds-tooltip">
                <label>
                  Estimated Staff
                  <br />
                  per hospital bed <IoIosInformationCircleOutline />
                </label>
              </a>
              <ReactTooltip id="hospitalBeds-tooltip">
                <p>
                  The average number of medical, nursing, administrative,
                  technical and cleaning staff per hospital bed. In the US and
                  Europe the average is approximately 2.5 staff/bed. In other
                  countries, it may be higher or lower than this number.
                </p>
              </ReactTooltip>
              <input
                {...hospitalStaffPerBed}
                required
                min="0"
                step="0.01"
                type="number"
              />
            </div>
            <div className="form-column">
              <label>Population size</label>
              <input {...population} required min="0" type="number" />

              <a data-tip data-for="belowPovertyLineProportion-tooltip">
                <label>
                  Urban population below
                  <br />
                  the poverty line (%) <IoIosInformationCircleOutline />
                </label>
              </a>
              <ReactTooltip id="belowPovertyLineProportion-tooltip">
                <p>
                  The percentage of the urban population living below the
                  poverty line. Many members of this population live in
                  conditions that make it difficult or impossible to comply with
                  social distancing or quarantine regulations.
                </p>
              </ReactTooltip>

              <input
                {...belowPovertyLineProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <a data-tip data-for="workingOutsideHomeProportion-tooltip">
                <label>
                  People working outside the home (%){' '}
                  <IoIosInformationCircleOutline />
                </label>
              </a>
              <ReactTooltip id="workingOutsideHomeProportion-tooltip">
                <p>
                  The percentage of the population whose occupation requires a
                  high level of contact with other people (even in quarantine
                  conditions), e.g. workers in essential shops, markets,
                  factories, public transport and delivery services, doctors and
                  dentists. Hospital staff are excluded (the number of hospital
                  staff is calculated from the number of hospital beds for the
                  country).
                </p>
              </ReactTooltip>
              <input
                {...workingOutsideHomeProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <a data-tip data-for="activePopulationProportion-tooltip">
                <label>
                  Active population (%) <IoIosInformationCircleOutline />
                </label>
              </a>
              <ReactTooltip id="activePopulationProportion-tooltip">
                <p>
                  The percentage of the population with the capability to engage
                  in economic activity. As a default, we use the percentage of
                  the population aged between 15 and 64 years.
                </p>
              </ReactTooltip>
              <input
                {...activePopulationProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <label>Population aged > 64 years (%)</label>
              <input
                {...over64Proportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
            </div>
          </div>
          <div className="world">
            <SVGMap map={World} />
            <button className="action" type="submit">
              Enter
            </button>
          </div>
        </div>
      </div>
      <div className="triangle">
        <div className={`loader ${loading ? 'loading' : ''}`}>
          <FontAwesomeIcon icon={faSpinner} pulse />
        </div>
      </div>
    </form>
  );
};

export default CountrySelector;
