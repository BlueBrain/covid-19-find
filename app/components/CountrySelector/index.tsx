import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown } from 'react-icons/io';

import './country-selector.less';
import useFormInput from '../../hooks/useFormInput';
import { CountryResponse } from '../../API';

const CountrySelector: React.FC<{
  countries: any[];
  onSubmit?: (value: CountryResponse) => void;
  onClickSelectCountry: (country: any) => void;
  countryInfo: CountryResponse;
  defaultCountryCode: string;
}> = ({
  countries,
  onSubmit,
  countryInfo = {},
  onClickSelectCountry,
  defaultCountryCode,
}) => {
  const population = useFormInput(countryInfo.population, 'Enter...');
  const over65Proportion = useFormInput(countryInfo.over65Proportion);
  const remoteAreasPopulationProportion = useFormInput(
    countryInfo.remoteAreasPopulationProportion,
  );
  const urbanPopulationInDegradedHousingProportion = useFormInput(
    countryInfo.urbanPopulationInDegradedHousingProportion,
  );
  const urbanPopulationProportion = useFormInput(
    countryInfo.urbanPopulationProportion,
  );
  const hospitalEmployment = useFormInput(countryInfo.hospitalEmployment);
  const hospitalBeds = useFormInput(countryInfo.hospitalBeds);
  const highContactPopulation = useFormInput(countryInfo.highContactPopulation);
  const [showCountries, setShowCountries] = React.useState(false);
  const [country, setCountry] = React.useState({
    name: '',
    countryCode: '',
  });

  React.useEffect(() => {
    countryInfo.population && population.changeValue(countryInfo.population);
    countryInfo.over65Proportion &&
      over65Proportion.changeValue(countryInfo.over65Proportion);
    countryInfo.remoteAreasPopulationProportion &&
      remoteAreasPopulationProportion.changeValue(
        countryInfo.remoteAreasPopulationProportion,
      );
    countryInfo.urbanPopulationInDegradedHousingProportion &&
      urbanPopulationInDegradedHousingProportion.changeValue(
        countryInfo.urbanPopulationInDegradedHousingProportion,
      );
    countryInfo.urbanPopulationProportion &&
      urbanPopulationProportion.changeValue(
        countryInfo.urbanPopulationProportion,
      );
    countryInfo.hospitalEmployment &&
      hospitalEmployment.changeValue(countryInfo.hospitalEmployment);
    countryInfo.hospitalBeds &&
      hospitalBeds.changeValue(countryInfo.hospitalBeds);
    countryInfo.highContactPopulation &&
      highContactPopulation.changeValue(countryInfo.highContactPopulation);
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
        countryCode: country.countryCode,
        population: population.value,
        hospitalEmployment: hospitalEmployment.value,
        hospitalBeds: hospitalBeds.value,
        highContactPopulation: highContactPopulation.value,
        urbanPopulationProportion: urbanPopulationProportion.value,
        remoteAreasPopulationProportion: remoteAreasPopulationProportion.value,
        urbanPopulationInDegradedHousingProportion:
          urbanPopulationInDegradedHousingProportion.value,
        over65Proportion: over65Proportion.value,
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
              <input {...urbanPopulationProportion} required />
              <label>
                Total hospital beds
                <br />
                (private and public)
              </label>
              <input {...hospitalBeds} required />
              <label>
                % population age <br />
                +65 years
              </label>
              <input {...over65Proportion} required />
              <label>
                Estimated Staff
                <br />
                per hospital bed
              </label>
              <input {...hospitalEmployment} required />
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
              <input {...remoteAreasPopulationProportion} required />
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
