import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown } from 'react-icons/io';
import useFormInput from '../../hooks/useFormInput';

import './country-selector.less';

export type CountrySelectorResponse = {
  countryCode: string;
  population: number | null;
  hospitalBeds: number | null;
  highContactPopulation: number | null;
  urbanPopulationInDegradedHousingProportion: number | null;
  urbanPopulationProportion: number | null;
  hospitalStaffPerBed: number | null;
  hospitalEmployment: number | null;
};

const CountrySelector: React.FC<{
  countries: any[];
  onSubmit?: (value: CountrySelectorResponse) => void;
  onClickSelectCountry: (country: any) => void;
  countryInfo: CountrySelectorResponse;
}> = ({ countries, onSubmit, countryInfo = {}, onClickSelectCountry }) => {
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
  const urbanPopulationInDegradedHousingProportion = useFormInput(
    countryInfo.urbanPopulationInDegradedHousingProportion,
    'Enter... [1 - 100]',
    true,
  );
  const hospitalBeds = useFormInput(countryInfo.hospitalBeds, null, true);
  const hospitalStaffPerBed = useFormInput(
    countryInfo.hospitalStaffPerBed,
    null,
    true,
  );
  const highContactPopulation = useFormInput(
    countryInfo.highContactPopulation,
    null,
    true,
  );
  const [showCountries, setShowCountries] = React.useState(false);
  const [country, setCountry] = React.useState({
    name: '',
    countryCode: '',
  });

  const selectCountry = selectedCountry => {
    const countryId = markSelectedCountry(selectedCountry);
    onClickSelectCountry(countryId);
  };

  const markSelectedCountry = selectedCountry => {
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
    return countryId;
  };

  React.useEffect(() => {
    const defaultCountry = countries.find(
      country => country.countryCode === countryInfo.countryCode,
    );
    if (defaultCountry) {
      markSelectedCountry(defaultCountry);
    }
  }, [countryInfo.countryCode, countries]);

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit &&
      onSubmit({
        countryCode: country.countryCode,
        population: population.value,
        hospitalEmployment: hospitalEmployment.value,
        hospitalBeds: hospitalBeds.value,
        hospitalStaffPerBed: hospitalStaffPerBed.value,
        highContactPopulation: highContactPopulation.value,
        urbanPopulationProportion: urbanPopulationProportion.value,
        urbanPopulationInDegradedHousingProportion:
          urbanPopulationInDegradedHousingProportion.value,
      });

    if (e.target.checkValidity()) {
      document.querySelector('#tests-form')?.scrollIntoView({
        behavior: 'smooth',
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} id="country-select-form">
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
              <input {...urbanPopulationProportion} required />
              <label>
                Total hospital beds
                <br />
                (private and public)
              </label>
              <input {...hospitalBeds} required />
              <label>
                Estimated Staff
                <br />
                per hospital bed
              </label>
              <input {...hospitalStaffPerBed} required />
            </div>
            <div className="form-column">
              <label>Population size</label>
              <input {...population} required />
              <label>
                % urban population in
                <br />
                degraded housing
              </label>
              <input {...urbanPopulationInDegradedHousingProportion} required />
              <label>
                population high
                <br />
                contact occupations
              </label>
              <input {...highContactPopulation} required />
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
