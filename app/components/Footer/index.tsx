import * as React from 'react';
import useVersion from '../../hooks/useVersion';

import './footer.less';

import logo from '../../assets/images/logo_header.svg';

const Header: React.FC = () => {
  const version = useVersion();

  return (
    <footer>
      <div className="footer-container">
        <img src={logo} className="logo" />
        <div className="links">
          <span className="item">
            FIND © 2021 -{' '}
            <a
              href="https://www.finddx.org/wp-content/uploads/2018/05/FIND-Privacy-Policy-on-Personal-Data-use-2018-.pdf"
              target="_blank"
            >
              Privacy policy
            </a>{' '}
          </span>

          <a
            className="item"
            href="https://www.finddx.org/disclaimer/"
            target="_blank"
          >
            | Disclaimer
          </a>
          <span className="item">
            {version && ` | Simulator Version: v${version}`}
          </span>
        </div>
      </div>
    </footer>
  );
};

export default Header;
