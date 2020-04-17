import * as React from 'react';

const useWindowWidth = () => {
  const isClient = typeof window === 'object';

  const getWidth = () => {
    return {
      width: isClient ? window.innerWidth : undefined,
    };
  };

  const [width, setWidth] = React.useState(getWidth);

  React.useEffect(() => {
    if (!isClient) {
      return null;
    }

    const handleResize = () => {
      setWidth(getWidth());
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return width;
};

export default useWindowWidth;
