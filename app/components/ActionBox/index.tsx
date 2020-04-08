import * as React from 'react';
import useAPI from '../../hooks/useAPI';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';
import { IoIosArrowDown } from 'react-icons/io';

import './action-box.less';

const ActionBox: React.FC = () => {
  const [country, setCountry] = React.useState({
    name: '',
    countryCode: '',
  });
  const [showCountries, setShowCountries] = React.useState(false);
  const [countries, setCountries] = React.useState([]);
  const api = useAPI();

  React.useEffect(() => {
    api
      .countries()
      .then(response => setCountries(response.countries))
      .catch(console.error);
  }, []);

  const selectCountry = selectedCountry => {
    if (country.countryCode !== '') {
      const previousCountry = document.getElementById(
        country.countryCode.toLowerCase(),
      );
      previousCountry.removeAttribute('class');
    }

    const countryId = selectedCountry.countryCode;
    const area = document.getElementById(countryId.toLowerCase());

    if (area) {
      area.setAttribute('class', 'selected');
    }

    setCountry(selectedCountry);
    setShowCountries(false);
  };

  const onClickSubmit = () => {
    console.log('country', country);
  };

  return (
    <>
      <section>
        <div className="action-box">
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
                  <label>
                    % population in cities of <br />1 mio
                  </label>
                  <input
                    placeholder="Enter... (0%-100%)"
                    name="population-cities"
                  />
                  <label>Estimated total hospital employment</label>
                  <input
                    placeholder="Enter... [0-100]"
                    name="population-cities"
                  />
                </div>
                <div className="form-column">
                  <label>Population size</label>
                  <input
                    placeholder="Enter... [0-100]"
                    name="population-size"
                  />
                  <label>% population in degraded housing</label>
                  <input
                    placeholder="Enter... (0%-100%)"
                    name="degraded-housing"
                  />
                  <label>% population high risk occupations</label>
                  <input
                    placeholder="Enter... (0%-100%)"
                    name="high-risk-occupations"
                  />
                </div>
                <div className="form-column">
                  <label>% population age +65 years</label>
                  <input placeholder="Enter... (0%-100%)" name="over-65" />
                  <label>% population remote/isolated areas</label>
                  <input placeholder="Enter... (0%-100%)" name="remote-areas" />
                </div>
              </form>
            </div>
            <div className="world">
              <SVGMap map={World} />
              <button className="action" onClick={onClickSubmit}>
                Submit
              </button>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="action-box primary">
          <div className="title">
            <div className="number">
              <span>2</span>
            </div>
            <h2 className="underline">
              Check out these <em>Cool Graphs</em>
            </h2>
          </div>
          <div className="container"></div>
        </div>
      </section>
    </>
  );
};

export default ActionBox;
