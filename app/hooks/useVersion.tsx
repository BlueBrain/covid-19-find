import * as React from 'react';
import packageJson from '../../package.json';

const useVersion = () => {
  return packageJson.version || null;
};

export default useVersion;
