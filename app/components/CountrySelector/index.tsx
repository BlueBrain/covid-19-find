import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown, IoIosInformationCircleOutline } from 'react-icons/io';
import useFormInput from '../../hooks/useFormInput';
import ReactTooltip from 'react-tooltip';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

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
  loading: boolean;
}> = ({
  countries,
  onSubmit,
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
    e.target.dataset.dirty = true;
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
  };

  return (
    <form id="country-select-form" onSubmit={handleSubmit}>
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
              <input
                {...urbanPopulationProportion}
                required
                min="0"
                max="100"
                type="number"
              />
              <label>
                Total hospital beds
                <br />
                (private and public)
              </label>
              <input {...hospitalBeds} required min="0" type="number" />
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
                  Europe the average is approximately 4. In other countries it
                  may be higher or lower than this number.
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
              <label>
                % urban population in
                <br />
                degraded housing
              </label>
              <input
                {...urbanPopulationInDegradedHousingProportion}
                required
                min="0"
                max="100"
                type="number"
              />
              <a data-tip data-for="highContactPopulation-tooltip">
                <label>
                  population high
                  <br />
                  contact occupations <IoIosInformationCircleOutline />
                </label>
              </a>
              <ReactTooltip id="highContactPopulation-tooltip">
                <p>
                  This number represents the % of the population whose
                  occupation requires an unavoidably high level of contact with
                  other people (even in quarantine conditions). Examples include
                  workers in essential shops, markets, factories, public
                  transport and delivery services, doctors and dentists etc.
                  Hospital staff are excluded (the number of hospital staff is
                  calculated from the number of hospital beds)
                </p>
              </ReactTooltip>
              <input
                {...highContactPopulation}
                required
                min="0"
                type="number"
              />
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
      <div className="triangle">
        <div className={`loader ${loading ? 'loading' : ''}`}>
          <FontAwesomeIcon icon={faSpinner} pulse />
        </div>
      </div>
    </form>
  );
};

export default CountrySelector;
