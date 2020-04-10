import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown } from 'react-icons/io';

import './country-selector.less';
import useFormInput from '../../hooks/useFormInput';

export type CountryParams = {
  total_pop?: number;
  pop_hospitals?: number;
  pop_high_contact?: number;
  prop_urban?: number;
  prop_isolated?: number;
  degraded?: number;
  ge_65?: number;
  prop_tests_hospitals?: number;
  prop_tests_high_contact?: number;
  prop_tests_rest_of_population?: number;
};

const CountrySelector: React.FC<{
  countries: any[];
  onSubmit?: (value: CountryParams) => void;
  onClickSelectCountry: (country: any) => void;
  countryInfo: CountryParams;
  defaultCountryCode: string;
}> = ({
  countries,
  onSubmit,
  countryInfo = {},
  onClickSelectCountry,
  defaultCountryCode,
}) => {
  const population = useFormInput(countryInfo.total_pop, 'Enter...');
  const over65Percentage = useFormInput(countryInfo.ge_65);
  const remoteAreasPopulationPercentage = useFormInput(
    countryInfo.prop_isolated,
  );
  const urbanPopulationInDegradedHousingPercentage = useFormInput(
    countryInfo.degraded,
  );
  const urbanPopulationPercentage = useFormInput(countryInfo.prop_urban);
  const hospitalEmployment = useFormInput(countryInfo.pop_hospitals);
  const highContactPopulation = useFormInput(countryInfo.pop_high_contact);
  const [showCountries, setShowCountries] = React.useState(false);
  const [country, setCountry] = React.useState({
    name: '',
    countryCode: '',
  });

  React.useEffect(() => {
    countryInfo.total_pop && population.changeValue(countryInfo.total_pop);
    countryInfo.ge_65 && over65Percentage.changeValue(countryInfo.ge_65);
    countryInfo.prop_isolated &&
      remoteAreasPopulationPercentage.changeValue(countryInfo.prop_isolated);
    countryInfo.degraded &&
      urbanPopulationInDegradedHousingPercentage.changeValue(
        countryInfo.degraded,
      );
    countryInfo.prop_urban &&
      urbanPopulationPercentage.changeValue(countryInfo.prop_urban);
    countryInfo.pop_hospitals &&
      hospitalEmployment.changeValue(countryInfo.pop_hospitals);
    countryInfo.pop_high_contact &&
      highContactPopulation.changeValue(countryInfo.pop_high_contact);
  }, [countryInfo]);

  const selectCountry = selectedCountry => {
    if (country.countryCode !== '') {
      const previousCountry = document.getElementById(
        country.countryCode.toLowerCase(),
      );
      previousCountry?.removeAttribute('class');
    }

    const countryId = selectedCountry.countryCode;
    const area = document.getElementById(countryId.toLowerCase());

    if (area) {
      area.setAttribute('class', 'selected');
    }

    setCountry(selectedCountry);
    setShowCountries(false);
    onClickSelectCountry(countryId);
  };

  React.useEffect(() => {
    const defaultCountry = countries.find(
      country => country.countryCode === defaultCountryCode,
    );
    if (defaultCountry) {
      selectCountry(defaultCountry);
    }
  }, [defaultCountryCode, countries]);

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit &&
      onSubmit({
        total_pop: population.value,
        pop_hospitals: hospitalEmployment.value,
        pop_high_contact: highContactPopulation.value,
        prop_urban: urbanPopulationPercentage.value,
        prop_isolated: remoteAreasPopulationPercentage.value,
        degraded: urbanPopulationInDegradedHousingPercentage.value,
        ge_65: over65Percentage.value,
        // TODO we dont have these values???
        // prop_tests_hospitals?: number;
        // prop_tests_high_contact?: number;
        // prop_tests_rest_of_population?: number;
      });
  };

  return (
    <form onSubmit={handleSubmit}>
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
              <div
                className="country-info-select"
                onClick={() => setShowCountries(!showCountries)}
              >
                <span>{country.name || 'Select'}</span>
                {country.name === '' && <IoIosArrowDown />}
              </div>
              {showCountries && (
                <div className="countries-list">
                  {countries.map(country => (
                    <p
                      onClick={() => selectCountry(country)}
                      key={country.countryCode}
                    >
                      {country.name}
                    </p>
                  ))}
                </div>
              )}
              <label>% population in urban areas</label>
              <input {...urbanPopulationPercentage} required />
              <label>
                Total hospital beds
                <br />
                (private and public)
              </label>
              <input {...hospitalEmployment} required />
              <label>
                % population age <br />
                +65 years
              </label>
              <input {...over65Percentage} required />
              <label>
                Estimated Staff
                <br />
                per hospital bed
              </label>
              <input
                // TODO this value doesnt exist yet
                value={4}
                readOnly
              />
            </div>
            <div className="form-column">
              <label>Population size</label>
              <input {...population} required />
              <label>
                % urban population in
                <br />
                degraded housing
              </label>
              <input {...urbanPopulationInDegradedHousingPercentage} required />
              <label>
                % population high
                <br />
                contact occupations
              </label>
              <input {...highContactPopulation} required />
              <label>
                % population
                <br />
                remote/isolated areas
              </label>
              <input {...remoteAreasPopulationPercentage} required />
            </div>
          </div>
          <div className="world">
            <SVGMap map={World} />
            <button className="action" type="submit">
              Submit
            </button>
          </div>
        </div>
      </div>
      <div className="triangle"></div>
    </form>
  );
};

export default CountrySelector;
