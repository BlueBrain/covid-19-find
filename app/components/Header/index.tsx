import * as React from 'react';

import './Header.less';

const logo = require('../../assets/images/logo_header.svg');

const Header: React.FC = () => {
  return (
    <header>
      <div className="header-container">
        <a href="https://www.finddx.org/">
          <img src={logo} className="logo" />
        </a>
      </div>
    </header>
  );
};

export default Header;
