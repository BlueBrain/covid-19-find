import * as React from 'react';
import Select from 'react-select';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import Color from 'color';

import colors from '../../colors';
import useFormInput from '../../hooks/useFormInput';
import WorldMap from '../WorldMap';
import TooltipLabel from '../TooltipLabel';

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
  fatalityReduction: number | null;
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
  const fatalityReduction = useFormInput(
    countryInfo.fatalityReduction,
    null,
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
          fatalityReduction: fatalityReduction.value,
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
              <TooltipLabel
                label={
                  <>
                    Estimated Staff
                    <br />
                    per hospital bed
                  </>
                }
                tooltipKey="hospitalBeds"
              />
              <input
                {...hospitalStaffPerBed}
                required
                min="0"
                step="0.01"
                type="number"
              />
              <TooltipLabel
                label={
                  <>
                    Est. Reduction
                    <br />
                    in fatality rate (%)
                  </>
                }
                tooltipKey="fatalityReduction"
              />
              <input
                {...fatalityReduction}
                required
                min="0"
                max="100"
                step="0.5"
                type="number"
              />
            </div>
            <div className="form-column">
              <label>Population size</label>
              <input {...population} required min="0" type="number" />
              <TooltipLabel
                label={
                  <>
                    Urban population below
                    <br />
                    the poverty line (%)
                  </>
                }
                tooltipKey="belowPovertyLineProportion"
              />
              <input
                {...belowPovertyLineProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <TooltipLabel
                label="People working outside the home (%)"
                tooltipKey="workingOutsideHomeProportion"
              />
              <input
                {...workingOutsideHomeProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <TooltipLabel
                label="Active population (%)"
                tooltipKey="activePopulationProportion"
              />
              <input
                {...activePopulationProportion}
                required
                min="0"
                max="100"
                step="0.01"
                type="number"
              />
              <label>Population aged {'>'} 64 years (%)</label>
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
            <WorldMap countryCode={countryInfo.countryCode} />
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
