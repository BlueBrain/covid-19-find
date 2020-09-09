import * as React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faSpinner,
  faExclamationCircle,
} from '@fortawesome/free-solid-svg-icons';

const AwaitingInput: React.FC<{
  ready: boolean;
  loading: boolean;
  error: Error;
}> = ({ ready, loading, error }) => {
  return (
    <div className="action-box primary">
      <div className="title">
        <div className="number">
          <span>3</span>
        </div>
        <h2 className="underline">
          Visualize the <em>Simulation Model Results</em>
        </h2>
      </div>
      <div className="container">
        {!ready && !error && !loading && (
          <p style={{ color: 'white' }}>
            Please complete the steps to view simulation results
          </p>
        )}
        {loading && !error && <p style={{ color: 'white' }}>Loading</p>}
        {error && (
          <p style={{ color: 'white' }}>
            There was a problem while processing the simulation
          </p>
        )}
      </div>
      <div className="triangle primary">
        <div
          className={`loader ${error ? 'loading' : ''}`}
          style={{ left: '-17px' }}
        >
          <FontAwesomeIcon icon={faExclamationCircle} />
        </div>
        <div className={`loader ${loading ? 'loading' : ''}`}>
          <FontAwesomeIcon icon={faSpinner} pulse />
        </div>
      </div>
    </div>
  );
};

export default AwaitingInput;
