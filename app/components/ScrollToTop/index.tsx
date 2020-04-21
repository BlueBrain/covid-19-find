import * as React from 'react';
import { IoIosArrowUp } from 'react-icons/io';
import useWindowWidth from '../../hooks/useWindowWidth';

import './scroll-to-top.less';

const ScrollToTop: React.FC<{ showAtPercentageHeight?: number }> = ({
  showAtPercentageHeight = 20,
}) => {
  const [visible, setVisible] = React.useState(false);
  const screenWidth = useWindowWidth();
  const isMobile = screenWidth.width < 400;

  React.useEffect(() => {
    const scrollEvent = () => {
      setVisible(
        window.scrollY / document.body.clientHeight >
          showAtPercentageHeight / 100,
      );
    };
    window.addEventListener('scroll', scrollEvent);
    return () => {
      window.removeEventListener('scroll', scrollEvent);
    };
  }, []);

  const scrollToTop = () => {
    document.body.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <button
      title="Back to top"
      className={`scroll-to-top ${visible && 'visible'}`}
      onClick={scrollToTop}
    >
      {!isMobile && 'Scroll to Top'} <IoIosArrowUp />
    </button>
  );
};

export default ScrollToTop;
