import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown } from 'react-icons/io';

import './country-selector.less';

export type CountryInfo = {
  countryCode: string;
  highContactPopulation: number;
  hospitalBeds: number;
  hospitalEmployment: number;
  over65Percentage: number;
  population: number;
  remoteAreasPopulationPercentage: number;
  urbanPopulationInDegradedHousingPercentage: number;
  urbanPopulationPercentage: number;
};

const CountrySelector: React.FC<{
  countries: any[];
  onClickSubmit: (country: any) => void;
  onClickSelectCountry: (country: any) => void;
  countryInfo: CountryInfo | null;
  defaultCountryCode: string;
}> = ({
  countries,
  onClickSubmit,
  countryInfo = {
    population: null,
    over65Percentage: null,
    remoteAreasPopulationPercentage: null,
    urbanPopulationInDegradedHousingPercentage: null,
    urbanPopulationPercentage: null,
    hospitalEmployment: null,
    highContactPopulation: null,
  },
  onClickSelectCountry,
  defaultCountryCode,
}) => {
  const [showCountries, setShowCountries] = React.useState(false);
  const [country, setCountry] = React.useState({
    name: '',
    countryCode: '',
  });

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

  const {
    population,
    over65Percentage,
    remoteAreasPopulationPercentage,
    urbanPopulationInDegradedHousingPercentage,
    urbanPopulationPercentage,
    hospitalEmployment,
    highContactPopulation,
  } = countryInfo;

  return (
    <>
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
            <form className="country-form">
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
                <input
                  value={urbanPopulationPercentage || 'Enter... (0%-100%)'}
                  required
                />
                <label>
                  Total hospital beds
                  <br />
                  (private and public)
                </label>
                <input
                  value={hospitalEmployment || 'Enter... [0-100]'}
                  required
                />
                <label>
                  % population age <br />
                  +65 years
                </label>
                <input
                  value={over65Percentage || 'Enter... (0%-100%)'}
                  required
                />
                <label>
                  Estimated Staff
                  <br />
                  per hospital bed
                </label>
                <input
                  value={hospitalEmployment || 'Enter... [0-100]'}
                  required
                />
              </div>
              <div className="form-column">
                <label>Population size</label>
                <input
                  value={population?.toLocaleString() || 'Enter... [0-100]'}
                  required
                />
                <label>
                  % urban population in
                  <br />
                  degraded housing
                </label>
                <input
                  value={
                    urbanPopulationInDegradedHousingPercentage ||
                    'Enter... (0%-100%)'
                  }
                  required
                />
                <label>
                  % population high
                  <br />
                  contact occupations
                </label>
                <input
                  value={highContactPopulation || 'Enter... (0%-100%)'}
                  required
                />
                <label>
                  % population
                  <br />
                  remote/isolated areas
                </label>
                <input
                  value={
                    remoteAreasPopulationPercentage || 'Enter... (0%-100%)'
                  }
                  required
                />
              </div>
            </form>
          </div>
          <div className="world">
            <SVGMap map={World} />
            <button className="action" onClick={() => onClickSubmit(country)}>
              Submit
            </button>
          </div>
        </div>
      </div>
      <div className="triangle"></div>
    </>
  );
};

export default CountrySelector;
