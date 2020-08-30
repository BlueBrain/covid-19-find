import * as React from 'react';
import World from '@svg-maps/world';
import { SVGMap } from 'react-svg-map';

import './world-map.less';

const WorldMap: React.FC<{ countryCode?: string }> = ({ countryCode }) => {
  React.useEffect(() => {
    if (countryCode) {
      const highlightedCountries = document.querySelectorAll(
        '.svg-map .selected',
      );
      Array.from(highlightedCountries).forEach(element => {
        element.classList.remove('selected');
      });
      const countrySVGID = document.getElementById(countryCode.toLowerCase());
      countrySVGID?.classList.add('selected');
    }
  }, [countryCode]);

  return <SVGMap map={World} />;
};

export default WorldMap;
