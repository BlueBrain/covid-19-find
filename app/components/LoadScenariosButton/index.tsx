import * as React from 'react';
import { ClientSimulationRequest } from '../../types/simulation';
import { load } from '../../libs/stateLoader';

const LoadScenariosButton: React.FC<{
  onLoad: (state: ClientSimulationRequest) => void;
}> = ({ onLoad }) => {
  const inputRef = React.useRef(null);
  const [fileName, setFileName] = React.useState(null);

  const handleLoadClick = () => {
    inputRef.current.click();
  };

  const handleLoad = async e => {
    const { name, contents } = await load(e as Event);
    if (contents) {
      onLoad(contents);
      setFileName(name);
    }
  };

  return (
    <>
      <div>
        <input
          type="file"
          style={{ display: 'none' }}
          ref={inputRef}
          onChange={handleLoad}
        />{' '}
        <button onClick={handleLoadClick}>Load Scenarios</button>
      </div>
      <span
        style={{
          marginLeft: '1em',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <em>{!!fileName && `using ${fileName}`}</em>
      </span>
    </>
  );
};

export default LoadScenariosButton;
