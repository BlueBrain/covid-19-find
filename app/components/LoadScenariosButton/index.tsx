import * as React from 'react';
import { isEqual } from 'lodash';
import { ClientSimulationRequest } from '../../types/simulation';
import { load } from '../../libs/stateLoader';

const LoadScenariosButton: React.FC<{
  onLoad: (state: ClientSimulationRequest) => void;
  state: ClientSimulationRequest;
}> = ({ onLoad, state }) => {
  const inputRef = React.useRef(null);
  const [fileContents, setFileContents] = React.useState(null);
  const [fileName, setFileName] = React.useState(null);
  const [
    fileEquivalencyStateTracker,
    setFileEquivalencyStateTracker,
  ] = React.useState(false);

  const handleLoadClick = () => {
    inputRef.current.click();
  };

  const handleLoad = async e => {
    const { name, contents } = await load(e as Event);
    if (contents) {
      setFileContents(contents);
      setFileName(name);
      onLoad(contents);
    }
  };

  React.useEffect(() => {
    if (!fileContents) {
      return;
    }
    if (isEqual(state, fileContents)) {
      setFileEquivalencyStateTracker(true);
    }
    if (!isEqual(state, fileContents) && fileEquivalencyStateTracker) {
      setFileName(null);
      setFileEquivalencyStateTracker(false);
    }
  }, [state, fileContents]);

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
